#!/usr/bin/env python3
"""
同步 agents/ 目录下的 SOUL.md 到 workspaces/ 目录
"""
from pathlib import Path
import shutil

BASE_DIR = Path("D:/tools/Tang-Political-System")
AGENTS_DIR = BASE_DIR / "agents"
WORKSPACES_DIR = BASE_DIR / "workspaces"

def sync_soul_md(agent_name: str):
    """同步单个 Agent 的 SOUL.md"""
    source = AGENTS_DIR / agent_name / "SOUL.md"
    target = WORKSPACES_DIR / agent_name / "SOUL.md"
    
    if not source.exists():
        print(f"[SKIP] {agent_name}: agents/{agent_name}/SOUL.md 不存在")
        return False
    
    if not target.parent.exists():
        print(f"[ERR] {agent_name}: workspaces/{agent_name}/ 目录不存在")
        return False
    
    shutil.copy2(source, target)
    print(f"[OK] {agent_name}: SOUL.md 已同步")
    return True

def main():
    """同步所有 Agent"""
    print("=" * 50)
    print("Sync SOUL.md: agents/ -> workspaces/")
    print("=" * 50)
    
    synced_count = 0
    total_count = 0
    
    # 获取所有 agent 目录
    agent_names = [d.name for d in AGENTS_DIR.iterdir() if d.is_dir()]
    
    for agent_name in sorted(agent_names):
        total_count += 1
        if sync_soul_md(agent_name):
            synced_count += 1
    
    print("=" * 50)
    print(f"Total: {synced_count}/{total_count} agents synced")
    print("=" * 50)

if __name__ == "__main__":
    main()
