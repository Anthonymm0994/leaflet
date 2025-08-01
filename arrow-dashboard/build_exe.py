#!/usr/bin/env python3
"""
Build script for Arrow Data Explorer
Creates a standalone executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build the standalone executable."""
    print("🔨 Building Arrow Data Explorer executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable
        "--windowed",  # No console window on Windows
        "--name=ArrowDataExplorer",
        "--add-data=requirements.txt;.",
        "--hidden-import=panel",
        "--hidden-import=plotly",
        "--hidden-import=polars",
        "--hidden-import=pyarrow",
        "--hidden-import=plotly.graph_objects",
        "--hidden-import=plotly.express",
        "--hidden-import=plotly.subplots",
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        print(f"📁 Executable location: dist/ArrowDataExplorer.exe")
        
        # Copy requirements to dist folder
        if os.path.exists("requirements.txt"):
            shutil.copy("requirements.txt", "dist/")
        
        print("\n🎉 Build Summary:")
        print("- Executable: dist/ArrowDataExplorer.exe")
        print("- Requirements: dist/requirements.txt")
        print("- Size: Check dist/ folder for file size")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True

def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["ArrowDataExplorer.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  - Removed {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  - Removed {file_name}")

def main():
    """Main build process."""
    print("🌿 Arrow Data Explorer - Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the arrow-dashboard directory.")
        return
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if build_executable():
        print("\n✅ Build process completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the executable: dist/ArrowDataExplorer.exe")
        print("2. Copy to desired location")
        print("3. Share with users (no Python installation required)")
    else:
        print("\n❌ Build process failed!")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main() 