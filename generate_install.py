#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate install.ps1 for Tang Political System"""

import os

SCRIPT_CONTENT = '''#Requires -Version 5.1
<#
.SYNOPSIS
    Tang Political System - Windows Installer with Smart Agent Integration
.DESCRIPTION
    Smart detection of user's OpenClaw config:
    - Single Agent: Create main agent, workspace points to user default space
    - Multi Agent: Configure first agent with zhongshu permission
#>
param(
    [switch]$DryRun,
    [switch]$Force,
    [switch]$SkipGatewayRestart
)

$ErrorActionPreference = "Stop"
$REPO_DIR = ${PSScriptRoot}
$OC_HOME = "$env:USERPROFILE\\.openclaw"
$OC_CFG = "$OC_HOME\\openclaw.json"

function Log($msg) { Write-Host "✅ $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "⚠️  $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "❌ $msg" -ForegroundColor Red }
function Info($msg) { Write-Host "ℹ️  $msg" -ForegroundColor Cyan }

function Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  🏛️  Tang Political System · Windows    ║" -ForegroundColor Cyan
    Write-Host "║       Smart Installer                     ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

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
    if (-not (Test-Path $OC_CFG)) {
        Err "openclaw.json not found. Please run 'openclaw' first"
        exit 1
    }
    Log "openclaw.json found"
}

function Analyze-Config {
    Info "Analyzing user OpenClaw configuration..."
    $cfg = Get-Content $OC_CFG -Raw | ConvertFrom-Json
    $agentsList = @($cfg.agents.list)
    $agentCount = $agentsList.Count
    Info "Detected $agentCount agent(s)"
    $tangAgentIds = @("zhongshu","menxia","shangshu","hubu","libu","bingbu","xingbu","gongbu","libu_hr","zaochao")
    $hasTangAgents = $agentsList | Where-Object { $_.id -in $tangAgentIds }
    if ($hasTangAgents) {
        Warn "Tang agents already exist, skipping main config"
        $script:SkipMainConfig = $true
        return
    }
    $script:SkipMainConfig = $false
    $script:DefaultWorkspace = $cfg.agents.defaults.workspace
    $script:AgentsList = $agentsList
    $script:FirstAgent = if ($agentCount -gt 0) { $agentsList[0] } else { $null }
    $script:FirstAgentId = if ($agentCount -gt 0) { $agentsList[0].id } else { $null }
    if ($agentCount -le 1) {
        $script:ConfigMode = "SINGLE"
        Info "Mode: Single Agent"
    } else {
        $script:ConfigMode = "MULTI"
        Info "Mode: Multi Agent (first: $script:FirstAgentId)"
    }
}

function Backup-Config {
    Info "Backing up configuration..."
    $backupFile = "$OC_CFG.bak.tang-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $OC_CFG $backupFile
    Log "Config backed up: $backupFile"
}

function Get-TangRules {
    return @"

## Tang Political System Activation Rules

You are the user's main agent and the entry point for Tang Political System.
When user messages contain the following activation words, forward to the corresponding agent.

### Emperor Exclusive (forward to zhongshu)
Activation words: `朕`, `圣旨`, `下旨`, `传旨`, `口谕`
- Example: "朕要做一个竞品分析" -> call zhongshu
- Example: "下旨：调研AI市场" -> call zhongshu

### Department Direct Call
| Activation | Agent | Purpose |
|------------|-------|---------|
| `中书省` | zhongshu | Planning, sorting |
| `门下省` | menxia | Review, audit |
| `尚书省` | shangshu | Dispatch, coordinate |
| `户部` | hubu | Data, reports |
| `礼部` | libu | Documents, standards |
| `兵部` | bingbu | Code, engineering |
| `刑部` | xingbu | Security, audit |
| `工部` | gongbu | Deployment, tools |
| `吏部` | libu_hr | HR, management |
| `早朝官` | zaochao | Reports, briefings |

### Quick Access
- `军机处`, `看板` -> reply with dashboard URL http://127.0.0.1:7891
- `奏折` -> query completed tasks
- `官员` -> query agent status
- `上朝` -> start service
- `退朝` -> stop service

### Shortcut
- `宣` + department name -> quick call (e.g., "宣兵部")

### Non-activation Messages
Messages without activation words are handled directly by you (main), not forwarded to Tang Political System.
"@
}

function Configure-MainAgent {
    if ($script:SkipMainConfig) { return }
    Info "Configuring main agent..."
    $cfg = Get-Content $OC_CFG -Raw | ConvertFrom-Json
    $rules = Get-TangRules
    
    if ($script:ConfigMode -eq "SINGLE") {
        if ($script:AgentsList.Count -eq 0) {
            Info "Creating new main agent..."
            $mainDir = "$OC_HOME\agents\main\agent"
            New-Item -ItemType Directory -Force -Path $mainDir | Out-Null
            $entry = @{
                id = "main"
                name = "main"
                workspace = $script:DefaultWorkspace
                agentDir = $mainDir
                subagents = @{ allowAgents = @("zhongshu") }
            }
            $cfg.agents.list = @($entry) + $cfg.agents.list
            $baseSoul = "# SOUL`n`nMain agent for user."
            Set-Content "$mainDir\SOUL.md" ($baseSoul + $rules) -NoNewline
            Log "Created main agent with workspace: $script:DefaultWorkspace"
        } else {
            $id = $script:FirstAgentId
            Info "Configuring existing agent: $id"
            for ($i = 0; $i -lt $cfg.agents.list.Count; $i++) {
                if ($cfg.agents.list[$i].id -eq $id) {
                    if (-not $cfg.agents.list[$i].subagents) {
                        $cfg.agents.list[$i] | Add-Member -NotePropertyName subagents -NotePropertyValue @{allowAgents=@("zhongshu")} -Force
                    } else {
                        $cfg.agents.list[$i].subagents.allowAgents = @("zhongshu")
                    }
                    break
                }
            }
            $dir = $script:FirstAgent.agentDir
            if (-not $dir) { $dir = "$OC_HOME\agents\$id\agent" }
            if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
            $soul = "$dir\SOUL.md"
            if (Test-Path $soul) {
                $c = Get-Content $soul -Raw
                if ($c -notmatch "Tang Political") {
                    Add-Content $soul $rules -NoNewline
                    Log "Updated SOUL.md for $id"
                } else {
                    Log "SOUL.md already has Tang rules"
                }
            } else {
                Set-Content $soul ("# SOUL`n`nAgent $id" + $rules) -NoNewline
                Log "Created SOUL.md for $id"
            }
        }
    } else {
        Info "Multi-agent: configuring first agent $script:FirstAgentId"
        $id = $script:FirstAgentId
        for ($i = 0; $i -lt $cfg.agents.list.Count; $i++) {
            if ($cfg.agents.list[$i].id -eq $id) {
                if (-not $cfg.agents.list[$i].subagents) {
                    $cfg.agents.list[$i] | Add-Member -NotePropertyName subagents -NotePropertyValue @{allowAgents=@("zhongshu")} -Force
                } else {
                    $existing = $cfg.agents.list[$i].subagents.allowAgents
                    if ($existing -notcontains "zhongshu") {
                        $cfg.agents.list[$i].subagents.allowAgents += "zhongshu"
                    }
                }
                break
            }
        }
        $dir = $script:FirstAgent.agentDir
        if