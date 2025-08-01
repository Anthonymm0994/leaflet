@echo off
echo 🔧 Starting Leaflet Arrow Explorer in Development Mode...
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start in development mode with DevTools
echo Starting in development mode with DevTools...
npm run dev

if errorlevel 1 (
    echo ❌ Failed to start in development mode
    pause
    exit /b 1
) 