# Start Tang Political System Dashboard Server
$ErrorActionPreference = "Continue"

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$REPO_DIR = "D:\tools\Tang-Political-System"
$SERVER_SCRIPT = "$REPO_DIR\dashboard\server.py"

Write-Host "Starting Tang Political System Dashboard Server..." -ForegroundColor Cyan
Write-Host "Server will run at http://127.0.0.1:7891" -ForegroundColor Green
Write-Host ""

# Start server in foreground
py $SERVER_SCRIPT
