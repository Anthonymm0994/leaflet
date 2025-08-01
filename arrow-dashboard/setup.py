#!/usr/bin/env python3
"""
Setup script for Arrow Data Explorer
Automates installation, testing, and build process.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print application header."""
    print("🌿 Arrow Data Explorer - Setup Script")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   Python 3.8+ is required")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def run_tests():
    """Run the test suite."""
    print("\n🧪 Running tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_app.py"
        ], check=True, capture_output=True, text=True)
        
        print("✅ All tests passed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def build_executable():
    """Build the standalone executable."""
    print("\n🔨 Building executable...")
    
    try:
        result = subprocess.run([
            sys.executable, "build_exe.py"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Executable built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def show_next_steps():
    """Show next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Run the application:")
    print("   - Development: python main.py")
    print("   - Windows: run.bat")
    print("   - Executable: dist/ArrowDataExplorer.exe")
    print("\n2. Open your browser to: http://localhost:8080")
    print("\n3. Upload an Arrow file to start exploring data")
    print("\n📚 Documentation: README.md")
    print("🐛 Issues: Check README.md troubleshooting section")

def main():
    """Main setup process."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found")
        print("   Please run this script from the arrow-dashboard directory")
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but continuing with setup...")
    
    # Ask about building executable
    print("\n🔨 Build Options:")
    print("1. Development mode only (faster)")
    print("2. Build standalone executable (slower, ~50-100MB)")
    
    choice = input("\nChoose option (1 or 2): ").strip()
    
    if choice == "2":
        if not build_executable():
            print("⚠️  Executable build failed, but development setup is complete")
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 