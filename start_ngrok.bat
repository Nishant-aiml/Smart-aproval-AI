@echo off
setlocal enabledelayedexpansion
title Smart Approval AI - Ngrok Tunnel
echo ===============================================================
echo     Smart Approval AI - Ngrok Tunnel Launcher
echo ===============================================================

where ngrok >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] ngrok is not found in PATH!
    echo Please install ngrok or add it to your system PATH.
    pause
    exit /b 1
)

:: Read configuration from .env if present
if exist "%~dp0.env" (
    for /f "usebackq tokens=1,* delims==" %%A in ("%~dp0.env") do (
        set "KEY=%%A"
        set "VAL=%%B"
        if "!KEY!"=="NGROK_AUTHTOKEN" set "NGROK_AUTHTOKEN=!VAL!"
        if "!KEY!"=="NGROK_DOMAIN" set "NGROK_DOMAIN=!VAL!"
        if "!KEY!"=="NGROK_INSPECT_PORT" set "NGROK_INSPECT_PORT=!VAL!"
        if "!KEY!"=="PORT" set "PORT=!VAL!"
        if "!KEY!"=="FRONTEND_PORT" set "FRONTEND_PORT=!VAL!"
    )
)

if "%PORT%"=="" set PORT=3050
if "%NGROK_INSPECT_PORT%"=="" set NGROK_INSPECT_PORT=4050
set LOCAL_NGROK_CONFIG=%~dp0ngrok.yml
set USER_NGROK_CONFIG=%LOCALAPPDATA%\ngrok\ngrok.yml

echo.
echo [PORT ALLOCATION FOR MULTI-PROJECT ISOLATION]
echo   - Local Frontend Port:   %PORT%
echo   - Backend Proxy Port:    8050 (routed via /api)
echo   - Ngrok Web Inspector:   http://127.0.0.1:%NGROK_INSPECT_PORT%
echo.

:: Build Ngrok command flags
set NGROK_CMD=ngrok http %PORT% --web-addr=127.0.0.1:%NGROK_INSPECT_PORT%

if not "%NGROK_AUTHTOKEN%"=="" (
    echo [INFO] Using dedicated NGROK_AUTHTOKEN from .env for project isolation.
    set NGROK_CMD=!NGROK_CMD! --authtoken %NGROK_AUTHTOKEN%
) else if exist "%USER_NGROK_CONFIG%" (
    set NGROK_CMD=!NGROK_CMD! --config "%USER_NGROK_CONFIG%"
)

if not "%NGROK_DOMAIN%"=="" (
    echo [INFO] Using dedicated NGROK_DOMAIN: %NGROK_DOMAIN%
    set NGROK_CMD=!NGROK_CMD! --url %NGROK_DOMAIN%
)

echo Starting: !NGROK_CMD!
echo.
echo If you see ERR_NGROK_334 (domain already online), another project is
echo currently using your primary ngrok domain. To run both concurrently:
echo   1. Create a free secondary ngrok account at https://dashboard.ngrok.com
echo   2. Add NGROK_AUTHTOKEN=your_secondary_token to this project's .env
echo   3. Re-run this script.
echo ===============================================================
echo.

!NGROK_CMD!

pause
