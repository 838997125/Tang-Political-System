"""
文件锁工具 — 防止多进程并发读写 JSON 文件导致数据丢失。
支持 Windows 和 Unix/Linux/macOS 跨平台。

用法:
    from file_lock import atomic_json_update, atomic_json_read

    # 原子读取
    data = atomic_json_read(path, default=[])

    # 原子更新（读 → 修改 → 写回，全程持锁）
    def modifier(tasks):
        tasks.append(new_task)
        return tasks
    atomic_json_update(path, modifier, default=[])
"""
import json
import os
import pathlib
import tempfile
import platform
from typing import Any, Callable

# 检测操作系统
IS_WINDOWS = platform.system() == 'Windows'

if IS_WINDOWS:
    import msvcrt
else:
    import fcntl


def _lock_file_windows(fd: int, exclusive: bool = True) -> bool:
    """Windows 文件锁定实现"""
    try:
        if exclusive:
            # 排他锁
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
        else:
            # 共享锁
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            msvcrt.locking(fd, msvcrt.LK_RLCK, 1)
        return True
    except (IOError, OSError):
        return False


def _unlock_file_windows(fd: int) -> bool:
    """Windows 文件解锁实现"""
    try:
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        return True
    except (IOError, OSError):
        return False


def _lock_path(path: pathlib.Path) -> pathlib.Path:
    return path.parent / (path.name + '.lock')


def atomic_json_read(path: pathlib.Path, default: Any = None) -> Any:
    """持锁读取 JSON 文件。"""
    lock_file = _lock_path(path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    fd = None
    try:
        if IS_WINDOWS:
            # Windows: 使用文件锁定
            fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
            _lock_file_windows(fd, exclusive=False)
        else:
            # Unix: 使用 fcntl
            fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
            fcntl.flock(fd, fcntl.LOCK_SH)

        try:
            return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default
        except Exception:
            return default
    finally:
        if fd is not None:
            if IS_WINDOWS:
                _unlock_file_windows(fd)
            else:
                fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)


def atomic_json_update(
    path: pathlib.Path,
    modifier: Callable[[Any], Any],
    default: Any = None,
) -> Any:
    """
    原子地读取 → 修改 → 写回 JSON 文件。
    modifier(data) 应返回修改后的数据。
    使用临时文件 + rename 保证写入原子性。
    """
    lock_file = _lock_path(path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    fd = None
    try:
        if IS_WINDOWS:
            # Windows: 使用文件锁定
            fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
            _lock_file_windows(fd, exclusive=True)
        else:
            # Unix: 使用 fcntl
            fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
            fcntl.flock(fd, fcntl.LOCK_EX)

        # Read
        try:
            data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else default
        except Exception:
            data = default

        # Modify
        result = modifier(data)

        # Atomic write via temp file + rename
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), suffix='.tmp', prefix=path.stem + '_'
        )
        try:
            with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, str(path))
        except Exception:
            try:
                os.unlink(tmp_path)
            except FileNotFoundError:
                pass
            raise
        return result
    finally:
        if fd is not None:
            if IS_WINDOWS:
                _unlock_file_windows(fd)
            else:
                fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)


def atomic_json_write(path: pathlib.Path, data: Any) -> None:
    """原子写入 JSON 文件（持排他锁 + tmpfile rename）。
    直接写入，不读取现有内容（避免 atomic_json_update 的多余读开销）。
    """
    lock_file = _lock_path(path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    fd = None
    try:
        if IS_WINDOWS:
            # Windows: 使用文件锁定
            fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
            _lock_file_windows(fd, exclusive=True)
        else:
            # Unix: 使用 fcntl
            fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
            fcntl.flock(fd, fcntl.LOCK_EX)

        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), suffix='.tmp', prefix=path.stem + '_'
        )
        try:
            with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, str(path))
        except Exception:
            try:
                os.unlink(tmp_path)
            except FileNotFoundError:
                pass
            raise
    finally:
        if fd is not None:
            if IS_WINDOWS:
                _unlock_file_windows(fd)
            else:
                fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
