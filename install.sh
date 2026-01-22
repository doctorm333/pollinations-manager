#!/bin/bash

echo ""
echo "========================================================"
echo "       Pollinations Manager - Installer v2.0"
echo "              AI Chat Hub Edition"
echo "========================================================"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

echo "[0/5] Detected OS: $OS"

# Install tkinter dependencies
echo ""
echo "[1/5] Checking tkinter dependencies..."

if [[ "$OS" == "macos" ]]; then
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        # Check if tcl-tk is installed
        if ! brew list tcl-tk &> /dev/null; then
            echo "[INFO] Installing tcl-tk via Homebrew..."
            brew install tcl-tk
        fi

        # Get Python version and install python-tk
        PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if ! brew list python-tk@$PYTHON_VERSION &> /dev/null 2>&1; then
            echo "[INFO] Installing python-tk@$PYTHON_VERSION via Homebrew..."
            brew install python-tk@$PYTHON_VERSION 2>/dev/null || brew install python-tk 2>/dev/null || true
        fi
        echo "[OK] tkinter dependencies installed"
    else
        echo "[WARNING] Homebrew not found. If you get tkinter errors, install Homebrew and run:"
        echo "         brew install python-tk tcl-tk"
    fi
elif [[ "$OS" == "linux" ]]; then
    # Check if tkinter is available
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "[INFO] Installing python3-tk..."
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y python3-tk
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm tk
        elif command -v zypper &> /dev/null; then
            sudo zypper install -y python3-tk
        else
            echo "[WARNING] Could not detect package manager. Please install python3-tk manually."
        fi
    fi
    echo "[OK] tkinter dependencies checked"
fi

# Check Python
echo ""
echo "[2/5] Checking Python..."
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
echo "[3/5] Creating virtual environment..."
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
echo "[4/5] Installing dependencies..."
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
echo "[5/5] Setting up run script..."
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
