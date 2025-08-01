@echo off
echo 🌿 Arrow Data Explorer
echo =====================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found. Please run this script from the arrow-dashboard directory.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import pyarrow, polars, panel, plotly" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Dependencies not found. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Run the application
echo 🚀 Starting Arrow Data Explorer...
echo 📱 The dashboard will open in your browser at http://localhost:8080
echo ⏹️  Press Ctrl+C to stop the application
echo.

python main.py

pause 