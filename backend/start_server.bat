@echo off
echo Starting Smart Approval AI Backend Server...
cd /d %~dp0
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found (.venv or venv).
    pause
    exit /b 1
)
if "%BACKEND_PORT%"=="" set BACKEND_PORT=8051
echo Starting FastAPI server on http://127.0.0.1:%BACKEND_PORT%
python -m uvicorn main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload
pause
