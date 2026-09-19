@echo off
title ORCAMarine Tests

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Run START_WINDOWS.bat first.
    pause
    exit /b 1
)

echo Running ORCAMarine tests...
echo.
call ".venv\Scripts\python.exe" -m pytest -v
echo.
pause
