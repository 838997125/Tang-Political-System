@echo off
chcp 65001 >nul
echo ==========================================
echo   Edict - OpenClaw Multi-Agent System
echo   Windows Installer (Batch Wrapper)
echo ==========================================
echo.

:: Check if PowerShell is available
where powershell >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERR] PowerShell not found. Please install PowerShell 5.1 or later.
    exit /b 1
)

echo [INFO] Starting installation with bypass execution policy...
echo.

:: Run the PowerShell script with bypass execution policy
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*

if %errorlevel% neq 0 (
    echo.
    echo [ERR] Installation failed with error code %errorlevel%
    exit /b %errorlevel%
)

echo.
echo [OK] Installation completed!
pause
