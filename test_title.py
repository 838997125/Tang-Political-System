#!/usr/bin/env python3
# Test title validation

import sys
sys.path.insert(0, 'scripts')

# Import functions
from kanban_update import (
    _MIN_TITLE_LEN,
    _sanitize_text,
    _sanitize_title,
    _is_valid_task_title
)

print(f"_MIN_TITLE_LEN = {_MIN_TITLE_LEN}")

test_titles = [
    "制作AI产品经理调研报告",
    "制作《AI产品经理调研报告》",
    "test",
    "这是一个很长的标题用于测试超过六个字符的限制",
]

for title in test_titles:
    print(f"\nOriginal: '{title}' (len={len(title)})")
    sanitized = _sanitize_title(title)
    print(f"Sanitized: '{sanitized}' (len={len(sanitized)})")
    valid, reason = _is_valid_task_title(sanitized)
    print(f"Valid: {valid}, Reason: {reason}")
