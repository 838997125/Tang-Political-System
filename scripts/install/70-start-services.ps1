# Step 70: Start Services in Background

function Start-Services {
    Info "Starting Tang Political System services..."
    
    # Check if services are already running
    $serverRunning = $false
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:7891/api/live-status" -Method GET -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $serverRunning = $true
            Info "Dashboard server already running"
        }
    } catch {
        # Server not running
    }
    
    if ($serverRunning) {
        Log "Services already running"
        return
    }
    
    # Start data refresh loop in background (hidden window)
    Info "Starting data refresh loop..."
    $refreshScript = "$REPO_DIR\scripts\run_loop.ps1"
    if (Test-Path $refreshScript) {
        # Use -WindowStyle Hidden to run in background without showing window
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "powershell.exe"
        $psi.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$refreshScript`""
        $psi.WorkingDirectory = $REPO_DIR
        $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        $psi.CreateNoWindow = $true
        [System.Diagnostics.Process]::Start($psi) | Out-Null
        Log "Data refresh loop started (background)"
    } else {
        Warn "run_loop.ps1 not found, skipping"
    }
    
    # Start dashboard server in background
    Info "Starting dashboard server..."
    $serverScript = "$REPO_DIR\dashboard\server.py"
    if (Test-Path $serverScript) {
        # Use py launcher instead of python
        $pythonCmd = if (Get-Command "py" -ErrorAction SilentlyContinue) { "py" } else { "python" }
        Start-Process $pythonCmd -ArgumentList "$serverScript" -WorkingDirectory $REPO_DIR -WindowStyle Hidden
        Log "Dashboard server started"
    } else {
        Warn "server.py not found, skipping"
    }
    
    # Wait a moment for services to start
    Start-Sleep -Seconds 3
    
    # Verify services started
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:7891/api/live-status" -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Log "Services started successfully"
        } else {
            Warn "Services may not have started properly"
        }
    } catch {
        Warn "Could not verify services status, please check manually"
    }
}
