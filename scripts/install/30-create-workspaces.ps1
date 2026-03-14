# Step 30: Create Workspaces

function Create-Workspaces {
    Info "Creating Agent Workspaces in project directory..."
    
    $AGENTS = @("zhongshu", "menxia", "shangshu", "hubu", "libu", "bingbu", "xingbu", "gongbu", "libu_hr", "zaochao")
    $WSDir = "$REPO_DIR\workspaces"
    
    New-Item -ItemType Directory -Force -Path $WSDir | Out-Null
    
    foreach ($a in $AGENTS) {
        $ws = "$WSDir\$a"
        New-Item -ItemType Directory -Force -Path "$ws\skills" | Out-Null
        New-Item -ItemType Directory -Force -Path "$ws\memory" | Out-Null
        
        if (Test-Path "$REPO_DIR\agents\$a\SOUL.md") {
            $c = Get-Content "$REPO_DIR\agents\$a\SOUL.md" -Raw
            $c = $c.Replace('__REPO_DIR__', $REPO_DIR)
            Set-Content "$ws\SOUL.md" $c -NoNewline
        }
        
        $content = @"
# AGENTS.md

1. Reply '已接旨' when receiving tasks.
2. Output must include: Task ID, Result, Evidence/File Path, Blockers.
3. Request dispatch from Shangshu when collaboration needed.

## Agent Directory
This agent is located at: $REPO_DIR\agents\$a
"@
        Set-Content "$ws\AGENTS.md" $content
        Log "Workspace: $a"
    }
}
