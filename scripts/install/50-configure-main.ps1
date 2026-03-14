# Step 50: Configure Main Agent
# Only adds Tang Political System activation rules to existing main agent
# Does NOT modify agentDir, workspace, or create new agents

function Configure-MainAgent {
    if ($script:SkipMain) { return }
    
    Info "Configuring main agent for Tang Political System..."
    $cfg = Get-Content $script:OC_CFG -Raw | ConvertFrom-Json
    $rules = Get-TangRules
    
    # Find existing main agent
    $mainAgent = $null
    $mainIndex = -1
    for ($i = 0; $i -lt $cfg.agents.list.Count; $i++) {
        if ($cfg.agents.list[$i].id -eq "main") {
            $mainAgent = $cfg.agents.list[$i]
            $mainIndex = $i
            break
        }
    }
    
    if ($mainAgent) {
        Info "Found existing main agent, adding Tang permissions..."
        
        # Add subagents.allowAgents if not exists
        if (-not $cfg.agents.list[$mainIndex].subagents) {
            $cfg.agents.list[$mainIndex] | Add-Member -NotePropertyName subagents -NotePropertyValue @{allowAgents=@("zhongshu")} -Force
            Log "Added subagents.allowAgents to main"
        } else {
            $existing = $cfg.agents.list[$mainIndex].subagents.allowAgents
            if ($existing -notcontains "zhongshu") {
                $cfg.agents.list[$mainIndex].subagents.allowAgents += "zhongshu"
                Log "Added zhongshu to main's allowAgents"
            }
        }
        
        # Update SOUL.md with Tang rules (append if not already present)
        $dir = $cfg.agents.list[$mainIndex].agentDir
        if ($dir) {
            $soul = "$dir\SOUL.md"
            if (Test-Path $soul) {
                $c = Get-Content $soul -Raw
                if ($c -notmatch "Tang Political System") {
                    Add-Content $soul $rules -NoNewline
                    Log "Updated SOUL.md for main with Tang rules"
                } else {
                    Log "SOUL.md already contains Tang rules"
                }
            } else {
                Log "Warning: SOUL.md not found at $soul"
            }
        }
    } else {
        Info "No main agent found, skipping main configuration"
        Log "Please manually add 'zhongshu' to your primary agent's subagents.allowAgents"
    }
    
    # Save using Python for proper formatting
    $tempFile = [System.IO.Path]::GetTempFileName() + ".json"
    $cfg | ConvertTo-Json -Depth 10 | Set-Content $tempFile -Encoding UTF8
    
    # Use raw string for Python script to avoid escape issues
    $tempFileEscaped = $tempFile -replace '\\', '/'
    $ocCfgEscaped = $script:OC_CFG -replace '\\', '/'
    
    $pyScript = @"
import json
with open('$tempFileEscaped', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
with open('$ocCfgEscaped', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
"@
    $pyScript | py -
    Remove-Item $tempFile -ErrorAction SilentlyContinue
    
    Log "Saved openclaw.json"
}
