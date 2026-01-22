@echo off
title Pollinations Manager - Install

echo.
echo ========================================================
echo        Pollinations Manager - Installer v2.0
echo                 AI Chat Hub Edition
echo ========================================================
echo.

:: Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found!
    echo Install Python 3.10+ from https://python.org
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

:: Create virtual environment
echo.
echo [2/4] Creating virtual environment...
if exist "venv" (
    echo [INFO] Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

:: Activate and install dependencies
echo.
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat

python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

:: Create run script
echo.
echo [4/4] Creating run script...

echo @echo off > run.bat
echo cd /d "%%~dp0" >> run.bat
echo call venv\Scripts\activate.bat >> run.bat
echo python main.py >> run.bat

echo [OK] run.bat created

:: Done
echo.
echo ========================================================
echo              Installation complete!
echo ========================================================
echo.
echo To start the app, run: run.bat
echo.

set /p LAUNCH="Launch now? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    echo.
    echo Starting Pollinations Manager...
    python main.py
)

pause
