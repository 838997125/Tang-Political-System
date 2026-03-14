#!/usr/bin/env python3
import sys
sys.path.insert(0, 'scripts')
from kanban_update import save_and_push, load

# Create a test task
task = {
    'id': 'JJC-TEST-001',
    'title': '测试任务',
    'official': '中书令',
    'org': '中书省',
    'state': 'Zhongshu',
    'now': '等待中书省接旨',
    'eta': '-',
    'block': '无',
    'output': '',
    'ac': '',
    'flow_log': [],
    'updatedAt': '2026-03-14T00:00:00Z'
}

# Save and push
save_and_push(task)

# Verify
tasks = load()
print(f'Tasks after save: {len(tasks)}')
for t in tasks:
    print(f'  - {t.get("id")}: {t.get("title")}')
