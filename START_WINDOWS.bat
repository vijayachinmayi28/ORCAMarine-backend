@echo off
title ORCAMarine Backend

echo ==========================================
echo        ORCAMarine Backend
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python could not create the virtual environment.
        echo Make sure Python is installed and added to PATH.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Virtual environment already exists.
)

echo.
echo [2/3] Installing/updating dependencies...
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)

if not exist ".env" (
    echo.
    echo Creating .env from .env.example...
    copy /Y ".env.example" ".env" >nul
)

echo.
echo [3/3] Starting ORCAMarine API...
echo.
echo Swagger docs: http://127.0.0.1:8000/docs
echo Health:       http://127.0.0.1:8000/health
echo.
echo Press CTRL+C to stop the server.
echo.

call ".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000

pause
