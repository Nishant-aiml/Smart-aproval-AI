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
        if "!KEY!"=="BACKEND_PORT" set "BACKEND_PORT=!VAL!"
    )
)

if "%PORT%"=="" (
    if not "%FRONTEND_PORT%"=="" (
        set "PORT=%FRONTEND_PORT%"
    ) else (
        set "PORT=3051"
    )
)
if "%BACKEND_PORT%"=="" set "BACKEND_PORT=8051"
if "%NGROK_INSPECT_PORT%"=="" set "NGROK_INSPECT_PORT=4051"
set "LOCAL_NGROK_CONFIG=%~dp0ngrok.yml"

:: Locate existing global/user ngrok configuration
set "USER_NGROK_CONFIG="
if exist "%LOCALAPPDATA%\ngrok\ngrok.yml" (
    set "USER_NGROK_CONFIG=%LOCALAPPDATA%\ngrok\ngrok.yml"
) else (
    for /d %%D in ("%LOCALAPPDATA%\Packages\ngrok.ngrok_*") do (
        if exist "%%D\LocalCache\Local\ngrok\ngrok.yml" (
            set "USER_NGROK_CONFIG=%%D\LocalCache\Local\ngrok\ngrok.yml"
        )
    )
)

echo.
echo [PORT ALLOCATION FOR MULTI-PROJECT ISOLATION]
echo   - Local Frontend Port:   %PORT%
echo   - Backend Proxy Port:    %BACKEND_PORT% (routed via /api)
echo   - Ngrok Web Inspector:   http://127.0.0.1:%NGROK_INSPECT_PORT%
echo.

:: Build Ngrok command flags
set NGROK_CMD=ngrok http %PORT%

if not "%NGROK_AUTHTOKEN%"=="" (
    echo [INFO] Using dedicated NGROK_AUTHTOKEN from .env for project isolation.
    set NGROK_CMD=!NGROK_CMD! --authtoken %NGROK_AUTHTOKEN%
) else if not "%USER_NGROK_CONFIG%"=="" (
    set NGROK_CMD=!NGROK_CMD! --config "%USER_NGROK_CONFIG%"
)

if exist "%LOCAL_NGROK_CONFIG%" (
    set NGROK_CMD=!NGROK_CMD! --config "%LOCAL_NGROK_CONFIG%"
)

if not "%NGROK_DOMAIN%"=="" (
    echo [INFO] Using dedicated NGROK_DOMAIN: %NGROK_DOMAIN%
    set NGROK_CMD=!NGROK_CMD! --url %NGROK_DOMAIN%
)

echo Starting: !NGROK_CMD!
echo.
echo ===============================================================
echo.

!NGROK_CMD!

pause
