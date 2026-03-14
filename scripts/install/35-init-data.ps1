# Step 35: Initialize Data Files

function Init-DataFiles {
    Info "Initializing data files..."
    
    $DATA_DIR = "$REPO_DIR\data"
    New-Item -ItemType Directory -Force -Path $DATA_DIR | Out-Null
    
    # Create empty tasks.json if not exists
    if (-not (Test-Path "$DATA_DIR\tasks.json")) {
        "[]" | Set-Content "$DATA_DIR\tasks.json" -Encoding UTF8
        Log "Created tasks.json"
    }
    
    # Create empty tasks_source.json if not exists
    if (-not (Test-Path "$DATA_DIR\tasks_source.json")) {
        "[]" | Set-Content "$DATA_DIR\tasks_source.json" -Encoding UTF8
        Log "Created tasks_source.json"
    }
    
    # Run sync scripts to generate actual data
    Info "Running sync scripts to generate data..."
    
    $scripts = @(
        @{ name = "sync_agent_config.py"; desc = "agent config" },
        @{ name = "sync_from_openclaw_runtime.py"; desc = "runtime data" },
        @{ name = "sync_officials_stats.py"; desc = "officials stats" }
    )
    
    foreach ($script in $scripts) {
        $scriptPath = "$REPO_DIR\scripts\$($script.name)"
        if (Test-Path $scriptPath) {
            Info "Running $($script.desc)..."
            try {
                # Set UTF-8 encoding for Python subprocess
                $env:PYTHONIOENCODING = "utf-8"
                $output = py $scriptPath 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Log "$($script.desc) synced"
                } else {
                    Warn "Failed to sync $($script.desc) (exit code: $LASTEXITCODE)"
                    if ($output) {
                        Warn "Output: $output"
                    }
                }
            } catch {
                Warn "Failed to run $($script.name): $_"
            }
        } else {
            Warn "Script not found: $($script.name)"
        }
    }
    
    # Create initial live_status.json if not exists (will be updated by refresh_live_data.py)
    if (-not (Test-Path "$DATA_DIR\live_status.json")) {
        $liveStatus = @{
            generatedAt = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            taskSource = "tasks.json"
            officials = @()
            tasks = @()
            history = @()
            metrics = @{
                officialCount = 0
                todayDone = 0
                totalDone = 0
                inProgress = 0
                blocked = 0
            }
            syncStatus = @{
                ok = $true
                lastSyncAt = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                durationMs = 0
                source = "initial"
                recordCount = 0
                scannedSessionFiles = 0
                missingFields = @{}
                error = $null
            }
            health = @{
                syncOk = $true
                syncLatencyMs = $null
                missingFieldCount = 0
            }
        } | ConvertTo-Json -Depth 5
        $liveStatus | Set-Content "$DATA_DIR\live_status.json" -Encoding UTF8
        Log "Created live_status.json"
    }
    
    Log "Data files initialized"
}
