@echo off
echo 🏗️ Building Leaflet Arrow Explorer Executable...
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

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "dist-build" rmdir /s /q "dist-build"

REM Build the executable
echo Building executable...
echo This will create a standalone .exe file that can be distributed.
echo.

npm run dist

if errorlevel 1 (
    echo ❌ Failed to build executable
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 📁 Executable created in: dist-build/
echo.
echo You can now distribute the .exe file to other computers.
echo.
pause 