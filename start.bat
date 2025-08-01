@echo off
echo 🌿 Starting Leaflet Arrow Explorer...
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

REM Build and start the application
echo Building and starting the application...
echo.
echo You should see:
echo - Loading bar with progress updates
echo - Main interface with file selection
echo - Dark theme with professional styling
echo.
echo If the app gets stuck, check the console for errors.
echo.

npm start

if errorlevel 1 (
    echo ❌ Failed to start the application
    pause
    exit /b 1
) 