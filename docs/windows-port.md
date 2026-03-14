# Edict Windows 移植文档

> 本文档汇总 Edict 项目在 Windows 系统上的移植过程、技术方案和完成状态。

---

## 核心结论

Edict 项目已成功移植到 Windows 系统。主要修改包括：

1. **文件锁模块** (`scripts/file_lock.py`) - 使用 `msvcrt` 实现 Windows 文件锁定
2. **进程检测** (`dashboard/server.py`) - 使用 `psutil` 或 Windows 原生命令
3. **安装脚本** (`install.ps1`) - PowerShell 版本的安装程序
4. **数据刷新脚本** (`scripts/run_loop.ps1`) - PowerShell 版本的数据循环刷新

---

## 移植技术方案

### 1. 文件锁机制 (`scripts/file_lock.py`)

**问题**: 原代码使用 `fcntl` 模块（仅 Unix/Linux/macOS 可用）

**解决**: 添加 Windows 支持，使用 `msvcrt` 实现跨平台文件锁

主要变更:
- 检测操作系统平台 (`IS_WINDOWS = platform.system() == 'Windows'`)
- Windows 使用 `msvcrt.locking()` 实现文件锁
- Unix/Linux/macOS 继续使用 `fcntl.flock()`

### 2. 进程管理 (`dashboard/server.py`)

**问题**: 使用 `pgrep` 命令检测进程（仅 Unix 可用），硬编码 `python3` 命令

**解决**:
- 添加 `_get_python_cmd()` 函数自动检测 `python` 或 `python3`
- 修改 `_check_gateway_alive()` 和 `_check_agent_process()` 支持 Windows
- Windows 优先使用 `psutil`，回退到 `wmic`/`tasklist`

### 3. Shell 脚本 (`install.sh`, `scripts/run_loop.sh`)

**问题**: Bash 脚本无法在 Windows 直接运行

**解决**: 创建 PowerShell 版本的安装脚本和数据刷新脚本

### 4. 路径处理

**问题**: 硬编码 `/` 路径分隔符和 Unix 路径格式

**解决**: 使用 `pathlib.Path` 统一处理跨平台路径

---

## 移植文件清单

| 文件 | 状态 | 说明 |
|------|------|------|
| `scripts/file_lock.py` | ✅ 完成 | 替换 fcntl 为 Windows 兼容实现 |
| `dashboard/server.py` | ✅ 完成 | 替换 pgrep 为 psutil |
| `scripts/run_loop.sh` | ✅ 完成 | 创建 `scripts/run_loop.ps1` |
| `install.sh` | ✅ 完成 | 创建 `install.ps1` |
| `scripts/kanban_update.py` | ✅ 兼容 | 依赖 file_lock.py |
| `scripts/skill_manager.py` | ✅ 兼容 | 无需修改 |
| `scripts/utils.py` | ✅ 兼容 | 无需修改 |
| `scripts/sync_*.py` | ✅ 兼容 | 依赖 file_lock.py |

---

## 新增文件

1. `install.ps1` - Windows 安装脚本
2. `scripts/run_loop.ps1` - Windows 数据刷新循环
3. `start-windows.ps1` - Windows 一键启动脚本
4. `docs/windows-install.md` - Windows 安装指南
5. `docs/windows-port.md` - 本移植文档

---

## 修改文件

1. `scripts/file_lock.py` - 添加 Windows 文件锁支持
   - 保留 Unix `fcntl` 实现
   - 新增 Windows `msvcrt` 实现
   - 自动检测操作系统

---

## 安装步骤

详见 [Windows 安装指南](./windows-install.md)

---

## 历史文档归档

本文档合并了以下历史文档的内容：
- `WINDOWS_PORT.md` - 移植技术方案
- `WINDOWS_PORT_COMPLETE.md` - 移植完成报告
- `WINDOWS_PORT_SUMMARY.md` - 移植完成总结
