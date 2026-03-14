# Edict Windows Uninstall Script
# Usage: .\uninstall.ps1 [-Force] [-KeepWorkspaces]

param(
    [switch]$Force,
    [switch]$KeepWorkspaces
)

$ErrorActionPreference = "Stop"

$REPO_DIR = $PSScriptRoot
if (-not $REPO_DIR) { $REPO_DIR = Get-Location }
$OC_HOME = Join-Path $env:USERPROFILE ".openclaw"
$OC_CFG = Join-Path $OC_HOME "openclaw.json"

# Agent list to remove
$AGENT_IDS = @('zhongshu', 'menxia', 'shangshu', 'hubu', 'libu', 'bingbu', 'xingbu', 'gongbu', 'libu_hr', 'zaochao')

function Banner {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Yellow
    Write-Host "  Edict - OpenClaw Multi-Agent System" -ForegroundColor Yellow
    Write-Host "  Windows Uninstaller" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Yellow
    Write-Host ""
}

function Log($msg) { Write-Host "[OK] $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "[ERR] $msg" -ForegroundColor Red; exit 1 }
function Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }

# Show uninstallation summary
function ShowUninstallSummary {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Yellow
    Write-Host "  卸载配置摘要" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "将从 openclaw.json 移除的 Agent:" -ForegroundColor White
    foreach ($agentId in $AGENT_IDS) {
        Write-Host "  - $agentId" -ForegroundColor Gray
    }
    Write-Host ""
    if (-not $KeepWorkspaces) {
        Write-Host "将删除的目录:" -ForegroundColor White
        Write-Host "  - $REPO_DIR\workspaces" -ForegroundColor Gray
        Write-Host "  - $REPO_DIR\data" -ForegroundColor Gray
    } else {
        Write-Host "将保留工作空间 (使用 -KeepWorkspaces)" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Pre-uninstallation confirmation
function ConfirmUninstallation {
    if ($Force) { return $true }
    
    Write-Host ""
    Write-Host "⚠️  警告：此操作将从 openclaw.json 中移除 Tang Political System 的 Agent 配置！" -ForegroundColor Yellow
    Write-Host "    此操作不可撤销，但会自动创建配置备份。" -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "是否继续卸载? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "卸载已取消" -ForegroundColor Yellow
        exit 0
    }
    return $true
}

# Remove Agents from config
function RemoveAgents {
    Info "Removing Agents from openclaw.json..."

    if (-not (Test-Path $OC_CFG)) {
        Warn "openclaw.json not found at $OC_CFG"
        return
    }

    $cfgBackup = "$OC_CFG.bak.uninstall.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -Path $OC_CFG -Destination $cfgBackup -Force
    Log "Config backed up to: $cfgBackup"

    $pythonCode = @'
import json, pathlib, sys

cfg_path = pathlib.Path.home() / '.openclaw' / 'openclaw.json'

AGENT_IDS = ["zhongshu", "menxia", "shangshu", "hubu", "libu", "bingbu", "xingbu", "gongbu", "libu_hr", "zaochao"]

try:
    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
except Exception as e:
    print(f'Error reading config: {e}')
    sys.exit(1)

agents_cfg = cfg.get('agents', {})
agents_list = agents_cfg.get('list', [])

original_count = len(agents_list)
filtered_list = [a for a in agents_list if a.get('id') not in AGENT_IDS]
removed_count = original_count - len(filtered_list)

agents_cfg['list'] = filtered_list
cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Removed {removed_count} agents from config')
'@

    $pythonCmd = if (Get-Command "py" -ErrorAction SilentlyContinue) { "py" } 
                  elseif (Get-Command "python" -ErrorAction SilentlyContinue) { "python" } 
                  else { "python3" }
    & $pythonCmd -c $pythonCode

    Log "Agents removed from config"
}

# Clean up data and workspaces
function CleanupFiles {
    if ($KeepWorkspaces) {
        Info "Skipping workspace cleanup (as requested)"
    } else {
        Info "Cleaning up workspaces and data..."

        $WORKSPACES_DIR = Join-Path $REPO_DIR "workspaces"
        $DATA_DIR = Join-Path $REPO_DIR "data"

        if (Test-Path $WORKSPACES_DIR) {
            Remove-Item -Path $WORKSPACES_DIR -Recurse -Force
            Log "Removed workspaces directory"
        }

        if (Test-Path $DATA_DIR) {
            Remove-Item -Path $DATA_DIR -Recurse -Force
            Log "Removed data directory"
        }
    }

    # Remove .env file
    $ENV_FILE = Join-Path $REPO_DIR ".env"
    if (Test-Path $ENV_FILE) {
        Remove-Item -Path $ENV_FILE -Force
        Log "Removed .env file"
    }
}

# Restart Gateway
function RestartGateway {
    Info "Restarting OpenClaw Gateway..."
    try {
        openclaw gateway restart 2>$null
        if ($LASTEXITCODE -eq 0) {
            Log "Gateway restarted"
        } else {
            Warn "Gateway restart failed, please restart manually with: openclaw gateway restart"
        }
    } catch {
        Warn "Gateway restart failed, please restart manually with: openclaw gateway restart"
    }
}

# Show uninstallation summary
function ShowSummary {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  Uninstallation Complete!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "已移除的 Agent:" -ForegroundColor White
    foreach ($agentId in $AGENT_IDS) {
        Write-Host "  ✓ $agentId" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "配置备份保存在:" -ForegroundColor White
    Write-Host "  $OC_CFG.bak.uninstall.*" -ForegroundColor Gray
    Write-Host ""
    Write-Host "如需恢复，可手动复制备份文件覆盖 openclaw.json" -ForegroundColor Cyan
    Write-Host ""
}

# Main
Banner
ShowUninstallSummary
ConfirmUninstallation
RemoveAgents
CleanupFiles
RestartGateway
ShowSummary
