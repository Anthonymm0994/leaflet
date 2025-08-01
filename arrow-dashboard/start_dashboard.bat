@echo off
echo 🚀 Arrow Data Explorer - Professional Dashboard
echo ================================================
echo.
echo Starting dashboard with Windows-specific settings...
echo.

REM Set environment variables for Windows
set PANEL_WEBSOCKET_ORIGIN=localhost,127.0.0.1,0.0.0.0
set PANEL_ALLOW_WEBSOCKET_ORIGIN=localhost,127.0.0.1,0.0.0.0
set PANEL_ADDRESS=0.0.0.0
set PANEL_PORT=8080
set PANEL_SSL_VERIFY=false
set PANEL_DEV=true

REM Launch the dashboard
python launch_windows.py

pause 