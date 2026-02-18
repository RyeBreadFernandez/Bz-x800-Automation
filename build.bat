@echo off
echo ================================================
echo Building Bz-x800 Automation Standalone Application
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Building executable with PyInstaller...

REM Check if icon exists, build accordingly
if exist "assets\icon.ico" (
    echo Using custom icon...
    pyinstaller --noconfirm --onefile --windowed ^
        --name "Microscope_Automation" ^
        --icon=assets/icon.ico ^
        --add-data "core;core" ^
        main.py
) else (
    echo No custom icon found, using default...
    pyinstaller --noconfirm --onefile --windowed ^
        --name "Microscope_Automation" ^
        --add-data "core;core" ^
        main.py
)

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build Complete!
echo ================================================
echo.
echo The executable is located in: dist\Microscope_Automation.exe
echo.
echo You can copy this .exe file to any Windows computer and run it
echo without needing Python installed!
echo.
pause
