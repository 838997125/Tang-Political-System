# Edict Windows Background Stopper
# Usage: .\stop-background.ps1
# 停止后台运行的数据刷新循环和看板服务器

$REPO_DIR = $PSScriptRoot
if (-not $REPO_DIR) { $REPO_DIR = Get-Location }

Write-Host ""
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host "  Stopping Edict Background Services" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host ""

$pidsFile = Join-Path $REPO_DIR ".running_pids"

if (Test-Path $pidsFile) {
    $pids = Get-Content -Path $pidsFile
    $pidList = $pids -split ","
    
    foreach ($pid in $pidList) {
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Stop-Process -Id $pid -Force
            Write-Host "Stopped process: $pid ($($process.ProcessName))" -ForegroundColor Green
        } catch {
            Write-Host "Process $pid not found or already stopped" -ForegroundColor Yellow
        }
    }
    
    Remove-Item -Path $pidsFile -Force
    Write-Host "Removed PID file" -ForegroundColor Gray
} else {
    Write-Host "No PID file found. Trying to find Edict processes..." -ForegroundColor Yellow
    
    # Try to find by process name
    $processes = Get-Process | Where-Object { $_.ProcessName -like "*python*" -or $_.ProcessName -like "*powershell*" }
    $found = $false
    
    foreach ($proc in $processes) {
        try {
            $cmdLine = (Get-WmiObject Win32_Process -Filter "ProcessId=$($proc.Id)").CommandLine
            if ($cmdLine -like "*Tang-Political-System*" -or $cmdLine -like "*edict*") {
                Stop-Process -Id $proc.Id -Force
                Write-Host "Stopped process: $($proc.Id) ($($proc.ProcessName))" -ForegroundColor Green
                $found = $true
            }
        } catch {}
    }
    
    if (-not $found) {
        Write-Host "No Edict processes found" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Done!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
