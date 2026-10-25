@echo off
setlocal enabledelayedexpansion
title Smart Approval AI - All-in-One Dev + Ngrok Launcher

:: Read configuration from .env if present
if exist "%~dp0.env" (
    for /f "usebackq tokens=1,* delims==" %%A in ("%~dp0.env") do (
        set "KEY=%%A"
        set "VAL=%%B"
        if "!KEY!"=="BACKEND_PORT" set "BACKEND_PORT=!VAL!"
        if "!KEY!"=="FRONTEND_PORT" set "FRONTEND_PORT=!VAL!"
        if "!KEY!"=="PORT" set "PORT=!VAL!"
        if "!KEY!"=="NGROK_INSPECT_PORT" set "NGROK_INSPECT_PORT=!VAL!"
    )
)

if "%BACKEND_PORT%"=="" set "BACKEND_PORT=8051"
if "%FRONTEND_PORT%"=="" (
    if not "%PORT%"=="" (
        set "FRONTEND_PORT=%PORT%"
    ) else (
        set "FRONTEND_PORT=3051"
    )
)
if "%NGROK_INSPECT_PORT%"=="" set "NGROK_INSPECT_PORT=4051"

echo ===============================================================
echo     Smart Approval AI - Full Stack + Ngrok Launcher
echo ===============================================================
echo [INFO] Configured Ports (Non-Conflicting with other projects):
echo   - Backend Port:        %BACKEND_PORT%
echo   - Frontend Port:       %FRONTEND_PORT%
echo   - Ngrok Inspector:     %NGROK_INSPECT_PORT%
echo ===============================================================

echo [1/3] Starting FastAPI Backend on port %BACKEND_PORT% ...
start "Smart Approval AI - Backend (Port %BACKEND_PORT%)" cmd /k "cd /d "%~dp0backend" && set "BACKEND_PORT=%BACKEND_PORT%" && start_server.bat"

echo [2/3] Starting Next.js Frontend on port %FRONTEND_PORT% ...
start "Smart Approval AI - Frontend (Port %FRONTEND_PORT%)" cmd /k "cd /d "%~dp0frontend" && set "BACKEND_PORT=%BACKEND_PORT%" && npx next dev -p %FRONTEND_PORT%"

echo [3/3] Waiting 4 seconds for frontend to initialize before opening Ngrok...
timeout /t 4 /nobreak >nul

echo Starting Ngrok Tunnel...
start "Smart Approval AI - Ngrok (Port %FRONTEND_PORT%)" cmd /k "cd /d "%~dp0" && start_ngrok.bat"

echo.
echo ===============================================================
echo  All services are launching:
echo    - Local Frontend:      http://localhost:%FRONTEND_PORT%
echo    - Local Backend API:   http://localhost:%BACKEND_PORT% (Docs: /docs)
echo    - Ngrok Web Inspector: http://127.0.0.1:%NGROK_INSPECT_PORT%
echo ===============================================================
echo  Check the Ngrok window to copy your public HTTPS URL!
echo ===============================================================
pause
