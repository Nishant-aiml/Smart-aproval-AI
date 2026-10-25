@echo off
title Smart Approval AI - All-in-One Dev + Ngrok Launcher
echo ===============================================================
echo     Smart Approval AI - Full Stack + Ngrok Launcher
echo ===============================================================
echo [INFO] Configured Ports (Non-Conflicting with other projects):
echo   - Backend Port:        8050
echo   - Frontend Port:       3050
echo   - Ngrok Inspector:     4050
echo ===============================================================

if "%BACKEND_PORT%"=="" set BACKEND_PORT=8050
if "%FRONTEND_PORT%"=="" set FRONTEND_PORT=3050

echo [1/3] Starting FastAPI Backend on port %BACKEND_PORT% ...
start "Smart Approval AI - Backend (Port %BACKEND_PORT%)" cmd /k "cd /d %~dp0backend && set BACKEND_PORT=%BACKEND_PORT% && start_server.bat"

echo [2/3] Starting Next.js Frontend on port %FRONTEND_PORT% ...
start "Smart Approval AI - Frontend (Port %FRONTEND_PORT%)" cmd /k "cd /d %~dp0frontend && set BACKEND_PORT=%BACKEND_PORT% && npx next dev -p %FRONTEND_PORT%"

echo [3/3] Waiting 4 seconds for frontend to initialize before opening Ngrok...
timeout /t 4 /nobreak >nul

echo Starting Ngrok Tunnel...
start "Smart Approval AI - Ngrok (Port %FRONTEND_PORT%)" cmd /k "cd /d %~dp0 && start_ngrok.bat"

echo.
echo ===============================================================
echo  All services are launching:
echo    - Local Frontend:      http://localhost:%FRONTEND_PORT%
echo    - Local Backend API:   http://localhost:%BACKEND_PORT% (Docs: /docs)
echo    - Ngrok Web Inspector: http://127.0.0.1:4050
echo ===============================================================
echo  Check the Ngrok window to copy your public HTTPS URL!
echo ===============================================================
pause
