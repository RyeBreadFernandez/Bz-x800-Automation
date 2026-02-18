@echo off
REM Simple launcher for Microscope Automation
REM Double-click this file to run the program

echo Starting Microscope Automation...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "venv\" (
    echo First time setup - installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the program
python main.py

pause
