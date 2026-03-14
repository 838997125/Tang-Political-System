# Start Run Loop in Background
$ErrorActionPreference = "Continue"

$REPO_DIR = "D:\tools\Tang-Political-System"
$SCRIPT = "$REPO_DIR\scripts\run_loop.ps1"

# Check if already running
$running = Get-Process powershell -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "run_loop" }
if ($running) {
    Write-Host "run_loop.ps1 is already running (PID: $($running.Id))" -ForegroundColor Green
    exit 0
}

Write-Host "Starting run_loop.ps1 in background..." -ForegroundColor Cyan

# Start in background
Start-Process powershell -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$SCRIPT`"" -WorkingDirectory $REPO_DIR

Start-Sleep 2

# Verify
$running = Get-Process powershell -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "run_loop" }
if ($running) {
    Write-Host "Started successfully (PID: $($running.Id))" -ForegroundColor Green
} else {
    Write-Host "Failed to start" -ForegroundColor Red
}
