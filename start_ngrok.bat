@echo off
title Smart Approval AI - Ngrok Tunnel
echo ===================================================
echo     Smart Approval AI - Ngrok Tunnel Launcher
echo ===================================================

where ngrok >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] ngrok is not found in PATH!
    echo Please install ngrok or add it to your system PATH.
    pause
    exit /b 1
)

set USER_NGROK_CONFIG=%LOCALAPPDATA%\ngrok\ngrok.yml
set LOCAL_NGROK_CONFIG=%~dp0ngrok.yml

if not exist "%USER_NGROK_CONFIG%" (
    echo [WARNING] Global ngrok config not found at %USER_NGROK_CONFIG%
    echo If ngrok asks for an authtoken, run: ngrok config add-authtoken ^<YOUR_TOKEN^>
)

echo.
echo Starting Ngrok tunnel for Smart Approval AI...
echo [INFO] Local Frontend Port: 3050
echo [INFO] Backend Proxy: http://127.0.0.1:8050 (routed via /api)
echo [INFO] Ngrok Web Inspector: http://127.0.0.1:4050
echo.

if "%NGROK_DOMAIN%" neq "" (
    echo [INFO] Using custom ngrok domain: %NGROK_DOMAIN%
    ngrok http 3050 --url %NGROK_DOMAIN% --config "%USER_NGROK_CONFIG%" --config "%LOCAL_NGROK_CONFIG%"
) else (
    ngrok start smart_approval --config "%USER_NGROK_CONFIG%" --config "%LOCAL_NGROK_CONFIG%"
)

pause
