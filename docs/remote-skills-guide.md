# 远程 Skills 资源管理指南

## 概述

三省六部现已支持从网上连接和增补 skills 资源，无需手动复制文件。支持从以下来源获取：

- **GitHub 仓库** (raw.githubusercontent.com)
- **任何 HTTPS URL** (需返回有效的 skill 文件)
- **本地文件路径**
- **内置仓库** (官方 skills 库)

---

## 功能架构

### 1. API 端点

#### `POST /api/add-remote-skill`

从远程 URL 或本地路径为指定 Agent 添加 skill。

**请求体：**
```json
{
  "agentId": "zhongshu",
  "skillName": "code_review",
  "sourceUrl": "https://raw.githubusercontent.com/org/skills-repo/main/code_review/SKILL.md",
  "description": "代码审查专项技能"
}
```

**参数说明：**
- `agentId` (string, 必需): 目标 Agent ID (验证有效性)
- `skillName` (string, 必需): skill 的内部名称 (仅允许字母/数字/下划线/汉字)
- `sourceUrl` (string, 必需): 远程 URL 或本地文件路径
  - GitHub: `https://raw.githubusercontent.com/user/repo/branch/path/SKILL.md`
  - 任意 HTTPS: `https://example.com/skills/my_skill.md`
  - 本地: `file:///Users/bingsen/skills/code_review.md` 或 `/Users/bingsen/skills/code_review.md`
- `description` (string, 可选): skill 的中文描述

**响应成功 (200)：**
```json
{
  "ok": true,
  "message": "技能 code_review 已添加到 zhongshu",
  "skillName": "code_review",
  "agentId": "zhongshu",
  "source": "https://raw.githubusercontent.com/...",
  "localPath": "/Users/bingsen/.openclaw/workspace-zhongshu/skills/code_review/SKILL.md",
  "size": 2048,
  "addedAt": "2026-03-02T14:30:00Z"
}
```

**响应失败 (400)：**
```json
{
  "ok": false,
  "error": "URL 无效或无法访问",
  "details": "Connection timeout after 10s"
}
```

#### `GET /api/remote-skills-list`

列出所有已添加的远程 skills 及其源信息。

**响应：**
```json
{
  "ok": true,
  "remoteSkills": [
    {
      "skillName": "code_review",
      "agentId": "zhongshu",
      "sourceUrl": "https://raw.githubusercontent.com/org/skills-repo/main/code_review/SKILL.md",
      "description": "代码审查专项技能",
      "localPath": "/Users/bingsen/.openclaw/workspace-zhongshu/skills/code_review/SKILL.md",
      "lastUpdated": "2026-03-02T14:30:00Z",
      "status": "valid"  // valid | invalid | not-found
    }
  ],
  "count": 5
}
```

#### `POST /api/update-remote-skill`

更新已添加的远程 skill 为最新版本。

**请求体：**
```json
{
  "agentId": "zhongshu",
  "skillName": "code_review"
}
```

**响应：**
```json
{
  "ok": true,
  "message": "技能已更新",
  "skillName": "code_review",
  "newVersion": "2.1.0",
  "updatedAt": "2026-03-02T15:00:00Z"
}
```

#### `DELETE /api/remove-remote-skill`

移除已添加的远程 skill。

**请求体：**
```json
{
  "agentId": "zhongshu",
  "skillName": "code_review"
}
```

---

## CLI 命令

### 添加远程 Skill

```bash
python3 scripts/skill_manager.py add-remote \
  --agent zhongshu \
  --name code_review \
  --source https://raw.githubusercontent.com/org/skills-repo/main/code_review/SKILL.md \
  --description "代码审查专项技能"
```

### 列出远程 Skills

```bash
python3 scripts/skill_manager.py list-remote
```

### 更新远程 Skill

```bash
python3 scripts/skill_manager.py update-remote \
  --agent zhongshu \
  --name code_review
```

### 移除远程 Skill

```bash
python3 scripts/skill_manager.py remove-remote \
  --agent zhongshu \
  --name code_review
```

---

## 官方 Skills 库

### OpenClaw Skills Hub

> **官方 skills 库地址**: https://github.com/openclaw-ai/skills-hub

可用 skills 列表：

| Skill 名称 | 描述 | 适用 Agent | 源 URL |
|-----------|------|----------|--------|
| `code_review` | 代码审查（支持 Python/JS/Go） | 兵部/刑部 | https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/code_review/SKILL.md |
| `api_design` | API 设计审查 | 兵部/工部 | https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/api_design/SKILL.md |
| `security_audit` | 安全审计 | 刑部 | https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/security_audit/SKILL.md |
| `data_analysis` | 数据分析 | 户部 | https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/data_analysis/SKILL.md |
| `doc_generation` | 文档生成 | 礼部 | https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/doc_generation/SKILL.md |
| `test_framework` | 测试框架设计 | 工部/刑部 | https://raw.githubusercontent.com/openclaw-ai/skills-hub/main/test_framework/SKILL.md |

**一键导入官方 skills**

```bash
python3 scripts/skill_manager.py import-official-hub \
  --agents zhongshu,menxia,shangshu,bingbu,xingbu,libu
```

---

## 看板 UI 操作

### 快捷添加 Skill

1. 打开看板 → 🔧 **技能配置** 面板
2. 点击 **➕ 添加远程 Skill** 按钮
3. 填写表单：
   - **Agent**: 选择目标 Agent
   - **Skill 名称**: 输入 skill 的内部 ID
   - **远程 URL**: 粘贴 GitHub/HTTPS URL
   - **中文描述**: 可选，简述 skill 功能
4. 点击 **确认** 按钮

### 管理已添加的 Skills

1. 看板 → 🔧 **技能配置** → **远程 Skills** 标签
2. 查看已添加的所有 skills 及其源地址
3. 操作：
   - **查看**: 展示 SKILL.md 内容
   - **更新**: 从源 URL 重新下载最新版本
   - **删除**: 移除本地副本（不影响源）
   - **复制源 URL**: 快速分享给他人

---

## Skill 文件规范

远程 skills 必须遵循标准的 Markdown 格式：

### 最小必需结构

```markdown
---
name: skill_internal_name
description: Short description
version: 1.0.0
tags: [tag1, tag2]
---

# Skill 名称

详细描述...

## 输入

说明接收什么参数

## 处理流程

具体步骤...

## 输出规范

输出格式说明
```

### 完整示例

```markdown
---
name: code_review
description: 对 Python/JavaScript 代码进行结构审查和优化建议
version: 2.1.0
author: openclaw-ai
tags: [code-quality, security, performance]
compatibleAgents: [bingbu, xingbu, menxia]
---

# 代码审查技能

本技能专门用于对生产代码进行多维度审查...

## 输入

- `code`: 要审查的源代码
- `language`: 编程语言 (python, javascript, go, rust)
- `focusAreas`: 审查重点 (security, performance, style, structure)

## 处理流程

1. 语言识别与语法验证
2. 安全漏洞扫描
3. 性能瓶颈识别
4. 代码风格检查
5. 最佳实践建议

## 输出规范

```json
{
  "issues": [
    {
      "type": "security|performance|style|structure",
      "severity": "critical|high|medium|low",
      "location": "line:column",
      "message": "问题描述",
      "suggestion": "修复建议"
    }
  ],
  "summary": {
    "totalIssues": 3,
    "criticalCount": 1,
    "highCount": 2
  }
}
```

## 适用场景

- 兵部（代码实现）的代码产出审查
- 刑部（合规审计）的安全检查
- 门下省（审议把关）的质量评估

## 依赖与限制

- 需要 Python 3.9+
- 支持文件大小: 最多 50KB
- 执行超时: 30 秒
```

---

## 数据存储

### 本地存储结构

```
~/.openclaw/
├── workspace-zhongshu/
│   └── skills/
│       ├── code_review/
│       │   ├── SKILL.md
│       │   └── .source.json    # 存储源 URL 和元数据
│       └── api_design/
│           ├── SKILL.md
│           └── .source.json
├── ...
```

### .source.json 格式

```json
{
  "skillName": "code_review",
  "sourceUrl": "https://raw.githubusercontent.com/...",
  "description": "代码审查专项技能",
  "version": "2.1.0",
  "addedAt": "2026-03-02T14:30:00Z",
  "lastUpdated": "2026-03-02T14:30:00Z",
  "lastUpdateCheck": "2026-03-02T15:00:00Z",
  "checksum": "sha256:abc123...",
  "status": "valid"
}
```

---

## 安全考虑

### URL 验证

✅ **允许的 URL 类型:**
- HTTPS URLs: `https://`
- 本地文件: `file://` 或绝对路径
- 相对路径: `./skills/`

❌ **禁止的 URL 类型:**
- HTTP (非 HTTPS): `http://` 被拒绝
- 本地模式 HTTP: `http://localhost/` (避免环回攻击)
- FTP/SSH: `ftp://`, `ssh://`

### 内容验证

1. **格式验证**: 确保是有效的 Markdown YAML frontmatter
2. **大小限制**: 最多 10 MB
3. **超时保护**: 下载超过 30 秒自动中止
4. **路径遍历防护**: 检查解析后的 skill 名称，禁用 `../` 模式
5. **checksum 验证**: 可选的 GPG 签名验证（仅官方库）

### 隔离执行

- 远程 skills 在沙箱中执行（由 OpenClaw runtime 提供）
- 无法访问 `~/.openclaw/config.json` 等敏感文件
- 只能访问分配的 workspace 目录

---

## 故障排查

### 常见问题

**Q: 下载失败，提示 "Connection timeout"**

A: 检查网络连接和 URL 有效性：
```bash
curl -I https://raw.githubusercontent.com/...
```

**Q: Skill 显示 "invalid" 状态**

A: 检查文件格式：
```bash
python3 -m json.tool ~/.openclaw/workspace-zhongshu/skills/xxx/SKILL.md
```

**Q: 能否从私有 GitHub 仓库导入？**

A: 不支持（安全考虑）。可以：
1. 将仓库设为公开
2. 在本地下载后直接添加
3. 通过 GitHub Gist 的公开链接

**Q: 如何创建自己的 skills 库？**

A: 参考 [OpenClaw Skills Hub](https://github.com/openclaw-ai/skills-hub) 的结构创建自己的仓库，然后：

```bash
git clone https://github.com/yourname/my-skills-hub.git
cd my-skills-hub
# 创建 skill 文件结构
# 提交 & 推送到 GitHub
```

然后通过 URL 或官方库导入功能添加即可。

---

## 最佳实践

### 1. 版本管理

始终在 SKILL.md 的 frontmatter 中标注版本号：
```yaml
---
version: 2.1.0
---
```

### 2. 向后兼容

更新 skill 时保持输入/输出格式兼容，避免破坏现有流程。

### 3. 文档完整

包含详细的:
- 功能描述
- 适用场景
- 依赖说明
- 输出示例

### 4. 定期更新

设置定期检查更新（周期可在看板中配置）：
```bash
python3 scripts/skill_manager.py check-updates --interval weekly
```

### 5. 贡献社区

成熟的 skills 可向 [OpenClaw Skills Hub](https://github.com/openclaw-ai/skills-hub) 贡献。

---

## API 完整参考

详见 [任务分发流转架构文档](task-dispatch-architecture.md) 的第三部分（API 与工具）。

---

<p align="center">
  <sub>用 <strong>开放</strong> 的生态，赋能 <strong>制度化</strong> 的 AI 协作</sub>
</p>
