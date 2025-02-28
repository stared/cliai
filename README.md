# CLI AI Chat

A command-line interface for chatting with various AI models including OpenAI GPT, Anthropic Claude, and Google Gemini.

## Features

- Chat with multiple AI models from a single interface
- Support for:
  - OpenAI models (gpt-4.5-preview-2025-02-27, gpt-4o-2024-08-06)
  - Anthropic models (claude-3-7-sonnet-20250219, claude-3-5-sonnet-20241022)
  - Google Gemini models
- Clean terminal UI with Rich
- History tracking for conversations
- Easy model switching

## Requirements

- **Python 3.12+** (This is a strict requirement - the app uses features from Python 3.12)

## Installation with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast, reliable Python package installer and resolver, with built-in Python version management through uvx.

### 1. Install uv

```bash
# Install uv (Unix/macOS)
curl -sSf https://astral.sh/uv/install.sh | sh

# Install uv (Windows PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

### 2. Clone the repository

```bash
git clone https://github.com/yourusername/cliai.git
cd cliai
```

### 3. Install with the correct Python version

```bash
# Create a virtual environment with Python 3.12 and install the package
uv venv --python=3.12

# Activate the virtual environment
# On Unix/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install the package in development mode
uv pip install -e .
```

If you have [uvx](https://github.com/astral-sh/uv/blob/main/crates/uv-x/README.md) installed (included with uv 0.1.24+), you can simplify the workflow:

```bash
# Create a venv, download Python 3.12 if needed, and install the package
uvx --python=3.12 pip install -e .

# Run the app directly with the correct Python version
uvx --python=3.12 run cliai chat
```

## Alternative Installation Methods

### With pip

```bash
# Ensure you have Python 3.12+
python --version

# Install in development mode
pip install -e .
```

## Environment Variables

Create a `.env` file in your project directory with your API keys:

```bash
# Copy the example file
cp .env.example .env

# Edit with your preferred editor
```

Required environment variables:

```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

## Usage

```bash
# List available models
cliai models

# Start a chat session
cliai chat

# Start with a specific model
cliai chat --model gpt-4o-2024-08-06

# Start with a custom system message
cliai chat --system "You are a helpful expert in Python programming."
```

### Running with uvx

The best way to run the app is with uvx, which ensures the correct Python version:

```bash
uvx --python=3.12 run cliai chat
```

## Troubleshooting

If you see an error like `Package 'cliai' requires a different Python: X.X.X not in '>=3.12'`:

1. **Using uv (recommended):**

   ```bash
   uvx --python=3.12 run cliai chat
   ```

2. **Using other tools:**
   - Make sure you're using Python 3.12 or newer
   - Consider using a tool like pyenv or asdf to manage Python versions
