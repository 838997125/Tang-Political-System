# Edict Windows Stop All Services
# Usage: .\stop-all.ps1
# 一键停止所有 Edict 相关服务（前台和后台）

# 获取脚本所在目录
$REPO_DIR = $PSScriptRoot
if ([string]::IsNullOrEmpty($REPO_DIR)) {
    $REPO_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
}
if ([string]::IsNullOrEmpty($REPO_DIR)) {
    $REPO_DIR = Get-Location
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host "  Stopping All Edict Services" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Yellow
Write-Host ""

$stoppedCount = 0

# 1. 停止后台服务（通过 PID 文件）
$pidsFile = Join-Path $REPO_DIR ".running_pids"
if (-not [string]::IsNullOrEmpty($pidsFile)) {
    if (Test-Path $pidsFile) {
        Write-Host "Found background services PID file..." -ForegroundColor Cyan
        $pids = Get-Content -Path $pidsFile
        $pidList = $pids -split ","
        
        foreach ($pid in $pidList) {
            if ($pid -match '^\d+$') {
                try {
                    $process = Get-Process -Id $pid -ErrorAction Stop
                    Stop-Process -Id $pid -Force
                    Write-Host "  ✓ Stopped background process: $pid ($($process.ProcessName))" -ForegroundColor Green
                    $stoppedCount++
                } catch {
                    Write-Host "  - Process $pid not found or already stopped" -ForegroundColor Gray
                }
            }
        }
        
        Remove-Item -Path $pidsFile -Force
        Write-Host "  ✓ Removed PID file" -ForegroundColor Gray
    }
}

# 2. 查找并停止 Python 进程（server.py）
Write-Host ""
Write-Host "Searching for Python server processes..." -ForegroundColor Cyan
$pythonProcesses = Get-Process | Where-Object { $_.ProcessName -like "*python*" }
foreach ($proc in $pythonProcesses) {
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId=$($proc.Id)").CommandLine
        if ($cmdLine -like "*dashboard\server.py*") {
            Stop-Process -Id $proc.Id -Force
            Write-Host "  ✓ Stopped Python server: $($proc.Id)" -ForegroundColor Green
            $stoppedCount++
        }
    } catch {}
}

# 3. 查找并停止 PowerShell 进程（run_loop.ps1）
Write-Host ""
Write-Host "Searching for PowerShell loop processes..." -ForegroundColor Cyan
$psProcesses = Get-Process | Where-Object { $_.ProcessName -eq "powershell" }
foreach ($proc in $psProcesses) {
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId=$($proc.Id)").CommandLine
        if ($cmdLine -like "*run_loop.ps1*") {
            Stop-Process -Id $proc.Id -Force
            Write-Host "  ✓ Stopped PowerShell loop: $($proc.Id)" -ForegroundColor Green
            $stoppedCount++
        }
    } catch {}
}

# 4. 清理日志锁文件
$lockFile = Join-Path $REPO_DIR "data\tasks_source.json.lock"
if (-not [string]::IsNullOrEmpty($lockFile)) {
    if (Test-Path $lockFile) {
        Remove-Item -Path $lockFile -Force -ErrorAction SilentlyContinue
        Write-Host ""
        Write-Host "  ✓ Cleaned up lock file" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
if ($stoppedCount -gt 0) {
    Write-Host "  Stopped $stoppedCount service(s)!" -ForegroundColor Green
} else {
    Write-Host "  No running services found" -ForegroundColor Yellow
}
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# 显示状态
Write-Host "Service Status:" -ForegroundColor White
$remainingPython = Get-Process | Where-Object { $_.ProcessName -like "*python*" } | Where-Object { (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine -like "*dashboard\server.py*" }
$remainingPS = Get-Process | Where-Object { $_.ProcessName -eq "powershell" } | Where-Object { (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine -like "*run_loop.ps1*" }

if ($remainingPython -or $remainingPS) {
    Write-Host "  ⚠ Some processes may still be running" -ForegroundColor Yellow
    Write-Host "  Run this script again or restart your computer" -ForegroundColor Gray
} else {
    Write-Host "  [OK] All services stopped successfully" -ForegroundColor Green
}
Write-Host ""
