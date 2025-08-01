@echo off
echo Committing and pushing changes...

REM Remove build files
if exist "dist" rmdir /s /q "dist"
if exist "node_modules" rmdir /s /q "node_modules"
if exist "bash.exe.stackdump" del "bash.exe.stackdump"
if exist "sh.exe.stackdump" del "sh.exe.stackdump"

REM Add all files
git add .

REM Commit
git commit -m "first commit"

REM Rename branch to main
git branch -M main

REM Add remote
git remote add origin https://github.com/Anthonymm0994/leaflet.git

REM Push
git push -u origin main

echo Done!
pause 