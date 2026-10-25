@echo off
title Smart Approval AI Launcher
echo ===================================================
echo   Starting Smart Approval AI (Backend + Frontend)
echo ===================================================

if "%BACKEND_PORT%"=="" set BACKEND_PORT=8050
if "%FRONTEND_PORT%"=="" set FRONTEND_PORT=3050

echo [1/2] Launching Backend (FastAPI) on http://localhost:%BACKEND_PORT% ...
start "Smart Approval AI - Backend (Port %BACKEND_PORT%)" cmd /k "cd /d %~dp0backend && set BACKEND_PORT=%BACKEND_PORT% && start_server.bat"

echo [2/2] Launching Frontend (Next.js) on http://localhost:%FRONTEND_PORT% ...
start "Smart Approval AI - Frontend (Port %FRONTEND_PORT%)" cmd /k "cd /d %~dp0frontend && set BACKEND_PORT=%BACKEND_PORT% && npx next dev -p %FRONTEND_PORT%"

echo ===================================================
echo Backend API:  http://localhost:%BACKEND_PORT% (Docs: /docs)
echo Frontend App: http://localhost:%FRONTEND_PORT%
echo ===================================================
