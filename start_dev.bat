@echo off
setlocal enabledelayedexpansion
title Smart Approval AI Launcher

:: Read configuration from .env if present
if exist "%~dp0.env" (
    for /f "usebackq tokens=1,* delims==" %%A in ("%~dp0.env") do (
        set "KEY=%%A"
        set "VAL=%%B"
        if "!KEY!"=="BACKEND_PORT" set "BACKEND_PORT=!VAL!"
        if "!KEY!"=="FRONTEND_PORT" set "FRONTEND_PORT=!VAL!"
        if "!KEY!"=="PORT" set "PORT=!VAL!"
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

echo ===================================================
echo   Starting Smart Approval AI (Backend + Frontend)
echo ===================================================
echo [1/2] Launching Backend (FastAPI) on http://localhost:%BACKEND_PORT% ...
start "Smart Approval AI - Backend (Port %BACKEND_PORT%)" cmd /k "cd /d "%~dp0backend" && set "BACKEND_PORT=%BACKEND_PORT%" && start_server.bat"

echo [2/2] Launching Frontend (Next.js) on http://localhost:%FRONTEND_PORT% ...
start "Smart Approval AI - Frontend (Port %FRONTEND_PORT%)" cmd /k "cd /d "%~dp0frontend" && set "BACKEND_PORT=%BACKEND_PORT%" && npx next dev -p %FRONTEND_PORT%"

echo ===================================================
echo Backend API:  http://localhost:%BACKEND_PORT% (Docs: /docs)
echo Frontend App: http://localhost:%FRONTEND_PORT%
echo ===================================================
pause
