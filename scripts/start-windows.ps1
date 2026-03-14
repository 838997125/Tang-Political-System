# Edict Windows Launcher
# Usage: .\start-windows.ps1 [-SkipLoop] [-Port 7891]

param(
    [switch]$SkipLoop,
    [int]$Port = 7891
)

$REPO_DIR = $PSScriptRoot
if (-not $REPO_DIR) { $REPO_DIR = Get-Location }

Write-Host ""
Write-Host "==========================================" -ForegroundColor Blue
Write-Host "  Edict - Windows Launcher" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

# Check dependencies
# Windows优先检测 py，然后是 python
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

# Start data refresh loop (background)
if (-not $SkipLoop) {
    Write-Host "Starting data refresh loop..." -ForegroundColor Cyan
    $loopScript = Join-Path $REPO_DIR "scripts\run_loop.ps1"
    if (Test-Path $loopScript) {
        Start-Process powershell -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$loopScript`"" -WorkingDirectory $REPO_DIR
        Write-Host "Data refresh loop started (running in background)" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Warning: run_loop.ps1 not found" -ForegroundColor Yellow
    }
}

# Start dashboard server
Write-Host ""
Write-Host "Starting dashboard server..." -ForegroundColor Cyan
$serverScript = Join-Path $REPO_DIR "dashboard\server.py"
if (Test-Path $serverScript) {
    Write-Host "Port: $Port" -ForegroundColor Gray
    Write-Host "URL: http://127.0.0.1:$Port" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press Ctrl+C to stop server" -ForegroundColor Yellow
    Write-Host ""

    Set-Location $REPO_DIR
    & $pythonCmd $serverScript --port $Port
} else {
    Write-Host "Error: dashboard/server.py not found" -ForegroundColor Red
    exit 1
}
