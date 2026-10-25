@echo off
title Smart Approval AI Launcher
echo ===================================================
echo   Starting Smart Approval AI (Backend + Frontend)
echo ===================================================

echo [1/2] Launching Backend (FastAPI) on http://localhost:8000 ...
start "Smart Approval AI - Backend" cmd /k "cd /d %~dp0backend && start_server.bat"

echo [2/2] Launching Frontend (Next.js) on http://localhost:3000 ...
start "Smart Approval AI - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo ===================================================
echo Backend API Docs: http://localhost:8000/docs
echo Frontend Web App: http://localhost:3000
echo ===================================================
