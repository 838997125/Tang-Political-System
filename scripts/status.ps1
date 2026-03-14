#!/usr/bin/env pwsh
# Tang Political System - Status Check

$ErrorActionPreference = "Continue"

$DASHBOARD_URL = "http://127.0.0.1:7891"

Write-Host "=========================================="
Write-Host "  Tang Political System Status"
Write-Host "=========================================="
Write-Host ""

# Use python to check status
try {
    $output = py -c "import urllib.request, json; r=urllib.request.urlopen('$DASHBOARD_URL/api/live-status'); d=json.load(r); print('OK', len(d.get('officials',0)))" 2>&1
    if ($output -match "OK (\d+)") {
        $agentCount = $matches[1]
        Write-Host "[OK] Project is running"
        Write-Host ""
        Write-Host "Dashboard: $DASHBOARD_URL"
        Write-Host "Agents: $agentCount"
    } else {
        throw "Invalid response"
    }
} catch {
    Write-Host "[STOPPED] Project is not running"
    Write-Host ""
    Write-Host "Use 'shang-chao' to start"
}
