# Step 0: Check Dependencies

function Check-Deps {
    Info "Checking dependencies..."
    
    if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) {
        Err "openclaw CLI not found. Please install OpenClaw"
        exit 1
    }
    Log "OpenClaw CLI found"
    
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Err "python not found. Please install Python 3.9+"
        exit 1
    }
    Log "Python found"
    
    if (-not (Test-Path $script:OC_CFG)) {
        Err "openclaw.json not found. Please run 'openclaw' first"
        exit 1
    }
    Log "openclaw.json found"
}
