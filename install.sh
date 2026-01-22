#!/bin/bash

echo ""
echo "========================================================"
echo "       Pollinations Manager - Installer v2.0"
echo "              AI Chat Hub Edition"
echo "========================================================"
echo ""

# Check Python
echo "[1/4] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERROR] Python3 not found!"
    echo "Install Python 3.10+ from https://python.org"
    echo "Or use: brew install python3 (macOS)"
    echo "Or use: sudo apt install python3 python3-venv (Ubuntu/Debian)"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "[OK] Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "[INFO] Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created"
fi

# Activate and install dependencies
echo ""
echo "[3/4] Installing dependencies..."
source venv/bin/activate

python -m pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "[OK] Dependencies installed"

# Make run script executable
echo ""
echo "[4/4] Setting up run script..."
chmod +x run.sh
echo "[OK] run.sh is ready"

# Done
echo ""
echo "========================================================"
echo "             Installation complete!"
echo "========================================================"
echo ""
echo "To start the app, run: ./run.sh"
echo ""

read -p "Launch now? (y/n): " LAUNCH
if [[ "$LAUNCH" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting Pollinations Manager..."
    python main.py
fi
