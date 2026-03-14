# Step 10: Analyze User Configuration

function Analyze-Config {
    Info "Analyzing user OpenClaw configuration..."
    
    $cfg = Get-Content $script:OC_CFG -Raw | ConvertFrom-Json
    $agentsList = @($cfg.agents.list)
    $agentCount = $agentsList.Count
    
    Info "Found $agentCount agent(s)"
    
    $tangIds = @("zhongshu","menxia","shangshu","hubu","libu","bingbu","xingbu","gongbu","libu_hr","zaochao")
    $hasTang = $agentsList | Where-Object {$_.id -in $tangIds}
    
    if ($hasTang) {
        Warn "Tang agents exist, skip main config"
        $script:SkipMain = $true
        return
    }
    
    $script:SkipMain = $false
    $script:DefWorkspace = $cfg.agents.defaults.workspace
    $script:AgentsList = $agentsList
    $script:FirstAgent = if ($agentCount -gt 0) { $agentsList[0] } else { $null }
    $script:FirstId = if ($agentCount -gt 0) { $agentsList[0].id } else { $null }
    
    if ($agentCount -le 1) {
        $script:Mode = "SINGLE"
        Info "Mode: Single Agent"
    } else {
        $script:Mode = "MULTI"
        Info "Mode: Multi Agent (first: $script:FirstId)"
    }
}
