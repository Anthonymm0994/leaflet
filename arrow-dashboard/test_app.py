#!/usr/bin/env python3
"""
Test script for Arrow Data Explorer
Verifies basic functionality and dependencies.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import pyarrow as pa
        print("✅ pyarrow imported successfully")
    except ImportError as e:
        print(f"❌ pyarrow import failed: {e}")
        return False
    
    try:
        import polars as pl
        print("✅ polars imported successfully")
    except ImportError as e:
        print(f"❌ polars import failed: {e}")
        return False
    
    try:
        import panel as pn
        print("✅ panel imported successfully")
    except ImportError as e:
        print(f"❌ panel import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        print("✅ plotly imported successfully")
    except ImportError as e:
        print(f"❌ plotly import failed: {e}")
        return False
    
    return True

def test_arrow_file_creation():
    """Test creating a sample Arrow file."""
    print("\n🧪 Testing Arrow file creation...")
    
    try:
        import pyarrow as pa
        import polars as pl
        
        # Create sample data
        data = {
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [25, 30, 35, 28, 32],
            'salary': [50000, 60000, 70000, 55000, 65000],
            'department': ['HR', 'IT', 'Sales', 'HR', 'IT']
        }
        
        # Create polars DataFrame
        df = pl.DataFrame(data)
        
        # Convert to Arrow table
        table = df.to_arrow()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.arrow', delete=False) as tmp_file:
            with pa.ipc.new_file(tmp_file.name, table.schema) as writer:
                writer.write_table(table)
            test_file_path = tmp_file.name
        
        print(f"✅ Sample Arrow file created: {test_file_path}")
        return test_file_path
        
    except Exception as e:
        print(f"❌ Arrow file creation failed: {e}")
        return None

def test_main_application():
    """Test that the main application can be imported and initialized."""
    print("\n🧪 Testing main application...")
    
    try:
        # Import the main application
        from main import ArrowDataExplorer
        
        # Create application instance
        app = ArrowDataExplorer()
        print("✅ ArrowDataExplorer initialized successfully")
        
        # Test basic attributes
        assert hasattr(app, 'df'), "Missing df attribute"
        assert hasattr(app, 'file_path'), "Missing file_path attribute"
        assert hasattr(app, 'dashboard'), "Missing dashboard attribute"
        
        print("✅ Application attributes verified")
        return True
        
    except Exception as e:
        print(f"❌ Main application test failed: {e}")
        return False

def test_file_loading():
    """Test loading an Arrow file."""
    print("\n🧪 Testing file loading...")
    
    # Create test file
    test_file = test_arrow_file_creation()
    if not test_file:
        return False
    
    try:
        from main import ArrowDataExplorer
        
        # Create app instance
        app = ArrowDataExplorer()
        
        # Simulate file loading
        import pyarrow as pa
        table = pa.ipc.open_file(test_file).read_all()
        app.df = pl.from_arrow(table)
        app.file_path = test_file
        
        # Test data properties
        assert app.df.height == 5, f"Expected 5 rows, got {app.df.height}"
        assert app.df.width == 5, f"Expected 5 columns, got {app.df.width}"
        
        print("✅ File loading test passed")
        
        # Clean up
        os.unlink(test_file)
        return True
        
    except Exception as e:
        print(f"❌ File loading test failed: {e}")
        if test_file and os.path.exists(test_file):
            os.unlink(test_file)
        return False

def run_integration_test():
    """Run a quick integration test."""
    print("\n🧪 Running integration test...")
    
    try:
        # Test imports
        if not test_imports():
            return False
        
        # Test main application
        if not test_main_application():
            return False
        
        # Test file loading
        if not test_file_loading():
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🌿 Arrow Data Explorer - Test Suite")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the arrow-dashboard directory.")
        return False
    
    # Run integration test
    success = run_integration_test()
    
    if success:
        print("\n✅ All tests passed! The application is ready to run.")
        print("\n📋 Next steps:")
        print("1. Run: python main.py")
        print("2. Open browser to: http://localhost:8080")
        print("3. Upload an Arrow file to test the dashboard")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version (3.8+)")
        print("3. Verify all imports work")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 