#Requires -Version 5.1
<#
.SYNOPSIS
    Tang Political System - Windows Installer
.DESCRIPTION
    Modular installer that delegates to step scripts in scripts/install/
#>
param(
    [switch]$DryRun,
    [switch]$Force,
    [switch]$SkipGatewayRestart
)

# Set UTF-8 encoding for output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$ErrorActionPreference = "Stop"
$REPO_DIR = $PSScriptRoot

# Load common functions
. "$REPO_DIR\scripts\utils\functions.ps1"

# Load all install steps
$installScripts = @(
    "00-check-deps.ps1"
    "10-analyze-config.ps1"
    "20-backup-config.ps1"
    "30-create-workspaces.ps1"
    "40-register-agents.ps1"
    "50-configure-main.ps1"
    "35-init-data.ps1"      # Moved after agent registration
    "60-copy-cheatsheet.ps1"
    "70-start-services.ps1"
    "99-finish.ps1"
)

foreach ($script in $installScripts) {
    $path = "$REPO_DIR\scripts\install\$script"
    if (Test-Path $path) {
        . $path
    } else {
        Err "Missing install script: $script"
        exit 1
    }
}

# Main installation flow
Banner
Check-Deps
Analyze-Config
Backup-Config
Create-Workspaces
Init-DataFiles
Register-TangAgents
Configure-MainAgent
Copy-Cheatsheet
Start-Services
Finish-Install
