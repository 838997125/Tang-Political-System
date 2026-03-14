# Edict Windows Background Launcher
# Usage: .\start-background.ps1 [-Port 7891]
# 后台运行数据刷新循环和看板服务器

param(
    [int]$Port = 7891
)

$SCRIPT_DIR = $PSScriptRoot
if (-not $SCRIPT_DIR) { $SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path }
$REPO_DIR = Split-Path -Parent $SCRIPT_DIR

Write-Host ""
Write-Host "==========================================" -ForegroundColor Blue
Write-Host "  Edict - Background Launcher" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

# Check dependencies
$pythonCmd = if (Get-Command "py" -ErrorAction SilentlyContinue) { "py" }
              elseif (Get-Command "python" -ErrorAction SilentlyContinue) { "python" }
              else { "python3" }
if (-not (Get-Command $pythonCmd -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command "openclaw" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: openclaw CLI not found. Please install OpenClaw first" -ForegroundColor Red
    exit 1
}

# Check data directory
$dataDir = Join-Path $REPO_DIR "data"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
}

# Create log directory
$logDir = Join-Path $REPO_DIR "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$loopLog = Join-Path $logDir "run_loop.log"
$loopErrLog = Join-Path $logDir "run_loop.err.log"
$serverLog = Join-Path $logDir "server.log"
$serverErrLog = Join-Path $logDir "server.err.log"

# Start data refresh loop (background, hidden window)
Write-Host "Starting data refresh loop (background)..." -ForegroundColor Cyan
$loopScript = Join-Path $REPO_DIR "scripts\run_loop.ps1"
if (Test-Path $loopScript) {
    $loopProcess = Start-Process powershell -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$loopScript`"" -WorkingDirectory $REPO_DIR -PassThru -RedirectStandardOutput $loopLog -RedirectStandardError $loopErrLog
    Write-Host "Data refresh loop started (PID: $($loopProcess.Id))" -ForegroundColor Green
    Write-Host "Log: $loopLog" -ForegroundColor Gray
} else {
    Write-Host "Warning: run_loop.ps1 not found" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# Start dashboard server (background, hidden window)
Write-Host ""
Write-Host "Starting dashboard server (background)..." -ForegroundColor Cyan
$serverScript = Join-Path $REPO_DIR "dashboard\server.py"
if (Test-Path $serverScript) {
    $serverProcess = Start-Process $pythonCmd -ArgumentList "$serverScript --port $Port" -WorkingDirectory $REPO_DIR -PassThru -RedirectStandardOutput $serverLog -RedirectStandardError $serverErrLog -WindowStyle Hidden
    Write-Host "Dashboard server started (PID: $($serverProcess.Id))" -ForegroundColor Green
    Write-Host "Log: $serverLog" -ForegroundColor Gray
    Write-Host ""
    Write-Host "URL: http://127.0.0.1:$Port" -ForegroundColor Cyan
} else {
    Write-Host "Error: dashboard/server.py not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Services running in background!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Commands:" -ForegroundColor White
Write-Host "  View logs: Get-Content $serverLog -Tail 20" -ForegroundColor Gray
Write-Host "  View errors: Get-Content $serverErrLog -Tail 20" -ForegroundColor Gray
Write-Host "  Stop all:  Stop-Process -Id $($loopProcess.Id),$($serverProcess.Id)" -ForegroundColor Gray
Write-Host ""

# Save PIDs to file for easy stopping
$pidsFile = Join-Path $REPO_DIR ".running_pids"
"$($loopProcess.Id),$($serverProcess.Id)" | Set-Content -Path $pidsFile
Write-Host "PIDs saved to: $pidsFile" -ForegroundColor Gray
