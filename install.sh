#!/bin/bash

# GenCAD AI Installation Script
# This script helps set up GenCAD AI on Linux systems

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${CYAN}$1${NC}"
}

# Header
clear
print_header "╔══════════════════════════════════════════════════════════════╗"
print_header "║                    GenCAD AI Installer                      ║"
print_header "║            Linux Desktop 3D Model Generator                 ║"
print_header "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. This script will install system packages."
    echo ""
fi

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    VERSION=$VERSION_ID
    print_status "Detected Linux distribution: $PRETTY_NAME"
else
    print_warning "Cannot detect Linux distribution. Proceeding with generic installation."
    DISTRO="unknown"
fi

echo ""

# Function to install FreeCAD based on distribution
install_freecad() {
    print_status "Installing FreeCAD..."
    
    case $DISTRO in
        ubuntu|debian)
            if command -v apt &> /dev/null; then
                sudo apt update
                sudo apt install -y freecad
            else
                print_error "apt package manager not found"
                return 1
            fi
            ;;
        fedora)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y freecad
            elif command -v yum &> /dev/null; then
                sudo yum install -y freecad
            else
                print_error "dnf/yum package manager not found"
                return 1
            fi
            ;;
        arch|manjaro)
            if command -v pacman &> /dev/null; then
                sudo pacman -S --needed freecad
            else
                print_error "pacman package manager not found"
                return 1
            fi
            ;;
        opensuse*|suse)
            if command -v zypper &> /dev/null; then
                sudo zypper install -y FreeCAD
            else
                print_error "zypper package manager not found"
                return 1
            fi
            ;;
        *)
            print_warning "Unsupported distribution for automatic FreeCAD installation."
            print_status "Please install FreeCAD manually using your distribution's package manager."
            print_status "Common commands:"
            print_status "  Ubuntu/Debian: sudo apt install freecad"
            print_status "  Fedora: sudo dnf install freecad"
            print_status "  Arch: sudo pacman -S freecad"
            print_status "  openSUSE: sudo zypper install FreeCAD"
            return 1
            ;;
    esac
}

# Check Python 3
print_status "Checking Python 3 installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed!"
    print_status "Installing Python 3..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update && sudo apt install -y python3 python3-pip python3-tk
            ;;
        fedora)
            sudo dnf install -y python3 python3-pip python3-tkinter
            ;;
        arch|manjaro)
            sudo pacman -S --needed python python-pip tk
            ;;
        opensuse*|suse)
            sudo zypper install -y python3 python3-pip python3-tk
            ;;
        *)
            print_error "Please install Python 3 manually"
            exit 1
            ;;
    esac
fi

# Check pip
print_status "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
elif command -v pip &> /dev/null; then
    print_success "pip found"
else
    print_error "pip is not installed!"
    print_status "Installing pip..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt install -y python3-pip
            ;;
        fedora)
            sudo dnf install -y python3-pip
            ;;
        arch|manjaro)
            sudo pacman -S --needed python-pip
            ;;
        opensuse*|suse)
            sudo zypper install -y python3-pip
            ;;
        *)
            print_error "Please install pip manually"
            exit 1
            ;;
    esac
fi

# Check FreeCAD
print_status "Checking FreeCAD installation..."
if command -v freecad &> /dev/null; then
    FREECAD_VERSION=$(freecad --version 2>&1 | head -n 1 || echo "Version information not available")
    print_success "FreeCAD found: $FREECAD_VERSION"
else
    print_warning "FreeCAD is not installed!"
    read -p "Would you like to install FreeCAD? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if install_freecad; then
            print_success "FreeCAD installed successfully"
        else
            print_warning "FreeCAD installation failed or was skipped"
            print_status "You can install it manually later"
        fi
    else
        print_warning "Skipping FreeCAD installation"
        print_status "Note: FreeCAD is required for GenCAD AI to function properly"
    fi
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install requests
elif command -v pip &> /dev/null; then
    pip install requests
else
    print_error "Cannot install Python dependencies - pip not found"
    exit 1
fi

print_success "Python dependencies installed"

# Make scripts executable
print_status "Setting up executable permissions..."
chmod +x "$(dirname "$0")/launch.sh"
chmod +x "$(dirname "$0")/test_gencad.py"

# Test the installation
print_status "Testing installation..."
if python3 "$(dirname "$0")/test_gencad.py"; then
    print_success "Installation test passed!"
else
    print_warning "Installation test had some issues, but GenCAD AI might still work"
fi

# Create desktop entry (optional)
print_status "Setting up desktop integration..."
DESKTOP_FILE="$HOME/Desktop/GenCAD-AI.desktop"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GenCAD AI
Comment=Generate 3D CAD Models from Text Prompts using AI
Exec=$APP_DIR/launch.sh
Icon=applications-engineering
Terminal=false
Categories=Graphics;Engineering;
StartupNotify=true
Keywords=CAD;3D;AI;FreeCAD;Model;Design;
EOF

chmod +x "$DESKTOP_FILE"
print_success "Desktop shortcut created: $DESKTOP_FILE"

# Final summary
echo ""
print_header "╔══════════════════════════════════════════════════════════════╗"
print_header "║                    Installation Complete!                   ║"
print_header "╚══════════════════════════════════════════════════════════════╝"
echo ""
print_success "GenCAD AI has been set up successfully!"
echo ""
print_status "To launch GenCAD AI, you can:"
print_status "  1. Double-click the desktop shortcut: GenCAD-AI.desktop"
print_status "  2. Run the launch script: ./launch.sh"
print_status "  3. Run directly: python3 gencad_ai.py"
echo ""
print_status "For help and examples, see:"
print_status "  - README.md (full documentation)"
print_status "  - examples/example_prompts.md (example prompts to try)"
echo ""
print_warning "Important: Make sure you have a valid internet connection"
print_warning "when using GenCAD AI as it requires access to Google's Gemini API."
echo ""
print_status "Enjoy creating 3D models with AI!"
