# Tang Political System - Common Functions

$script:OC_HOME = "$env:USERPROFILE\.openclaw"
$script:OC_CFG = "$script:OC_HOME\openclaw.json"

function Log($msg) { Write-Host "[OK] $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "[ERR] $msg" -ForegroundColor Red }
function Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }

function Banner {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  Tang Political System Installer" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Get-TangRules {
    return @"

## Tang Political System Activation Rules

You are the user's main agent and the entry point for Tang Political System.

### Emperor Exclusive (forward to zhongshu)
Activation words: zhen(朕), sheng-zhi(圣旨), xia-zhi(下旨), chuan-zhi(传旨), kou-yu(口谕)
- Example: 'zhen yao zuo yi ge jing pin fen xi' -> call zhongshu
- Example: 'xia zhi: diao yan AI shi chang' -> call zhongshu

### Department Direct Call
| Activation | Agent | Purpose |
|------------|-------|---------|
| zhong-shu-sheng(中书省) | zhongshu | Planning, sorting |
| men-xia-sheng(门下省) | menxia | Review, audit |
| shang-shu-sheng(尚书省) | shangshu | Dispatch, coordinate |
| hu-bu(户部) | hubu | Data, reports |
| li-bu(礼部) | libu | Documents, standards |
| bing-bu(兵部) | bingbu | Code, engineering |
| xing-bu(刑部) | xingbu | Security, audit |
| gong-bu(工部) | gongbu | Deployment, tools |
| li-bu-hr(吏部) | libu_hr | HR, management |
| zao-chao-guan(早朝官) | zaochao | Reports, briefings |

### Quick Access
- kanban(看板) -> reply with dashboard URL http://127.0.0.1:7891
- zou-zhe(奏折) -> query completed tasks
- guan-yuan(官员) -> query agent status
- shang-chao(上朝) -> start service
- tui-chao(退朝) -> stop service

### Shortcut
- xuan + department name -> quick call (e.g., 'xuan bingbu')

### Non-activation Messages
Messages without activation words are handled directly by you (main), not forwarded to Tang Political System.

### Help Command
When user types 'help', reply with activation rules summary.

### Welcome Message (First Time)
Display welcome message with quick start guide on first conversation.
"@
}
