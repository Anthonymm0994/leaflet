#!/usr/bin/env python3
"""
Windows-specific launcher for the Arrow Data Explorer Dashboard.
Fixes websocket connection issues on Windows.
"""

import os
import sys
import subprocess
import webbrowser
import time

def set_windows_environment():
    """Set Windows-specific environment variables."""
    # Set environment variables to fix websocket issues
    os.environ['PANEL_WEBSOCKET_ORIGIN'] = 'localhost,127.0.0.1,0.0.0.0'
    os.environ['PANEL_ALLOW_WEBSOCKET_ORIGIN'] = 'localhost,127.0.0.1,0.0.0.0'
    os.environ['PANEL_ADDRESS'] = '0.0.0.0'
    os.environ['PANEL_PORT'] = '8080'
    
    # Disable SSL verification for local development
    os.environ['PANEL_SSL_VERIFY'] = 'false'
    
    # Set Panel to development mode for better error handling
    os.environ['PANEL_DEV'] = 'true'
    
    print("✅ Windows environment configured")

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = ['pyarrow', 'polars', 'panel', 'plotly', 'numpy']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    """Launch the dashboard with Windows-specific settings."""
    print("🚀 Arrow Data Explorer - Professional Dashboard (Windows)")
    print("=" * 60)
    
    # Set Windows environment
    set_windows_environment()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ All dependencies found!")
    print("🎨 Starting beautiful dashboard...")
    print("🌐 Dashboard will open in your browser")
    print("🔧 Windows-specific settings applied")
    print("=" * 60)
    
    try:
        # Import and run the dashboard
        from main import main as run_dashboard
        run_dashboard()
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure all dependencies are installed")
        print("   2. Check if port 8080 is available")
        print("   3. Try running: pip install -r requirements.txt")
        print("   4. Try running as administrator if firewall blocks the connection")

if __name__ == "__main__":
    main() 