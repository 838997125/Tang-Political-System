# Edict Windows 安装指南

## 前置条件

- Windows 10/11
- Python 3.9+
- Node.js 18+ (可选，用于构建前端)
- OpenClaw CLI 已安装

## 安装步骤

### 1. 安装依赖

```powershell
# 安装 Python 依赖
pip install psutil

# 确保 OpenClaw 已安装
openclaw --version
```

### 2. 运行安装脚本

```powershell
# 以管理员身份打开 PowerShell，进入项目目录
cd D:\code\edict-main

# 执行安装脚本
.\install.ps1
```

### 3. 启动数据刷新循环

```powershell
# 在新窗口中运行
.\scripts\run_loop.ps1
```

### 4. 启动看板服务器

```powershell
# 在另一个新窗口中运行
python dashboard/server.py
```

### 5. 访问看板

打开浏览器访问 http://127.0.0.1:7891

## 一键启动

也可以使用一键启动脚本：

```powershell
.\start-windows.ps1
```

这将同时启动数据刷新循环和看板服务器。

## 常见问题

### 1. 执行策略限制

如果 PowerShell 提示执行策略限制，运行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Python 命令找不到

确保 Python 已添加到系统 PATH，或使用 `py` 命令代替 `python`。

### 3. 端口被占用

如果 7891 端口被占用，修改 `dashboard/server.py` 中的端口配置或关闭占用该端口的程序。

---

本文档由 `WINDOWS_INSTALL.md` 迁移而来。
