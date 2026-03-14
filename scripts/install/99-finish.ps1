# Step 99: Finish Installation

function Finish-Install {
    Log "Configuration complete!"
    
    if ($script:SkipMain) {
        Info "Tang agents already configured, skipped main agent setup"
    } elseif ($script:Mode -eq "SINGLE") {
        Info "Mode: Single Agent"
        Info "Main agent configured with zhongshu access"
    } else {
        Info "Mode: Multi Agent"
        Info "First agent ($script:FirstId) configured with zhongshu access"
    }
    
    Write-Host ""
    Write-Host "Tang Political System installed and started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Services Status:"
    Write-Host "  - Dashboard: http://127.0.0.1:7891"
    Write-Host "  - Data Refresh: Running in background"
    Write-Host ""
    Write-Host "Quick start:"
    Write-Host "  - Type 'help' to see activation rules"
    Write-Host "  - Type '朕要...' for emperor commands"
    Write-Host "  - Type '宣兵部' to call bingbu"
    Write-Host "  - Type '看板' to open dashboard"
    Write-Host ""
    Write-Host "To stop services:"
    Write-Host "  - Run .\scripts\stop-all.ps1"
    Write-Host ""
}