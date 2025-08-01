#!/usr/bin/env python3
"""
Simple launcher for the Arrow Data Explorer Dashboard.
"""

import os
import sys
import subprocess
import webbrowser
import time

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
    """Launch the dashboard."""
    print("🚀 Arrow Data Explorer - Professional Dashboard")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ All dependencies found!")
    print("🎨 Starting beautiful dashboard...")
    print("🌐 Dashboard will open in your browser")
    print("=" * 50)
    
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

if __name__ == "__main__":
    main() 