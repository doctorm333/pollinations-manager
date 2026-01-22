@echo off
title Pollinations Manager - Build EXE

echo.
echo ========================================================
echo        Pollinations Manager - EXE Builder
echo ========================================================
echo.

:: Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found!
    echo Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

:: Create/activate venv if needed
echo.
echo [2/4] Setting up environment...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Install dependencies
echo.
echo [3/4] Installing build dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
pip install -r build_requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

:: Build EXE
echo.
echo [4/4] Building EXE (this may take a few minutes)...
echo.

pyinstaller pollinations_manager.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

:: Done
echo.
echo ========================================================
echo                  Build complete!
echo ========================================================
echo.
echo EXE location: dist\Pollinations Manager.exe
echo.
echo You can now distribute this file to users.
echo.

pause
