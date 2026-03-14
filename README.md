<h1 align="center">⚔️ 大唐政治体制 · Tang Political System</h1>

<p align="center">
  <strong>基于三省六部架构的 AI 多 Agent 协作系统 · Windows 优化版</strong>
</p>

<p align="center">
  <sub>10 个 AI Agent 组成三省六部：中书省分拣规划、门下省审核封驳、尚书省派发、六部+吏部并行执行。<br>比 CrewAI 多一层<b>制度性审核</b>，比 AutoGen 多一个<b>实时看板</b>。</sub>
</p>

<p align="center">
  <sub>本项目基于 <a href="https://github.com/cft0808/edict">cft0808/edict (三省六部)</a> 修改，专注于 Windows 兼容性优化</sub>
</p>
<p align="center">
  <a href="#-架构">🏛️ 架构</a> ·
  <a href="#-功能全景">📋 看板功能</a> ·
  <a href="docs/task-dispatch-architecture.md">📚 架构文档</a> ·
  <a href="README_EN.md">English</a> ·
  <a href="CONTRIBUTING.md">参与贡献</a>
</p>

<p align="center">
  <strong>📖 推荐优先阅读：</strong>
  <a href="docs/background-zh.md">项目背景介绍 (中文)</a> ·
  <a href="docs/background-en.md">Project Background (English)</a>
</p>


<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Required-blue?style=flat-square" alt="OpenClaw">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Agents-10_Specialized-8B5CF6?style=flat-square" alt="Agents">
  <img src="https://img.shields.io/badge/Dashboard-Real--time-F59E0B?style=flat-square" alt="Dashboard">
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Frontend-React_18-61DAFB?style=flat-square&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/Backend-stdlib_only-EC4899?style=flat-square" alt="Zero Backend Dependencies">
</p>
---

## 📖 项目背景介绍（推荐阅读）

> **首次使用本项目？建议先阅读背景文档，了解设计理念和历史渊源。**

<div align="center">

| 文档 | 语言 | 说明 |
|:---:|:---:|:---|
| [📜 项目背景介绍](docs/background-zh.md) | 中文 | 了解三省六部制的历史渊源、设计哲学与现代AI治理的关联 |
| [📜 Project Background](docs/background-en.md) | English | Learn about the historical origins of the Three Departments system and its relevance to modern AI governance |

</div>

**核心观点**：我们将中国唐代（618-907年）延续1400年的**三省六部制**政治体制，转化为现代AI多智能体协作系统的治理框架。这不是简单的文化包装，而是对**分权制衡、层层把关、流程化治理**这一古老智慧的现代化演绎。

---

## 🤔 为什么是三省六部？

大多数 Multi-Agent 框架的套路是：

> *"来，你们几个 AI 自己聊，聊完把结果给我。"*

然后你拿到一坨不知道经过了什么处理的结果，无法复现，无法审计，无法干预。

**三省六部的思路完全不同** —— 我们用了一个在中国存在 1400 年的制度架构：

```
你 (皇上) → 中书省 (分拣+规划) → 门下省 (审议) → 尚书省 (派发) → 六部 (执行) → 回奏
```

这不是花哨的 metaphor，这是**真正的分权制衡**：

| | CrewAI | MetaGPT | AutoGen | **三省六部** |
|---|:---:|:---:|:---:|:---:|
| **审核机制** | ❌ 无 | ⚠️ 可选 | ⚠️ Human-in-loop | **✅ 门下省专职审核 · 可封驳** |
| **实时看板** | ❌ | ❌ | ❌ | **✅ 军机处 Kanban + 时间线** |
| **任务干预** | ❌ | ❌ | ❌ | **✅ 叫停 / 取消 / 恢复** |
| **流转审计** | ⚠️ | ⚠️ | ❌ | **✅ 完整奏折存档** |
| **Agent 健康监控** | ❌ | ❌ | ❌ | **✅ 心跳 + 活跃度检测** |
| **热切换模型** | ❌ | ❌ | ❌ | **✅ 看板内一键切换 LLM** |
| **技能管理** | ❌ | ❌ | ❌ | **✅ 查看 / 添加 Skills** |
| **新闻聚合推送** | ❌ | ❌ | ❌ | **✅ 天下要闻 + 飞书推送** |
| **部署难度** | 中 | 高 | 中 | **低 · 一键安装 / Docker** |

> **核心差异：制度性审核 + 完全可观测 + 实时可干预**

<details>
<summary><b>🔍 为什么「门下省审核」是杀手锏？（点击展开）</b></summary>
<br>

CrewAI 和 AutoGen 的 Agent 协作模式是 **"做完就交"**——没有人检查产出质量。就像一个公司没有 QA 部门，工程师写完代码直接上线。

三省六部的 **门下省** 专门干这件事：

- 📋 **审查方案质量** —— 中书省的规划是否完备？子任务拆解是否合理？
- 🚫 **封驳不合格的产出** —— 不是 warning，是直接打回重做
- 🔄 **强制返工循环** —— 直到方案达标才放行

这不是可选的插件——**它是架构的一部分**。每一个旨意都必须经过门下省，没有例外。

这就是为什么三省六部能处理复杂任务而结果可靠：因为在送到执行层之前，有一个强制的质量关卡。1300 年前唐太宗就想明白了——**不受制约的权力必然会出错**。

</details>

---

## ✨ 功能全景

### 🏛️ 十部制 Agent 架构
- **三省**（中书·门下·尚书）负责规划、审议、派发
- **七部**（户·礼·兵·刑·工·吏 + 早朝官）负责专项执行
- 严格的权限矩阵 —— 谁能给谁发消息，白纸黑字
- 每个 Agent 独立 Workspace · 独立 Skills · 独立模型
- **旨意数据清洗** —— 标题/备注自动剥离文件路径、元数据、无效前缀

### 📋 军机处看板（10 个功能面板）

<table>
<tr><td width="50%">

**📋 旨意看板 · Kanban**
- 按状态列展示全部任务
- 省部过滤 + 全文搜索
- 心跳徽章（🟢活跃 🟡停滞 🔴告警）
- 任务详情 + 完整流转链
- 叫停 / 取消 / 恢复操作

</td><td width="50%">

**🔭 省部调度 · Monitor**
- 可视化各状态任务数量
- 部门分布横向条形图
- Agent 健康状态实时卡片

</td></tr>
<tr><td>

**📜 奏折阁 · Memorials**
- 已完成旨意自动归档为奏折
- 五阶段时间线：圣旨→中书→门下→尚书→六部→回奏
- 一键复制为 Markdown
- 按状态筛选

</td><td>

**📜 旨库 · Template Library**
- 9 个预设圣旨模板
- 分类筛选 · 参数表单 · 预估时间和费用
- 预览旨意 → 一键下旨

</td></tr>
<tr><td>

**👥 官员总览 · Officials**
- Token 消耗排行榜
- 活跃度 · 完成数 · 会话统计

</td><td>

**📰 天下要闻 · News**
- 每日自动采集科技/财经资讯
- 分类订阅管理 + 飞书推送

</td></tr>
<tr><td>

**⚙️ 模型配置 · Models**
- 每个 Agent 独立切换 LLM
- 应用后自动重启 Gateway（~5秒生效）

</td><td>

**🛠️ 技能配置 · Skills**
- 各省部已安装 Skills 一览
- 查看详情 + 添加新技能

</td></tr>
<tr><td>

**💬 小任务 · Sessions**
- OC-* 会话实时监控
- 来源渠道 · 心跳 · 消息预览

</td><td>

**🎬 上朝仪式 · Ceremony**
- 每日首次打开播放开场动画
- 今日统计 · 3.5秒自动消失

</td></tr>
</table>

---

## 🖼️ 截图

### 旨意看板
![旨意看板](docs/screenshots/01-kanban-main.png)

<details>
<summary>📸 展开查看更多截图</summary>

### 省部调度
![省部调度](docs/screenshots/02-monitor.png)

### 任务流转详情
![任务流转详情](docs/screenshots/03-task-detail.png)

### 模型配置
![模型配置](docs/screenshots/04-model-config.png)

### 技能配置
![技能配置](docs/screenshots/05-skills-config.png)

### 官员总览
![官员总览](docs/screenshots/06-official-overview.png)

### 会话记录
![会话记录](docs/screenshots/07-sessions.png)

### 奏折归档
![奏折归档](docs/screenshots/08-memorials.png)

### 圣旨模板
![圣旨模板](docs/screenshots/09-templates.png)

### 天下要闻
![天下要闻](docs/screenshots/10-morning-briefing.png)

### 上朝仪式
![上朝仪式](docs/screenshots/11-ceremony.png)

</details>

---

## 🚀 30 秒快速体验

> ### 🪟 Windows 用户注意
> 如果你遇到 **PowerShell 执行策略错误**，请使用我们提供的 `install.bat` 文件：
> ```batch
> install.bat
> ```
> 它会自动处理执行策略问题。详细说明见下方的 [Windows 安装](#-windows-安装) 章节。

### Docker 一键启动

```bash
docker run -p 7891:7891 cft0808/sansheng-demo
```
打开 http://localhost:7891 即可体验军机处看板。

<details>
<summary><b>⚠️ 遇到 <code>exec format error</code>？（点击展开）</b></summary>

如果你在 **x86/amd64** 机器（如 Ubuntu、WSL2）上看到：
```
exec /usr/local/bin/python3: exec format error
```

这是因为镜像架构不匹配。请使用 `--platform` 参数：
```bash
docker run --platform linux/amd64 -p 7891:7891 cft0808/sansheng-demo
```

或使用 docker-compose（已内置 `platform: linux/amd64`）：
```bash
docker compose up
```

</details>

---

## 🚀 快速部署

### 🤖 方式一：让龙虾帮你部署（推荐，最简单）

<div align="center">

**如果你正在使用 OpenClaw，直接把下面这句话发给你的龙虾：**

```
https://github.com/838997125/Tang-Political-System.git 帮我把这个项目下载到 D:\tools 目录下，并安装
```

**龙虾会帮你完成：**

✅ 自动克隆项目 → ✅ 检测安装依赖 → ✅ 运行安装脚本 → ✅ 配置 10 个 Agent → ✅ 启动系统

</div>

<details>
<summary><b>💡 点击查看详细说明（可选）</b></summary>

**指令格式：**
```
https://github.com/838997125/Tang-Political-System.git 帮我把这个项目下载到 <你的目录> 目录下，并安装
```

**示例：**
- Windows: `https://github.com/838997125/Tang-Political-System.git 帮我把这个项目下载到 D:\tools 目录下，并安装`
- macOS/Linux: `https://github.com/838997125/Tang-Political-System.git 帮我把这个项目下载到 ~/projects 目录下，并安装`

</details>

---

### 🔗 与现有 Agent 集成

如果你已有 OpenClaw Agent（如 `main`），可以通过**激活词**与 Tang Political System 集成：

**在 `main` 的 SOUL.md 中添加：**
```markdown
## Tang Political System 激活规则

### 皇帝专属（转发给 zhongshu）
激活词：朕、圣旨、下旨、传旨、口谕

### 部门直调（转发给对应部门）
中书省、门下省、尚书省、户部、礼部、兵部、刑部、工部、吏部、早朝官

### 功能直达
军机处/看板、奏折、上朝、退朝

### 快捷指令
宣 + 部门名
```

**配置权限：**
```json
"main": {
  "subagents": {
    "allowAgents": ["zhongshu"]
  }
}
```

**工作流程：**
```
用户消息 → main 检测激活词 → 转发给 zhongshu → 中书省规划 → 六部执行
```

**示例：**
- `"朕要做一个竞品分析"` → main → zhongshu → 三省六部流程
- `"普通消息"` → main 直接处理

---

### 🧠 智能 Agent 配置（自动检测）

`install.ps1` 脚本会**自动检测**你的 OpenClaw 配置，并智能集成 Tang Political System：

#### 单 Agent 配置

**场景：** 你的 OpenClaw 只有 0 或 1 个 agent

**脚本行为：**
1. **创建 `main` agent**（如果不存在）
2. **Workspace 指向**你的默认工作空间（`agents.defaults.workspace`）
3. **AgentDir** 指向 `$OC_HOME\agents\main\agent`
4. **配置权限：**
   ```json
   {
     "id": "main",
     "workspace": "C:\\Users\\<user>\\.openclaw\\workspace",
     "agentDir": "C:\\Users\\<user>\\.openclaw\\agents\\main\\agent",
     "subagents": {
       "allowAgents": ["zhongshu"]
     }
   }
   ```
5. **写入 SOUL.md：** 自动添加 Tang Political System 激活规则

**优势：** 保持你现有的 workspace 和配置，零迁移成本

#### 多 Agent 配置

**场景：** 你的 OpenClaw 已有多个 agents

**脚本行为：**
1. **选择第一个 agent** 作为 Tang Political System 的入口
2. **添加调用权限：**
   ```json
   {
     "subagents": {
       "allowAgents": ["zhongshu"]
     }
   }
   ```
3. **更新 SOUL.md：** 在第一个 agent 的 SOUL.md 中追加激活规则

**优势：** 不破坏现有 agents，只增强第一个 agent 的能力

#### 配置检测逻辑

```powershell
# 脚本内部逻辑
$agentsList = $cfg.agents.list
$agentCount = $agentsList.Count

if ($agentCount -le 1) {
    # 单 Agent 模式
    $ConfigMode = "SINGLE"
    # 创建或配置 main agent
} else {
    # 多 Agent 模式
    $ConfigMode = "MULTI"
    # 配置第一个 agent
}
```

#### Tang Political System 激活规则

安装完成后，你的 main/第一个 agent 会自动获得以下能力：

| 激活词 | 调用 Agent | 用途 |
|--------|-----------|------|
| `朕`、`圣旨`、`下旨`、`传旨`、`口谕` | zhongshu | 皇帝专属，转发给中书省 |
| `中书省` | zhongshu | 规划、分拣 |
| `门下省` | menxia | 审议、审核 |
| `尚书省` | shangshu | 派发、协调 |
| `户部` | hubu | 数据、报表 |
| `礼部` | libu | 文档、规范 |
| `兵部` | bingbu | 代码、工程 |
| `刑部` | xingbu | 安全、审计 |
| `工部` | gongbu | 部署、工具 |
| `吏部` | libu_hr | 人事、管理 |
| `早朝官` | zaochao | 汇报、简报 |
| `军机处`/`看板` | - | 回复看板地址 |
| `奏折` | - | 查询已完成任务 |
| `官员` | - | 查询 Agent 状态 |
| `上朝` | - | 启动服务 |
| `退朝` | - | 停止服务 |

---

### 📦 方式二：手动安装

<details>
<summary><b>🐧 Linux / macOS 安装（点击展开）</b></summary>

#### ⚠️ 重要提示

安装脚本会修改您的 OpenClaw 配置文件 `openclaw.json`，具体包括：
- ✅ 自动备份原配置到 `openclaw.json.bak.YYYYMMDD-HHMMSS`
- ✅ 添加 10 个 Agent（中书省、门下省、尚书省、六部、吏部、早朝官）
- ✅ 配置 Agent 之间的权限矩阵
- ✅ 重启 Gateway 使配置生效

**建议：安装前备份您的配置，或确保您了解这些修改。**

#### 前置条件
- [OpenClaw](https://openclaw.ai) 已安装
- Python 3.9+
- macOS / Linux

#### 安装

```bash
git clone https://github.com/838997125/Tang-Political-System.git
cd Tang-Political-System
chmod +x install.sh && ./install.sh
```

安装脚本自动完成：
- ✅ 创建全量 Agent Workspace（含中书省/门下省/尚书省/六部/吏部/早朝官）
- ✅ 写入各省部 SOUL.md（角色人格 + 工作流规则 + 数据清洗规范）
- ✅ 注册 Agent 及权限矩阵到 `openclaw.json`
- ✅ 构建 React 前端（需 Node.js 18+，如未安装则跳过）
- ✅ 初始化数据目录 + 首次数据同步
- ✅ 重启 Gateway 使配置生效

#### 启动

```bash
# 终端 1：数据刷新循环
bash scripts/run_loop.sh

# 终端 2：看板服务器
python3 dashboard/server.py

# 打开浏览器
open http://127.0.0.1:7891
```

</details>

<details>
<summary><b>🪟 Windows 安装（点击展开）</b></summary>

#### ⚠️ 重要提示

安装脚本会修改您的 OpenClaw 配置文件 `openclaw.json`，具体包括：
- ✅ 自动备份原配置到 `openclaw.json.bak.YYYYMMDD-HHMMSS`
- ✅ 添加 10 个 Agent（中书省、门下省、尚书省、六部、吏部、早朝官）
- ✅ 配置 Agent 之间的权限矩阵
- ✅ 重启 Gateway 使配置生效

**建议：安装前备份您的配置，或确保您了解这些修改。**

#### 前置条件

<details>
<summary><b>📋 点击查看详细安装指引（点击展开）</b></summary>

**1. Windows 10/11 (64位)**
- 确保系统为 64 位版本

**2. Python 3.9+**
- 下载地址: https://www.python.org/downloads/
- ⚠️ **安装时务必勾选 "Add Python to PATH"**
- 验证安装: 打开 PowerShell 运行 `python --version` 或 `py --version`

**3. OpenClaw CLI**
- 官网: https://openclaw.ai
- 安装指南: https://docs.openclaw.ai/getting-started
- 安装后运行 `openclaw` 完成初始化配置
- 验证安装: 运行 `openclaw --version`

**4. Node.js 18+** (可选)
- 如需构建前端，请安装 Node.js
- 下载地址: https://nodejs.org/

**5. PowerShell**
- Windows 10/11 自带 PowerShell 5.1+
- 也可安装 PowerShell 7: https://aka.ms/powershell

</details>

- Windows 10/11 (64位)
- [Python 3.9+](https://www.python.org/downloads/) ⚠️ 安装时勾选 "Add Python to PATH"
- [Node.js 18+](https://nodejs.org/) (可选，用于构建前端)
- [OpenClaw CLI](https://openclaw.ai) 已安装并初始化 ([安装指南](https://docs.openclaw.ai/getting-started))
- PowerShell 5.1+ 或 PowerShell 7+

#### 安装依赖

```powershell
# 安装 Python 依赖
pip install psutil
```

> **注意**：文档中的 `<PROJECT_DIR>` 表示你下载项目的目录路径，请根据实际路径替换。
> 例如：`D:\tools\Tang-Political-System` 或 `C:\Users\YourName\Projects\Tang-Political-System`

#### 运行安装脚本

> **💡 提示**：`<PROJECT_DIR>` 是你克隆项目的目录，例如 `D:\tools\Tang-Political-System` 或 `C:\Users\YourName\Projects\Tang-Political-System`

**方式一：使用 install.bat（推荐，自动处理执行策略）**

```batch
# 进入项目目录（将 <PROJECT_DIR> 替换为你的实际路径）
cd <PROJECT_DIR>

# 双击运行 install.bat，或在命令行执行
install.bat
```

**方式二：直接使用 PowerShell**

```powershell
# 进入项目目录（将 <PROJECT_DIR> 替换为你的实际路径）
cd <PROJECT_DIR>

# 执行安装脚本（需要管理员权限）
.\install.ps1

# 或使用参数
.\install.ps1 -DryRun        # 预览模式，不实际修改
.\install.ps1 -Force         # 跳过确认提示
.\install.ps1 -SkipGatewayRestart  # 不重启 Gateway
```

安装脚本自动完成：
- ✅ 创建 10 个 Agent Workspace（三省/六部/吏部/早朝官）
- ✅ 写入各省部 SOUL.md（角色人格 + 工作流规则）
- ✅ 注册 Agent 及权限矩阵到 `openclaw.json`
- ✅ 初始化数据目录
- ✅ 执行首次数据同步
- ✅ 重启 Gateway

#### 启动系统

> **💡 提示**：以下命令需要在项目目录 `<PROJECT_DIR>` 中执行

**方式一：后台启动（推荐）**

使用 `scripts\start-background.ps1` 脚本在后台启动所有服务，不占用前台窗口：

```powershell
# 进入项目目录
cd <PROJECT_DIR>

# 后台启动所有服务
.\scripts\start-background.ps1

# 查看日志
Get-Content logs\server.log -Tail 20

# 停止所有服务
.\scripts\stop-all.ps1
```

**方式二：前台启动**

如果需要在前台查看实时输出，使用 `scripts\start-windows.ps1`：

```powershell
# 进入项目目录
cd <PROJECT_DIR>

# 前台启动（按 Ctrl+C 停止）
.\scripts\start-windows.ps1
```

**方式三：分别启动**

如果需要分别控制两个服务，可以手动启动：

```powershell
# 进入项目目录
cd <PROJECT_DIR>

# 终端 1：启动数据刷新循环（保持运行）
.\scripts\run_loop.ps1

# 终端 2：启动看板服务器（保持运行）
python dashboard\server.py
```

#### 访问看板

启动成功后，打开浏览器访问：http://127.0.0.1:7891

> 如果端口 7891 被占用，可以在 `.env` 文件中修改 `DASHBOARD_PORT`

#### ⚠️ 故障排查

<details>
<summary><b>🔴 执行策略错误（点击展开）</b></summary>

如果遇到 `无法加载文件 .\install.ps1，因为在此系统上禁止运行脚本`：

**方案 1：使用 install.bat（推荐）**
```batch
install.bat
```

**方案 2：临时允许当前会话**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\install.ps1
```

**方案 3：查看当前执行策略**
```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

<details>
<summary><b>🔴 依赖未找到（点击展开）</b></summary>

**OpenClaw CLI 未找到**
```powershell
# 访问 https://openclaw.ai 安装
# 安装后运行初始化
openclaw
```

**Python 未找到**
```powershell
# 从 https://www.python.org/downloads/ 安装 Python 3.9+
# 安装时勾选 "Add Python to PATH"
```

**openclaw.json 未找到**
```powershell
# 运行 OpenClaw 初始化
openclaw
```

</details>

<details>
<summary><b>🔴 Gateway 重启失败（点击展开）</b></summary>

**可能的原因：**
1. OpenClaw Gateway 未运行
2. 权限不足（尝试以管理员身份运行）
3. 端口被占用（默认 18789）

**故障排查步骤：**

```powershell
# 1. 检查 Gateway 状态
openclaw gateway status

# 2. 手动启动 Gateway
openclaw gateway start

# 3. 查看日志文件
Get-Content $env:LOCALAPPDATA\Temp\openclaw\openclaw-*.log | Select-Object -Last 50

# 4. 检查端口占用
netstat -ano | findstr :18789
```

**如果 Gateway 启动失败：**
- 配置已保存，Gateway 启动后将自动生效
- 可以跳过 Gateway 重启，稍后手动启动：
  ```powershell
  .\install.ps1 -SkipGatewayRestart
  ```

</details>

📖 [查看完整故障排查指南](docs/windows-troubleshooting.md)

#### 卸载

如需卸载 Tang Political System：

```powershell
# 运行卸载脚本
.\uninstall.ps1

# 或使用参数
.\uninstall.ps1 -Force         # 跳过确认提示
.\uninstall.ps1 -KeepBackup    # 保留备份文件
```

卸载脚本会：
- 从 `openclaw.json` 中移除添加的 10 个 Agent
- 可选择恢复安装前的配置备份
- 删除工作空间目录
- 重启 Gateway

更多 Windows 安装细节请看 [Windows 安装指南](docs/windows-install.md)。

</details>

> 💡 **看板即开即用**：`server.py` 内嵌 `dashboard/dashboard.html`，Docker 镜像包含预构建的 React 前端

> 💡 详细教程请看 [Getting Started 指南](docs/getting-started.md)

---

## 🏛️ 架构

```
                           ┌───────────────────────────────────┐
                           │          👑 皇上（你）              │
                           │     Feishu · Telegram · Signal     │
                           └─────────────────┬─────────────────┘
                                             │ 下旨
                           ┌─────────────────▼─────────────────┐
                           │          📜 中书省 (zhongshu)       │
                           │  接旨分拣：闲聊直接回 / 旨意建任务    │
                           │       规划 → 拆解子任务              │
                           └─────────────────┬─────────────────┘
                                             │ 提交审核
                           ┌─────────────────▼─────────────────┐
                           │          🔍 门下省 (menxia)         │
                           │       审议方案 → 准奏 / 封驳 🚫      │
                           └─────────────────┬─────────────────┘
                                             │ 准奏 ✅
                           ┌─────────────────▼─────────────────┐
                           │          📮 尚书省 (shangshu)       │
                           │     派发任务 → 协调六部 → 汇总回奏    │
                           └───┬──────┬──────┬──────┬──────┬───┘
                               │      │      │      │      │
                         ┌─────▼┐ ┌───▼───┐ ┌▼─────┐ ┌───▼─┐ ┌▼─────┐
                         │💰 户部│ │📝 礼部│ │⚔️ 兵部│ │⚖️ 刑部│ │🔧 工部│
                         │ 数据  │ │ 文档  │ │ 工程  │ │ 合规  │ │ 基建  │
                         └──────┘ └──────┘ └──────┘ └─────┘ └──────┘
                                                               ┌──────┐
                                                               │📋 吏部│
                                                               │ 人事  │
                                                               └──────┘
```

### 各省部职责

| 部门 | Agent ID | 职责 | 擅长领域 |
|------|----------|------|---------|
| 📜 **中书省** | `zhongshu` | 接旨分拣、规划、拆解 | 消息分拣、需求理解、任务分解、方案设计 |
| 🔍 **门下省** | `menxia` | 审议把关、准奏派发、封驳退回 | 质量评审、风险识别、标准把控、审核后派发尚书省 |
| 📮 **尚书省** | `shangshu` | 派发、协调、汇总 | 任务调度、进度跟踪、结果整合 |
| 💰 **户部** | `hubu` | 数据、资源、核算 | 数据处理、报表生成、成本分析 |
| 📝 **礼部** | `libu` | 文档、规范、报告 | 技术文档、API 文档、规范制定 |
| ⚔️ **兵部** | `bingbu` | 代码、算法、巡检 | 功能开发、Bug 修复、代码审查 |
| ⚖️ **刑部** | `xingbu` | 安全、合规、审计 | 安全扫描、合规检查、红线管控 |
| 🔧 **工部** | `gongbu` | CI/CD、部署、工具 | Docker 配置、流水线、自动化 |
| 📋 **吏部** | `libu_hr` | 人事、Agent 管理 | Agent 注册、权限维护、培训 |
| 🌅 **早朝官** | `zaochao` | 每日早朝、新闻聚合 | 定时播报、数据汇总 |

### 权限矩阵

> 不是想发就能发 —— 真正的分权制衡

| From ↓ \ To → | 中书 | 门下 | 尚书 | 户 | 礼 | 兵 | 刑 | 工 | 吏 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **中书省** | — | ✅ | ✅ |  | | | | | |
| **门下省** | ✅ | — | ✅ |  | | | | | |
| **尚书省** | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **六部+吏部** | | | ✅ |  | | | | | |

> **权限说明：**
>
> - **中书省**：唯一调度中枢，可提交门下省审议，可直接派发尚书省执行
> - **门下省**：审议后**准奏→派发尚书省执行**，**封驳→返回中书省重规划**
> - **尚书省**：可协调六部执行，封驳时可返回门下省，完成后回传中书省
> - **六部+吏部**：仅可回传尚书省，不可跨部门直接通信

### 任务状态流转

```
皇上 → 中书分拣规划 → 门下审议 → 已派发 → 执行中 → 待审查 → ✅ 已完成
                      ↑          │                              │
                      └──── 封驳 ─┘                    阻塞 Blocked
```

---

## 📁 项目结构

```
edict/
├── agents/                     # 9 个 Agent 的人格模板
│   ├── zhongshu/SOUL.md        # 中书省 · 规划中枢
│   ├── menxia/SOUL.md          # 门下省 · 审议把关
│   ├── shangshu/SOUL.md        # 尚书省 · 调度大脑
│   ├── hubu/SOUL.md            # 户部 · 数据资源
│   ├── libu/SOUL.md            # 礼部 · 文档规范
│   ├── bingbu/SOUL.md          # 兵部 · 工程实现
│   ├── xingbu/SOUL.md          # 刑部 · 合规审计
│   ├── gongbu/SOUL.md          # 工部 · 基础设施
│   ├── libu_hr/                # 吏部 · 人事管理
│   └── zaochao/SOUL.md         # 早朝官 · 情报枢纽
├── dashboard/
│   ├── dashboard.html          # 军机处看板（单文件 · 零依赖 · ~2500 行）
│   ├── dist/                   # React 前端构建产物（Docker 镜像内包含，本地可选）
│   └── server.py               # API 服务器（Python 标准库 · 零依赖 · ~1200 行）
├── scripts/
│   ├── run_loop.sh             # 数据刷新循环（每 15 秒）
│   ├── kanban_update.py        # 看板 CLI（含旨意数据清洗 + 标题校验）
│   ├── skill_manager.py        # Skill 管理工具（远程/本地 Skills 添加、更新、移除）
│   ├── sync_from_openclaw_runtime.py
│   ├── sync_agent_config.py
│   ├── sync_officials_stats.py
│   ├── fetch_morning_news.py
│   ├── refresh_live_data.py
│   ├── apply_model_changes.py
│   └── file_lock.py            # 文件锁（防多 Agent 并发写入）
├── tests/
│   └── test_e2e_kanban.py      # 端到端测试（17 个断言）
├── data/                       # 运行时数据（gitignored）
├── docs/
│   ├── task-dispatch-architecture.md  # 📚 详细架构文档：任务分发、流转、调度的完整设计（业务+技术）
│   ├── getting-started.md             # 快速上手指南
│   ├── wechat-article.md              # 微信文章
│   └── screenshots/                   # 功能截图（11 张）
├── install.sh                  # 一键安装脚本
├── CONTRIBUTING.md             # 贡献指南
└── LICENSE                     # MIT License
```

---

## 🎯 使用方法

### 向 AI 下旨

通过 Feishu / Telegram / Signal 给中书省发消息：

```
圣旨：给我设计一个用户注册系统，要求：
1. RESTful API（FastAPI）
2. PostgreSQL 数据库
3. JWT 鉴权
4. 完整测试用例
5. 部署文档
```

**然后坐好，看戏：**

1. 📜 中书省接旨，规划子任务分配方案
2. 🔍 门下省审议，通过 / 封驳打回重规划
3. 📮 尚书省准奏，派发给兵部 + 工部 + 礼部
4. ⚔️ 各部并行执行，进度实时可见
5. 📮 尚书省汇总结果，回奏给你

全程可在**军机处看板**实时监控，随时可以**叫停、取消、恢复**。

### 使用圣旨模板

> 看板 → 📜 旨库 → 选模板 → 填参数 → 下旨

9 个预设模板：周报生成 · 代码审查 · API 设计 · 竞品分析 · 数据报告 · 博客文章 · 部署方案 · 邮件文案 · 站会摘要

### 自定义 Agent

编辑 `agents/<id>/SOUL.md` 即可修改 Agent 的人格、职责和输出规范。

### 增补 Skills（从网上连接）

**三种方式添加 Skills：**

#### 1️⃣ 看板 UI（最简单）

```
看板 → 🔧 技能配置 → ➕ 添加远程 Skill
→ 输入 Agent + Skill 名称 + GitHub URL
→ 确认 → ✅ 完成
```

#### 2️⃣ CLI 命令（最灵活）

```bash
# 从 GitHub 添加 code_review skill 到中书省
python3 scripts/skill_manager.py add-remote \
  --agent zhongshu \
  --name code_review \
  --source https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/code_review/SKILL.md \
  --description "代码审查技能"

# 一键导入官方 skills 库到指定 agents
python3 scripts/skill_manager.py import-official-hub \
  --agents zhongshu,menxia,shangshu,bingbu,xingbu

# 列出所有已添加的远程 skills
python3 scripts/skill_manager.py list-remote

# 更新某个 skill 到最新版本
python3 scripts/skill_manager.py update-remote \
  --agent zhongshu \
  --name code_review
```

#### 3️⃣ API 请求（自动化集成）

```bash
# 添加远程 skill
curl -X POST http://localhost:7891/api/add-remote-skill \
  -H "Content-Type: application/json" \
  -d '{
    "agentId": "zhongshu",
    "skillName": "code_review",
    "sourceUrl": "https://raw.githubusercontent.com/...",
    "description": "代码审查"
  }'

# 查看所有远程 skills
curl http://localhost:7891/api/remote-skills-list
```

**官方 Skills Hub：** https://github.com/openclaw-ai/skills-hub

支持的 Skills：
- `code_review` — 代码审查（Python/JS/Go）
- `api_design` — API 设计审查
- `security_audit` — 安全审计
- `data_analysis` — 数据分析
- `doc_generation` — 文档生成
- `test_framework` — 测试框架设计

详见 [🎓 远程 Skills 资源管理指南](docs/remote-skills-guide.md)

---

## 🔧 技术亮点

| 特点 | 说明 |
|------|------|
| **React 18 前端** | TypeScript + Vite + Zustand 状态管理，13 个功能组件 |
| **纯 stdlib 后端** | `server.py` 基于 `http.server`，零依赖，同时提供 API + 静态文件服务 |
| **Agent 思考可视** | 实时展示 Agent 的 thinking 过程、工具调用、返回结果 |
| **一键安装** | `install.sh` 自动完成全部配置 |
| **15 秒同步** | 数据自动刷新，看板倒计时显示 |
| **每日仪式** | 首次打开播放上朝开场动画 |
| **远程 Skills 生态** | 从 GitHub/URL 一键导入能力，支持版本管理 + CLI + API + UI |

---

## � 深入了解

### 核心文档

- **[📖 任务分发流转完整架构](docs/task-dispatch-architecture.md)** — **必读文档**
  - 详细讲解三省六部如何处理复杂任务的业务设计和技术实现
  - 涵盖：9大任务状态机 / 权限矩阵 / 4阶段调度（重试→升级→回滚）/ Session JSONL数据融合
  - 包含完整的使用案例、API端点说明、CLI工具文档
  - 对标 CrewAI/AutoGen：为什么制度化>自由协作
  - 故障场景与恢复机制
  - **读这个文档会理解为什么三省六部这么强大**（9500+ 字，30 分钟完整理解）

- **[🎓 远程 Skills 资源管理指南](docs/remote-skills-guide.md)** — Skills 生态
  - 从网上连接和增补 skills，支持 GitHub/Gitee/任意 HTTPS URL
  - 官方 Skills Hub 预设能力库
  - CLI 工具 + 看板 UI + Restful API
  - Skills 文件规范与安全防护
  - 支持版本管理和一键更新

- **[⚡ Remote Skills 快速入门](docs/remote-skills-quickstart.md)** — 5 分钟上手
  - 快速体验、CLI 命令、看板操作示例
  - 创建自己的 Skills 库
  - API 完整参考 + 常见问题

- **[🚀 快速上手指南](docs/getting-started.md)** — 新手入门
- **[🤝 贡献指南](CONTRIBUTING.md)** — 想参与贡献？从这里开始

---
## 🔧 常见问题排查

<details>
<summary><b>❌ 任务总超时 / 下属完成了但无法传回中书省</b></summary>

**症状**：六部或尚书省已完成任务，但中书省收不到回报，最终超时。

**排查步骤**：

1. **检查 Agent 注册状态**：
```bash
curl -s http://127.0.0.1:7891/api/agents-status | python3 -m json.tool
```
确认 `zhongshu` agent 的 `statusLabel` 是 `alive`。

2. **检查 Gateway 日志**：
```bash
ls /tmp/openclaw/ | tail -5          # 找到最新日志
grep -i "error\|fail\|unknown" /tmp/openclaw/openclaw-*.log | tail -20
```

3. **常见原因**：
   - Agent ID 不匹配（已在 v1.2 修复：`main` → `zhongshu`）
   - LLM provider 超时（增加了自动重试）
   - 僵尸 Agent 进程（运行 `ps aux | grep openclaw` 检查）

4. **强制重试**：
```bash
# 手动触发巡检扫描（自动重试卡住的任务）
curl -X POST http://127.0.0.1:7891/api/scheduler-scan \
  -H 'Content-Type: application/json' -d '{"thresholdSec":60}'
```

</details>

<details>
<summary><b>❌ Docker: exec format error</b></summary>

**症状**：`exec /usr/local/bin/python3: exec format error`

**原因**：镜像架构（arm64）与主机架构（amd64）不匹配。

**解决**：
```bash
# 方法 1：指定平台
docker run --platform linux/amd64 -p 7891:7891 cft0808/sansheng-demo

# 方法 2：使用 docker-compose（已内置 platform）
docker compose up
```

</details>

<details>
<summary><b>❌ Skill 下载失败</b></summary>

**症状**：`python3 scripts/skill_manager.py import-official-hub` 报错。

**排查**：
```bash
# 测试网络连通性
curl -I https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/code_review/SKILL.md

# 如果超时，使用代理
export https_proxy=http://your-proxy:port
python3 scripts/skill_manager.py import-official-hub --agents zhongshu
```

**常见原因**：
- 中国大陆访问 GitHub raw 资源需要代理
- 网络超时（已增加到 30 秒 + 自动重试 3 次）
- 官方 Skills Hub 仓库维护中

</details>

---
## �🗺️ Roadmap

> 完整路线图及参与方式：[ROADMAP.md](ROADMAP.md)

### Phase 1 — 核心架构 ✅
- [x] 十部制 Agent 架构（中书省/门下省/尚书省 + 六部 + 吏部 + 早朝官）+ 权限矩阵
- [x] 军机处实时看板（10 个功能面板 + 实时活动面板）
- [x] 任务叫停 / 取消 / 恢复
- [x] 奏折系统（自动归档 + 五阶段时间线）
- [x] 圣旨模板库（9 个预设 + 参数表单）
- [x] 上朝仪式感动画
- [x] 天下要闻 + 飞书推送 + 订阅管理
- [x] 模型热切换 + 技能管理 + 技能添加
- [x] 官员总览 + Token 消耗统计
- [x] 小任务 / 会话监控
- [x] 中书省消息分拣（闲聊自动回复 / 旨意建任务）
- [x] 旨意数据清洗（路径/元数据/前缀自动剥离）
- [x] 重复任务防护 + 已完成任务保护
- [x] 端到端测试覆盖（17 个断言）
- [x] React 18 前端重构（TypeScript + Vite + Zustand · 13 组件）
- [x] Agent 思考过程可视化（实时 thinking / 工具调用 / 返回结果）
- [x] 前后端一体化部署（server.py 同时提供 API + 静态文件服务）

### Phase 2 — 制度深化 🚧
- [ ] 御批模式（人工审批 + 一键准奏/封驳）
- [ ] 功过簿（Agent 绩效评分体系）
- [ ] 急递铺（Agent 间实时消息流可视化）
- [ ] 国史馆（知识库检索 + 引用溯源）

### Phase 3 — 生态扩展
- [ ] Docker Compose + Demo 镜像
- [ ] Notion / Linear 适配器
- [ ] 年度大考（Agent 年度绩效报告）
- [ ] 移动端适配 + PWA
- [ ] ClawHub 上架

---

## 📂 案例

`examples/` 目录收录了真实的端到端使用案例：

| 案例 | 旨意 | 涉及部门 |
|------|------|----------|
| [竞品分析](examples/competitive-analysis.md) | "分析 CrewAI vs AutoGen vs LangGraph" | 中书→门下→户部+兵部+礼部 |
| [代码审查](examples/code-review.md) | "审查这段 FastAPI 代码的安全性" | 中书→门下→兵部+刑部 |
| [周报生成](examples/weekly-report.md) | "生成本周工程团队周报" | 中书→门下→户部+礼部 |

每个案例包含：完整旨意 → 中书省规划 → 门下省审核意见 → 各部执行结果 → 最终奏折。

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [📖 任务分发流转架构](docs/task-dispatch-architecture.md) | 详细架构设计：状态机、权限矩阵、调度系统 |
| [🏗️ 架构重设计](docs/architecture.md) | Agent 架构重设计文档（事件驱动、可观测性） |
| [🗺️ 路线图](docs/ROADMAP.md) | 项目路线图和贡献指南 |
| [🤝 贡献指南](docs/CONTRIBUTING.md) | 如何参与贡献 |
| [🎓 远程 Skills 指南](docs/remote-skills-guide.md) | Skills 生态和使用 |
| [⚡ Remote Skills 快速入门](docs/remote-skills-quickstart.md) | 5 分钟上手 Skills |
| [🪟 Windows 安装指南](docs/windows-install.md) | Windows 系统安装说明 |
| [🪟 Windows 移植文档](docs/windows-port.md) | Windows 移植技术方案 |
| [📝 权限更新记录](docs/permission-update-2026-03-12.md) | Agent 权限矩阵优化记录 |

---

## 📜 项目来源

**Tang Political System (大唐政治体制)** 是基于 [cft0808/edict (三省六部)](https://github.com/cft0808/edict) 的衍生项目，专注于 Windows 系统兼容性优化和权限矩阵改进。

### 主要修改
- ✅ Windows 系统兼容性修复（文件锁、进程检测、安装脚本）
- ✅ Agent 权限矩阵优化（收紧门下省权限，强化中书省调度中枢地位）
- ✅ 移除太子角色，简化架构为 10 个 Agent
- ✅ 文档整理和合并

### 本项目
- **GitHub**: https://github.com/838997125/Tang-Political-System
- **作者**: 838997125
- **许可证**: MIT

### 原始项目
- **GitHub**: https://github.com/cft0808/edict
- **作者**: cft0808
- **许可证**: MIT

> 💡 **Linux / macOS 用户**: 建议直接使用原始项目 [cft0808/edict](https://github.com/cft0808/edict) 以获得完整体验。

---

## 📄 License

[MIT](LICENSE) · 本项目: [838997125/Tang-Political-System](https://github.com/838997125/Tang-Political-System) · 基于 [cft0808/edict](https://github.com/cft0808/edict) 修改

---

<p align="center">
  <strong>⚔️ 以古制御新技，以智慧驾驭 AI</strong><br>
  <sub>Governing AI with the wisdom of ancient empires</sub><br><br>
</p>

