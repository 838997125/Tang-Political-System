#!/usr/bin/env python3
"""
修复所有 Agent SOUL.md 文件中的 python/python3 命令为 py
"""
import re
from pathlib import Path

BASE_DIR = Path("D:/tools/Tang-Political-System")
AGENTS_DIR = BASE_DIR / "agents"

def fix_soul_md(agent_dir: Path):
    """修复单个 Agent 的 SOUL.md 文件"""
    soul_file = agent_dir / "SOUL.md"
    if not soul_file.exists():
        print(f"[ERR] {agent_dir.name}: SOUL.md 不存在")
        return False
    
    content = soul_file.read_text(encoding='utf-8')
    original_content = content
    
    # 替换 python3 scripts/ 为 py scripts/
    content = re.sub(r'python3\s+scripts/', 'py scripts/', content)
    
    # 替换 python scripts/ 为 py scripts/
    content = re.sub(r'python\s+scripts/', 'py scripts/', content)
    
    if content != original_content:
        soul_file.write_text(content, encoding='utf-8')
        # 统计替换次数
        changes = len(re.findall(r'py scripts/', content)) - len(re.findall(r'py scripts/', original_content))
        print(f"[OK] {agent_dir.name}: 已修复 ({changes} 处)")
        return True
    else:
        print(f"[SKIP] {agent_dir.name}: 无需修改")
        return False

def main():
    """修复所有 Agent"""
    print("=" * 50)
    print("Fix Agent SOUL.md files")
    print("=" * 50)
    
    fixed_count = 0
    total_count = 0
    
    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if agent_dir.is_dir():
            total_count += 1
            if fix_soul_md(agent_dir):
                fixed_count += 1
    
    print("=" * 50)
    print(f"总计: {fixed_count}/{total_count} 个 Agent 已修复")
    print("=" * 50)

if __name__ == "__main__":
    main()
