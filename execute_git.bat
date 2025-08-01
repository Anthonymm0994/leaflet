@echo off
echo Removing build files...
if exist "dist" rmdir /s /q "dist"
if exist "node_modules" rmdir /s /q "node_modules"
if exist "bash.exe.stackdump" del "bash.exe.stackdump"
if exist "sh.exe.stackdump" del "sh.exe.stackdump"

echo Adding files to git...
git add .

echo Checking if this is the first commit...
git log --oneline >nul 2>&1
if %errorlevel% neq 0 (
    echo This is the first commit...
    git commit -m "first commit"
    git branch -M main
    
    echo Checking if remote origin exists...
    git remote get-url origin >nul 2>&1
    if %errorlevel% neq 0 (
        echo Adding remote origin...
        git remote add origin https://github.com/Anthonymm0994/leaflet.git
    ) else (
        echo Remote origin already exists
    )
    
    echo Pushing to GitHub...
    git push -u origin main
) else (
    echo Committing changes...
    git commit -m "Update: Clean build files and improve gitignore"
    
    echo Pushing to GitHub...
    git push
)

echo Done!
pause 