#!/usr/bin/env python3
"""
看板任务更新工具 - Edict 兼容层

保持与旧版完全相同的 CLI 接口，内部改为调用 Edict REST API。
如果 API 不可用，降级回写 JSON 文件（过渡期保障）。

用法（与旧版 100% 兼容）:
  python3 kanban_update.py create JJC-20260223-012 "任务标题" Zhongshu 中书省 中书令
  python3 kanban_update.py state JJC-20260223-012 Menxia "规划方案已提交门下省"
  python3 kanban_update.py flow JJC-20260223-012 "中书省" "门下省" "规划方案提交审核"
  python3 kanban_update.py done JJC-20260223-012 "/path/to/output" "任务完成摘要"
  python3 kanban_update.py todo JJC-20260223-012 1 "实现API接口" in-progress
  python3 kanban_update.py progress JJC-20260223-012 "正在分析需求" "1.调研✅|2.文档🔄|3.原型"
"""

import json
import logging
import os
import re
import sys
import pathlib

log = logging.getLogger('kanban')
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(message)s', datefmt='%H:%M:%S')

# Edict API 地址 — 环境变量 > 默认 localhost:8000
EDICT_API_URL = os.environ.get('EDICT_API_URL', 'http://localhost:8000')

# 是否启用 API 模式（EDICT_MODE=api | json | auto）
EDICT_MODE = os.environ.get('EDICT_MODE', 'auto').lower()

# ── 文本清洗逻辑（与旧版完全一致） ──

_MIN_TITLE_LEN = 6
_JUNK_TITLES = {
    '?', '？', '好', '好的', '是', '否', '不', '不是', '对', '了解', '收到',
    '嗯', '哦', '知道了', '开启了么', '可以', '不行', '行', 'ok', 'yes', 'no',
    '你去开启', '测试', '试试', '看看',
}

STATE_ORG_MAP = {
    'Taizi': '太子', 'Zhongshu': '中书省', 'Menxia': '门下省', 'Assigned': '尚书省',
    'Doing': '执行中', 'Review': '尚书省', 'Done': '完成', 'Blocked': '阻塞',
}

# State → Edict TaskState value 映射
_STATE_TO_EDICT = {
    'Taizi': 'taizi', 'Zhongshu': 'zhongshu', 'Menxia': 'menxia',
    'Assigned': 'assigned', 'Next': 'next', 'Doing': 'doing',
    'Review': 'review', 'Done': 'done', 'Blocked': 'blocked',
    'Cancelled': 'cancelled', 'Pending': 'pending',
}


def _sanitize_text(raw, max_len=80):
    t = (raw or '').strip()
    t = re.split(r'\n*Conversation\b', t, maxsplit=1)[0].strip()
    t = re.split(r'\n*```', t, maxsplit=1)[0].strip()
    t = re.sub(r'[/\\.~][A-Za-z0-9_\-./]+(?:\.(?:py|js|ts|json|md|sh|yaml|yml|txt|csv|html|css|log))?', '', t)
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'^(传旨|下旨)([（(][^)）]*[)）])?[：:\uff1a]\s*', '', t)
    t = re.sub(r'(message_id|session_id|chat_id|open_id|user_id|tenant_key)\s*[:=]\s*\S+', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) > max_len:
        t = t[:max_len] + '…'
    return t


def _sanitize_title(raw):
    return _sanitize_text(raw, 80)


def _sanitize_remark(raw):
    return _sanitize_text(raw, 120)


def _is_valid_task_title(title):
    t = (title or '').strip()
    if len(t) < _MIN_TITLE_LEN:
        return False, f'标题过短（{len(t)}<{_MIN_TITLE_LEN}字），疑似非旨意'
    if t.lower() in _JUNK_TITLES:
        return False, f'标题 "{t}" 不是有效旨意'
    if re.fullmatch(r'[\s?？!！.。,，…·\-—~]+', t):
        return False, '标题只有标点符号'
    if re.match(r'^[/\\~.]', t) or re.search(r'/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', t):
        return False, f'标题看起来像文件路径，请用中文概括任务'
    if re.fullmatch(r'[\s\W]*', t):
        return False, '标题清洗后为空'
    return True, ''


def _infer_agent_id():
    for k in ('OPENCLAW_AGENT_ID', 'OPENCLAW_AGENT', 'AGENT_ID'):
        v = (os.environ.get(k) or '').strip()
        if v:
            return v
    cwd = str(pathlib.Path.cwd())
    m = re.search(r'workspace-([a-zA-Z0-9_\-]+)', cwd)
    if m:
        return m.group(1)
    return 'system'


# ── API 客户端 ──

def _api_available() -> bool:
    """检查 Edict API 是否可用。"""
    if EDICT_MODE == 'json':
        return False
    if EDICT_MODE == 'api':
        return True
    # auto mode: 探测
    try:
        import urllib.request
        req = urllib.request.Request(f"{EDICT_API_URL}/health", method='GET')
        req.add_header('Accept', 'application/json')
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def _api_post(path: str, data: dict) -> dict | None:
    """向 Edict API 发送 POST 请求。"""
    try:
        import urllib.request
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            f"{EDICT_API_URL}{path}",
            data=body,
            method='POST',
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        log.warning(f'API 调用失败 ({path}): {e}')
        return None


def _api_put(path: str, data: dict) -> dict | None:
    """向 Edict API 发送 PUT 请求。"""
    try:
        import urllib.request
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            f"{EDICT_API_URL}{path}",
            data=body,
            method='PUT',
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        log.warning(f'API 调用失败 ({path}): {e}')
        return None


# ── 命令 → API 调用 ──

# 缓存 API 可用性
_api_ok = None


def _check_api():
    global _api_ok
    if _api_ok is None:
        _api_ok = _api_available()
        if _api_ok:
            log.debug('Edict API 可用，使用 API 模式')
        else:
            log.debug('Edict API 不可用，降级到 JSON 模式')
    return _api_ok


def _fallback_json():
    """降级：导入旧版 kanban_update 逻辑。"""
    # 回退到同目录下的旧版实现
    old_path = pathlib.Path(__file__).parent / 'kanban_update_legacy.py'
    if old_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('kanban_legacy', old_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    return None


def cmd_create(task_id, title, state, org, official, remark=None):
    title = _sanitize_title(title)
    valid, reason = _is_valid_task_title(title)
    if not valid:
        log.warning(f'⚠️ 拒绝创建 {task_id}：{reason}')
        print(f'[看板] 拒绝创建：{reason}', flush=True)
        return

    if _check_api():
        edict_state = _STATE_TO_EDICT.get(state, state.lower())
        result = _api_post('/api/tasks', {
            'title': title,
            'description': remark or f'下旨：{title}',
            'priority': '中',
            'assignee_org': org,
            'creator': official,
            'tags': [task_id],
            'meta': {'legacy_id': task_id, 'legacy_state': state},
        })
        if result:
            log.info(f'✅ 创建 {task_id} → Edict {result.get("task_id", "?")} | {title[:30]}')
            return

    # 降级
    legacy = _fallback_json()
    if legacy:
        legacy.cmd_create(task_id, title, state, org, official, remark)
    else:
        log.error(f'无法创建任务：API 不可用且无降级模块')


def cmd_state(task_id, new_state, now_text=None):
    if _check_api():
        edict_state = _STATE_TO_EDICT.get(new_state, new_state.lower())
        agent = _infer_agent_id()
        # 需要先通过 legacy_id 查找 edict task_id
        # 暂用 legacy_id tag 搜索
        result = _api_post(f'/api/tasks/by-legacy/{task_id}/transition', {
            'new_state': edict_state,
            'agent': agent,
            'reason': now_text or f'状态更新为 {new_state}',
        })
        if result:
            log.info(f'✅ {task_id} 状态更新 → {new_state}')
            return

    legacy = _fallback_json()
    if legacy:
        legacy.cmd_state(task_id, new_state, now_text)
    else:
        log.error(f'无法更新状态：API 不可用且无降级模块')


def cmd_flow(task_id, from_dept, to_dept, remark):
    clean_remark = _sanitize_remark(remark)
    if _check_api():
        agent = _infer_agent_id()
        result = _api_post(f'/api/tasks/by-legacy/{task_id}/progress', {
            'agent': agent,
            'content': f'流转: {from_dept} → {to_dept} | {clean_remark}',
        })
        if result:
            log.info(f'✅ {task_id} 流转记录: {from_dept} → {to_dept}')
            return

    legacy = _fallback_json()
    if legacy:
        legacy.cmd_flow(task_id, from_dept, to_dept, remark)


def cmd_done(task_id, output_path='', summary=''):
    if _check_api():
        agent = _infer_agent_id()
        result = _api_post(f'/api/tasks/by-legacy/{task_id}/transition', {
            'new_state': 'done',
            'agent': agent,
            'reason': summary or '任务已完成',
        })
        if result:
            log.info(f'✅ {task_id} 已完成')
            return

    legacy = _fallback_json()
    if legacy:
        legacy.cmd_done(task_id, output_path, summary)


def cmd_block(task_id, reason):
    if _check_api():
        agent = _infer_agent_id()
        result = _api_post(f'/api/tasks/by-legacy/{task_id}/transition', {
            'new_state': 'blocked',
            'agent': agent,
            'reason': reason,
        })
        if result:
            log.warning(f'⚠️ {task_id} 已阻塞: {reason}')
            return

    legacy = _fallback_json()
    if legacy:
        legacy.cmd_block(task_id, reason)


def cmd_progress(task_id, now_text, todos_pipe='', tokens=0, cost=0.0, elapsed=0):
    clean = _sanitize_remark(now_text)

    # 解析 todos
    parsed_todos = None
    if todos_pipe:
        new_todos = []
        for i, item in enumerate(todos_pipe.split('|'), 1):
            item = item.strip()
            if not item:
                continue
            if item.endswith('✅'):
                status = 'completed'
                title = item[:-1].strip()
            elif item.endswith('🔄'):
                status = 'in-progress'
                title = item[:-1].strip()
            else:
                status = 'not-started'
                title = item
            new_todos.append({'id': str(i), 'title': title, 'status': status})
        if new_todos:
            parsed_todos = new_todos

    if _check_api():
        agent = _infer_agent_id()
        # 更新进度
        _api_post(f'/api/tasks/by-legacy/{task_id}/progress', {
            'agent': agent,
            'content': clean,
        })
        # 更新 todos
        if parsed_todos:
            _api_put(f'/api/tasks/by-legacy/{task_id}/todos', {
                'todos': parsed_todos,
            })
        log.info(f'📡 {task_id} 进展: {clean[:40]}...')
        return

    legacy = _fallback_json()
    if legacy:
        legacy.cmd_progress(task_id, now_text, todos_pipe, tokens, cost, elapsed)


def cmd_todo(task_id, todo_id, title, status='not-started', detail=''):
    if status not in ('not-started', 'in-progress', 'completed'):
        status = 'not-started'

    if _check_api():
        # 读取现有 todos，更新后写回
        # 这里简化处理，直接发进度更新
        agent = _infer_agent_id()
        _api_post(f'/api/tasks/by-legacy/{task_id}/progress', {
            'agent': agent,
            'content': f'Todo #{todo_id}: {title} → {status}',
        })
        log.info(f'✅ {task_id} todo: {todo_id} → {status}')
        return

    legacy = _fallback_json()
    if legacy:
        legacy.cmd_todo(task_id, todo_id, title, status, detail)


# ── CLI 分发 ──

_CMD_MIN_ARGS = {
    'create': 6, 'state': 3, 'flow': 5, 'done': 2, 'block': 3, 'todo': 4, 'progress': 3,
}

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    if cmd in _CMD_MIN_ARGS and len(args) < _CMD_MIN_ARGS[cmd]:
        print(f'错误："{cmd}" 命令至少需要 {_CMD_MIN_ARGS[cmd]} 个参数，实际 {len(args)} 个')
        print(__doc__)
        sys.exit(1)

    if cmd == 'create':
        cmd_create(args[1], args[2], args[3], args[4], args[5], args[6] if len(args) > 6 else None)
    elif cmd == 'state':
        cmd_state(args[1], args[2], args[3] if len(args) > 3 else None)
    elif cmd == 'flow':
        cmd_flow(args[1], args[2], args[3], args[4])
    elif cmd == 'done':
        cmd_done(args[1], args[2] if len(args) > 2 else '', args[3] if len(args) > 3 else '')
    elif cmd == 'block':
        cmd_block(args[1], args[2])
    elif cmd == 'todo':
        todo_pos = []
        todo_detail = ''
        ti = 1
        while ti < len(args):
            if args[ti] == '--detail' and ti + 1 < len(args):
                todo_detail = args[ti + 1]; ti += 2
            else:
                todo_pos.append(args[ti]); ti += 1
        cmd_todo(
            todo_pos[0] if len(todo_pos) > 0 else '',
            todo_pos[1] if len(todo_pos) > 1 else '',
            todo_pos[2] if len(todo_pos) > 2 else '',
            todo_pos[3] if len(todo_pos) > 3 else 'not-started',
            detail=todo_detail,
        )
    elif cmd == 'progress':
        pos_args = []
        kw = {}
        i = 1
        while i < len(args):
            if args[i] == '--tokens' and i + 1 < len(args):
                kw['tokens'] = args[i + 1]; i += 2
            elif args[i] == '--cost' and i + 1 < len(args):
                kw['cost'] = args[i + 1]; i += 2
            elif args[i] == '--elapsed' and i + 1 < len(args):
                kw['elapsed'] = args[i + 1]; i += 2
            else:
                pos_args.append(args[i]); i += 1
        cmd_progress(
            pos_args[0] if len(pos_args) > 0 else '',
            pos_args[1] if len(pos_args) > 1 else '',
            pos_args[2] if len(pos_args) > 2 else '',
            tokens=kw.get('tokens', 0),
            cost=kw.get('cost', 0.0),
            elapsed=kw.get('elapsed', 0),
        )
    else:
        print(__doc__)
        sys.exit(1)
