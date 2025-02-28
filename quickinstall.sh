#!/bin/bash
# Quick installation script for cliai using uv/uvx

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -sSf https://astral.sh/uv/install.sh | sh
    
    # Refresh path to include uv
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Check if uvx is available (included with uv 0.1.24+)
if uv --version | grep -q "uvx"; then
    echo "Installing cliai with uvx..."
    uvx --python=3.12 pip install -e .
    
    # Create .env from example if it doesn't exist
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        echo "Creating .env from .env.example (please edit with your API keys)"
        cp .env.example .env
    fi
    
    echo "Installation complete!"
    echo "To run cliai: uvx --python=3.12 run cliai chat"
    
else
    # Fallback to regular uv
    echo "Installing cliai with uv..."
    uv venv --python=3.12
    source .venv/bin/activate
    uv pip install -e .
    
    # Create .env from example if it doesn't exist
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        echo "Creating .env from .env.example (please edit with your API keys)"
        cp .env.example .env
    fi
    
    echo "Installation complete!"
    echo "To run cliai: source .venv/bin/activate && cliai chat"
fi 