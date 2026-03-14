# Tang Political System v1.1.0 发布说明

## 🎉 重要更新

本次更新主要针对用户反馈的问题 #9 进行了全面优化，提升了安装体验并增加了卸载功能。

---

## ✨ 新功能

### 1. 安装脚本增强 (`install.ps1`)

#### 新增参数支持
| 参数 | 说明 |
|------|------|
| `-DryRun` | 预览模式，显示将要执行的操作但不实际修改 |
| `-Force` | 跳过安装前确认提示 |
| `-SkipGatewayRestart` | 安装完成后不自动重启 Gateway |

#### 改进功能
- ✅ **安装前配置摘要**：显示将要添加的 10 个 Agent 列表
- ✅ **安装前确认提示**：明确告知用户会修改 `openclaw.json`
- ✅ **优化 Python 检测**：Windows 优先检测 `py` 命令
- ✅ **改进错误提示**：更友好的依赖缺失提示

**使用示例：**
```powershell
# 预览安装（不实际执行）
.\install.ps1 -DryRun

# 跳过确认直接安装
.\install.ps1 -Force

# 安装但不重启 Gateway
.\install.ps1 -SkipGatewayRestart
```

---

### 2. 新增 `install.bat` (Windows 推荐)

**解决 PowerShell 执行策略问题**

用户无需再手动运行 `Set-ExecutionPolicy`，直接双击 `install.bat` 即可：

```batch
# 最简单的方式
install.bat

# 传递参数
install.bat -DryRun
install.bat -Force
```

---

### 3. 新增 `uninstall.ps1`

**完全卸载 Tang Political System**

| 参数 | 说明 |
|------|------|
| `-Force` | 跳过卸载确认提示 |
| `-KeepBackup` | 保留配置备份文件 |

**卸载功能：**
- ✅ 从 `openclaw.json` 移除所有 Tang Political System Agent
- ✅ 可选择恢复安装前的配置备份
- ✅ 清理工作空间目录
- ✅ 自动重启 Gateway

**使用示例：**
```powershell
# 交互式卸载
.\uninstall.ps1

# 强制卸载（跳过确认）
.\uninstall.ps1 -Force

# 卸载但保留备份
.\uninstall.ps1 -KeepBackup
```

---

### 4. README 文档更新

- ✅ **添加安装警告**：明确说明会修改 `openclaw.json`
- ✅ **更新安装说明**：推荐使用 `install.bat`
- ✅ **添加卸载说明**：完整的卸载指南
- ✅ **添加参数说明**：所有脚本参数详细说明

---

## 🔧 问题修复

### 问题 #9：安装过程会修改 openclaw.json（已解决）

**之前的痛点：**
- 用户不知道安装会修改核心配置文件
- 安装后难以回滚
- PowerShell 执行策略阻碍安装

**解决方案：**
1. ✅ 安装前显示配置摘要
2. ✅ 安装前确认提示
3. ✅ 自动创建配置备份
4. ✅ 提供完整的卸载脚本
5. ✅ 提供 `install.bat` 绕过执行策略
6. ✅ README 明确标注风险

---

## 📋 文件变更

```
新增：
  + install.bat      # Windows 安装批处理
  + uninstall.ps1    # 卸载脚本

修改：
  ~ install.ps1      # 增强版安装脚本
  ~ README.md        # 更新文档
```

---

## 🚀 快速开始

### 新用户安装

```batch
# 1. 克隆项目
git clone https://github.com/838997125/Tang-Political-System.git
cd Tang-Political-System

# 2. 运行安装（推荐）
install.bat

# 或 PowerShell
.\install.ps1
```

### 现有用户升级

```powershell
# 1. 拉取最新代码
git pull origin master

# 2. 重新运行安装
.\install.ps1
```

### 如需卸载

```powershell
.\uninstall.ps1
```

---

## 🙏 致谢

感谢用户反馈的问题 #9，这些改进让 Tang Political System 的安装体验更加友好和安全。

---

**完整更新日志**: [View on GitHub](https://github.com/838997125/Tang-Political-System/commits/master)

**问题反馈**: [GitHub Issues](https://github.com/838997125/Tang-Political-System/issues)
