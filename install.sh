#!/bin/bash
# Installation script for cliai

echo "CLI AI Chat Installation Script"
echo "=============================="
echo

# Check if uv is installed
if command -v uv >/dev/null 2>&1; then
    echo "uv found, using uv for installation (recommended)"
    USE_UV=true
else
    echo "uv not found, using traditional pip/venv"
    echo "Consider installing uv for better dependency management:"
    echo "curl -sSf https://astral.sh/uv/install.sh | sh"
    echo
    USE_UV=false
fi

# Check for Python 3.12+
if [ "$USE_UV" = true ]; then
    echo "Checking for Python 3.12 using uv..."
    # uv will handle Python version management
else
    echo "Checking for Python 3.12..."
    command -v python3.12 >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Python 3.12 is not found in your system."
        echo "You need Python 3.12 or newer to use this application."
        echo
        echo "Installation options:"
        echo "1. macOS (Homebrew): brew install python@3.12"
        echo "2. Ubuntu/Debian: sudo apt install python3.12"
        echo "3. Download from https://www.python.org/downloads/"
        echo "4. Install uv: curl -sSf https://astral.sh/uv/install.sh | sh"
        echo
        echo "After installing Python 3.12 or uv, run this script again."
        exit 1
    fi

    # Print Python version
    python_version=$(python3.12 --version)
    echo "Found $python_version"
fi

echo

# Create and set up environment
if [ "$USE_UV" = true ]; then
    echo "Creating virtual environment with uv and Python 3.12..."
    uv venv --python=3.12
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment with uv."
        exit 1
    fi
    
    echo "Activating virtual environment..."
    source .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "Failed to activate virtual environment."
        exit 1
    fi
    
    echo "Installing cliai with uv..."
    uv pip install -e .
    if [ $? -ne 0 ]; then
        echo "Failed to install package with uv."
        exit 1
    fi
else
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment with Python 3.12..."
        python3.12 -m venv venv
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment."
            echo "Make sure venv module is installed: python3.12 -m pip install --user virtualenv"
            exit 1
        fi
        echo "Virtual environment created."
    else
        echo "Using existing virtual environment."
    fi

    echo "Activating virtual environment..."
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "Failed to activate virtual environment."
        exit 1
    fi

    # Install the package
    echo "Installing cliai..."
    pip install -e .
    if [ $? -ne 0 ]; then
        echo "Failed to install package."
        exit 1
    fi
fi

echo
echo "Installation completed successfully!"
echo

if [ "$USE_UV" = true ]; then
    echo "To use cliai:"
    echo "1. Activate the virtual environment: source .venv/bin/activate"
    echo "2. Make sure to create a .env file with your API keys (copy from .env.example)"
    echo "3. Run the application: cliai chat"
    echo
    echo "Or run directly with uvx (recommended):"
    echo "uvx --python=3.12 run cliai chat"
else
    echo "To use cliai:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Make sure to create a .env file with your API keys (copy from .env.example)"
    echo "3. Run the application: cliai chat"
fi

echo
echo "For more information, see the README.md file." 