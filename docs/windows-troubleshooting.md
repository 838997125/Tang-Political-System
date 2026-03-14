# Windows 安装故障排查指南

如果你在 Windows 上安装 Tang Political System 时遇到问题，请参考以下解决方案。

---

## 🔴 执行策略错误

### 问题现象
```
无法加载文件 .\install.ps1，因为在此系统上禁止运行脚本。
有关详细信息，请参阅 https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
```

### 解决方案

#### 方案 1：使用 install.bat（推荐）
```batch
# 在项目目录中双击运行，或在命令行执行
install.bat
```

`install.bat` 会自动绕过执行策略限制，无需手动修改系统设置。

#### 方案 2：临时允许当前会话
```powershell
# 在 PowerShell 中运行
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\install.ps1
```

#### 方案 3：查看当前执行策略
```powershell
Get-ExecutionPolicy
# 如果是 Restricted，需要修改为 RemoteSigned 或 Bypass
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🔴 依赖未找到

### OpenClaw CLI 未找到
```
[ERR] openclaw CLI not found. Please install OpenClaw first: https://openclaw.ai
```

**解决方案**：
1. 访问 https://openclaw.ai 安装 OpenClaw
2. 安装完成后运行 `openclaw` 初始化配置
3. 确保 `openclaw` 命令在 PATH 中

### Python 未找到
```
[ERR] Python not found. Please install Python 3.9+ from https://www.python.org/downloads/
```

**解决方案**：
1. 从 https://www.python.org/downloads/ 下载 Python 3.9+
2. 安装时勾选 "Add Python to PATH"
3. 重新打开 PowerShell 再试

### openclaw.json 未找到
```
[ERR] openclaw.json not found at C:\Users\<用户名>\.openclaw\openclaw.json
```

**解决方案**：
```powershell
# 运行 OpenClaw 初始化
openclaw
# 按照提示完成配置
```

---

## 🔴 Gateway 相关问题

### Gateway 未启动
```
[WARN] Gateway restart failed, please restart manually with: openclaw gateway restart
```

**解决方案**：
```powershell
# 手动启动 Gateway
openclaw gateway start

# 检查 Gateway 状态
openclaw gateway status

# 如果启动失败，查看日志
cat $env:LOCALAPPDATA\Temp\openclaw\openclaw-*.log | Select-Object -Last 50
```

---

## 🟡 其他常见问题

### 安装过程中断
如果安装过程中断，可能导致配置不完整。

**解决方案**：
```powershell
# 运行卸载脚本清理
.\uninstall.ps1 -Force

# 重新安装
.\install.ps1
```

### 如何预览安装（不实际修改）
```powershell
# 试运行模式
.\install.ps1 -DryRun
```

### 如何跳过确认提示
```powershell
# 强制安装模式
.\install.ps1 -Force
```

### 如何跳过 Gateway 重启
```powershell
# 安装但不重启 Gateway
.\install.ps1 -SkipGatewayRestart
```

---

## 📞 获取帮助

如果以上方案无法解决你的问题：

1. 查看 [GitHub Issues](https://github.com/838997125/Tang-Political-System/issues)
2. 提交新的 Issue，包含：
   - 操作系统版本
   - PowerShell 版本 (`$PSVersionTable.PSVersion`)
   - 完整的错误信息
   - 已尝试的解决方案

---

## ✅ 安装前检查清单

在运行安装脚本前，请确认：

- [ ] Windows 10/11 (64位)
- [ ] Python 3.9+ 已安装并添加到 PATH
- [ ] OpenClaw CLI 已安装 (`openclaw --version`)
- [ ] OpenClaw 已初始化 (`openclaw.json` 存在)
- [ ] 了解安装会修改 `openclaw.json` 配置文件
- [ ] 已备份重要配置（可选但推荐）
