@echo off
echo 🧪 Testing Leaflet Arrow Explorer...
echo.

REM Build the application
echo Building application...
npm run build
if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo ✅ Build successful!
echo.
echo 🚀 Starting application...
echo.
echo The application should now open with:
echo - Dark mode interface
echo - Auto-loaded test data
echo - Beautiful visualizations
echo.
echo Press Ctrl+C to stop the application
echo.

npm start 