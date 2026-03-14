# Start Tang Political System Dashboard
$ErrorActionPreference = "Continue"

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$REPO_DIR = "D:\tools\Tang-Political-System"

Write-Host "Starting Tang Political System Dashboard..." -ForegroundColor Cyan
Write-Host "This will run in the foreground. Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

# Change to project directory
Set-Location $REPO_DIR

# Start server
py dashboard\server.py
