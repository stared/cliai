@echo off
REM Installation script for cliai on Windows

echo CLI AI Chat Installation Script
echo ==============================
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo uv found, using uv for installation (recommended)
    set USE_UV=true
) else (
    echo uv not found, using traditional pip/venv
    echo Consider installing uv for better dependency management:
    echo irm https://astral.sh/uv/install.ps1 ^| iex
    echo.
    set USE_UV=false
)

REM Check for Python
if "%USE_UV%"=="true" (
    echo Checking for Python using uv...
    REM uv will handle Python version management
) else (
    echo Checking for Python...
    where python >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Python is not found in your PATH.
        echo You need Python 3.12 or newer to use this application.
        echo.
        echo Installation options:
        echo 1. Download from https://www.python.org/downloads/
        echo 2. Make sure to check "Add Python to PATH" during installation
        echo 3. Install uv: irm https://astral.sh/uv/install.ps1 ^| iex
        echo.
        echo After installing Python 3.12 or uv, run this script again.
        exit /b 1
    )

    REM Check Python version
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
    echo Found Python %PYVER%

    REM Extract major and minor version
    for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
        set PYMAJOR=%%a
        set PYMINOR=%%b
    )

    REM Check if Python version is at least 3.12
    if %PYMAJOR% LSS 3 (
        echo Python 3.12 or newer is required. You have Python %PYMAJOR%.%PYMINOR%
        exit /b 1
    )
    if %PYMAJOR% EQU 3 (
        if %PYMINOR% LSS 12 (
            echo Python 3.12 or newer is required. You have Python %PYMAJOR%.%PYMINOR%
            exit /b 1
        )
    )
)

echo.

REM Create and set up environment
if "%USE_UV%"=="true" (
    echo Creating virtual environment with uv and Python 3.12...
    uv venv --python=3.12
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment with uv.
        exit /b 1
    )
    
    echo Activating virtual environment...
    call .venv\Scripts\activate
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to activate virtual environment.
        exit /b 1
    )
    
    echo Installing cliai with uv...
    uv pip install -e .
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install package with uv.
        exit /b 1
    )
) else (
    REM Create virtual environment if it doesn't exist
    if not exist venv (
        echo Creating virtual environment with Python 3.12+...
        python -m venv venv
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to create virtual environment.
            echo Make sure venv module is installed: python -m pip install --user virtualenv
            exit /b 1
        )
        echo Virtual environment created.
    ) else (
        echo Using existing virtual environment.
    )

    echo Activating virtual environment...
    call venv\Scripts\activate
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to activate virtual environment.
        exit /b 1
    )

    REM Install the package
    echo Installing cliai...
    pip install -e .
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install package.
        exit /b 1
    )
)

echo.
echo Installation completed successfully!
echo.

if "%USE_UV%"=="true" (
    echo To use cliai:
    echo 1. Activate the virtual environment: .venv\Scripts\activate
    echo 2. Make sure to create a .env file with your API keys (copy from .env.example)
    echo 3. Run the application: cliai chat
    echo.
    echo Or run directly with uvx (recommended):
    echo uvx --python=3.12 run cliai chat
) else (
    echo To use cliai:
    echo 1. Activate the virtual environment: venv\Scripts\activate
    echo 2. Make sure to create a .env file with your API keys (copy from .env.example)
    echo 3. Run the application: cliai chat
)

echo.
echo For more information, see the README.md file. 