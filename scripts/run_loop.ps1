# Edict Data Refresh Loop (Windows)
# Usage: .\run_loop.ps1 [interval_seconds] (default: 15)

param(
    [int]$Interval = 15,
    [int]$ScanInterval = 120
)

$ErrorActionPreference = "Continue"

$SCRIPT_DIR = $PSScriptRoot
if (-not $SCRIPT_DIR) { $SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path }
$REPO_DIR = Split-Path -Parent $SCRIPT_DIR
$LOG = Join-Path $env:TEMP "edict_refresh.log"

Write-Host "Edict Data Refresh Loop Started"
Write-Host "Interval: ${Interval}s"
Write-Host "Log: $LOG"
Write-Host "Press Ctrl+C to stop"

function RotateLog {
    if (Test-Path $LOG) {
        $size = (Get-Item $LOG).Length
        if ($size -gt 10MB) {
            $bak = "$LOG.1"
            if (Test-Path $bak) { Remove-Item $bak -Force }
            Move-Item $LOG $bak -Force
            "Log rotated $(Get-Date)" | Set-Content -Path $LOG
        }
    }
}

function SafeRun($scriptName) {
    $python = if (Get-Command "python" -ErrorAction SilentlyContinue) { "python" } else { "python3" }
    $path = Join-Path $SCRIPT_DIR $scriptName
    $timestamp = Get-Date -Format "HH:mm:ss"
    "$timestamp Running $scriptName" | Add-Content -Path $LOG

    try {
        $output = & $python $path 2>&1
        if ($output) {
            $output | Add-Content -Path $LOG
        }
    } catch {
        $errMsg = $_.Exception.Message
        "$timestamp Error in $scriptName`: $errMsg" | Add-Content -Path $LOG
    }
}

$SCAN_COUNTER = 0
$scripts = @(
    "sync_from_openclaw_runtime.py",
    "sync_agent_config.py",
    "apply_model_changes.py",
    "sync_officials_stats.py",
    "refresh_live_data.py"
)

while ($true) {
    RotateLog

    foreach ($script in $scripts) {
        SafeRun $script
    }

    $SCAN_COUNTER += $Interval
    if ($SCAN_COUNTER -ge $ScanInterval) {
        $SCAN_COUNTER = 0
        try {
            Invoke-RestMethod -Uri "http://127.0.0.1:7891/api/scheduler-scan" -Method POST -Body '{"thresholdSec":180}' -ContentType "application/json" -TimeoutSec 5 | Out-Null
        } catch {}
    }

    Start-Sleep -Seconds $Interval
}
