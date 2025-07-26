#!/bin/bash

# GenCAD AI Launcher Script
# This script provides an easy way to launch the GenCAD AI application

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}GenCAD AI - Linux Desktop 3D Model Generator${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    echo "Please install Python 3 using your system's package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora: sudo dnf install python3"
    echo "  Arch: sudo pacman -S python"
    exit 1
fi

# Check if FreeCAD is installed
if ! command -v freecad &> /dev/null; then
    echo -e "${YELLOW}Warning: FreeCAD is not installed or not in PATH${NC}"
    echo "FreeCAD is required for generating 3D models."
    echo "Install FreeCAD using your system's package manager:"
    echo "  Ubuntu/Debian: sudo apt install freecad"
    echo "  Fedora: sudo dnf install freecad"
    echo "  Arch: sudo pacman -S freecad"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if requests module is available
if ! python3 -c "import requests" &> /dev/null; then
    echo -e "${YELLOW}Warning: Python 'requests' module not found${NC}"
    echo "Installing requests module..."
    pip3 install requests
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install requests module${NC}"
        echo "Please install manually: pip3 install requests"
        exit 1
    fi
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if the main application file exists
if [ ! -f "$SCRIPT_DIR/gencad_ai.py" ]; then
    echo -e "${RED}Error: gencad_ai.py not found in $SCRIPT_DIR${NC}"
    echo "Please ensure all files are in the correct location."
    exit 1
fi

echo -e "${GREEN}All dependencies checked. Launching GenCAD AI...${NC}"
echo ""

# Change to the script directory and run the application
cd "$SCRIPT_DIR"
python3 gencad_ai.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}GenCAD AI exited successfully.${NC}"
else
    echo -e "${RED}GenCAD AI exited with an error.${NC}"
fi
