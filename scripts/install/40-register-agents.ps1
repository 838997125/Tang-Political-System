# Step 40: Register Tang Agents

function Register-TangAgents {
    Info "Registering Tang Political System Agents..."
    
    $cfg = Get-Content $script:OC_CFG -Raw | ConvertFrom-Json
    
    # Get default model from config
    $defaultModelObj = $cfg.agents.defaults.model
    # Extract the model string from the primary field (agents.list expects string, not object)
    if ($defaultModelObj -is [System.Management.Automation.PSCustomObject] -and $defaultModelObj.primary) {
        $defaultModel = $defaultModelObj.primary
    } else {
        $defaultModel = $defaultModelObj
    }
    Info "Using default model: $defaultModel"
    
    $TANG_AGENTS = @(
        @{ id = "zhongshu"; model = $defaultModel; subagents = @{ allowAgents = @("menxia", "shangshu") } },
        @{ id = "menxia";   model = $defaultModel; subagents = @{ allowAgents = @("zhongshu", "shangshu") } },
        @{ id = "shangshu"; model = $defaultModel; subagents = @{ allowAgents = @("zhongshu", "menxia", "hubu", "libu", "bingbu", "xingbu", "gongbu", "libu_hr") } },
        @{ id = "hubu";     model = $defaultModel; subagents = @{ allowAgents = @("shangshu") } },
        @{ id = "libu";     model = $defaultModel; subagents = @{ allowAgents = @("shangshu") } },
        @{ id = "bingbu";   model = $defaultModel; subagents = @{ allowAgents = @("shangshu") } },
        @{ id = "xingbu";   model = $defaultModel; subagents = @{ allowAgents = @("shangshu") } },
        @{ id = "gongbu";   model = $defaultModel; subagents = @{ allowAgents = @("shangshu") } },
        @{ id = "libu_hr";  model = $defaultModel; subagents = @{ allowAgents = @("shangshu") } },
        @{ id = "zaochao";  model = $defaultModel; subagents = @{ allowAgents = @() } }
    )
    
    $existingIds = @()
    foreach ($a in $cfg.agents.list) { $existingIds += $a.id }
    
    $added = 0
    foreach ($ag in $TANG_AGENTS) {
        $agId = $ag.id
        if ($existingIds -contains $agId) {
            # Agent 已存在，检查是否需要添加 model 字段
            for ($i = 0; $i -lt $cfg.agents.list.Count; $i++) {
                if ($cfg.agents.list[$i].id -eq $agId) {
                    if (-not $cfg.agents.list[$i].model) {
                        $cfg.agents.list[$i] | Add-Member -NotePropertyName model -NotePropertyValue $defaultModel -Force
                        Log "Updated: $agId (added model)"
                    }
                    break
                }
            }
            continue
        }
        
        $ws = "$REPO_DIR\workspaces\$agId"
        $agentDir = "$REPO_DIR\agents\$agId"
        
        # Create agentDir directory to prevent OpenClaw from creating it in ~/.openclaw/agents/
        # SOUL.md already exists in REPO_DIR/agents/$agId/, no need to copy
        New-Item -ItemType Directory -Force -Path $agentDir | Out-Null
        Log "Created agentDir for: $agId"
        
        # Use ordered dictionary to ensure consistent field order: id -> model -> workspace -> agentDir -> subagents
        $entry = [ordered]@{
            id = $agId
            model = $defaultModel
            workspace = $ws
            agentDir = $agentDir
        }
        if ($ag.subagents) {
            $entry.subagents = $ag.subagents
        }
        
        $cfg.agents.list += $entry
        $added++
        Log "Added: $agId"
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
    
    Log "Saved openclaw.json with $added new agents"
}
