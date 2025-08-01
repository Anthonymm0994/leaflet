@echo off
echo 📁 Copying static files to dist directory...

REM Create dist/renderer directory if it doesn't exist
if not exist "dist\renderer" mkdir "dist\renderer"

REM Copy HTML and CSS files
copy "src\renderer\index.html" "dist\renderer\" >nul 2>&1
copy "src\renderer\styles.css" "dist\renderer\" >nul 2>&1

echo ✅ Static files copied successfully! 