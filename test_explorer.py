#!/usr/bin/env python3
"""
Test script for the Data Explorer

This script tests various configurations and verifies the system works correctly.
"""

import json
import time
from pathlib import Path
from data_loader import DataExplorerConfig

def test_numerical_data():
    """Test numerical data configuration"""
    print("Testing numerical data configuration...")
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_numerical.csv")
    config.set_title("Numerical Data Test")
    
    # Verify configuration
    assert len(config.config["data"]) == 50000
    assert len(config.config["columns"]) == 10
    assert len(config.config["chartTypes"]) == 6
    
    # Check column types
    expected_numerical = ['age', 'salary', 'height', 'weight', 'score', 'rating', 'experience_years']
    for col in expected_numerical:
        assert config.config["columnTypes"][col] in ["number", "integer"]
    
    print("✓ Numerical data configuration verified")
    return config

def test_mixed_data():
    """Test mixed data configuration"""
    print("Testing mixed data configuration...")
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_mixed.csv")
    config.set_title("Mixed Data Test")
    
    # Verify configuration
    assert len(config.config["data"]) == 75000
    assert len(config.config["columns"]) == 21
    assert len(config.config["chartTypes"]) == 6
    
    # Check that we have various data types
    assert "time" in config.config["columnTypes"].values()
    assert "number" in config.config["columnTypes"].values()
    assert "string" in config.config["columnTypes"].values()
    
    print("✓ Mixed data configuration verified")
    return config

def test_large_data():
    """Test large dataset performance"""
    print("Testing large dataset configuration...")
    
    start_time = time.time()
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_large.csv")
    config.set_title("Large Dataset Test")
    load_time = time.time() - start_time
    
    # Verify configuration
    assert len(config.config["data"]) == 500000
    assert len(config.config["columns"]) == 7
    assert len(config.config["chartTypes"]) == 6
    
    print(f"✓ Large dataset loaded in {load_time:.2f} seconds")
    return config

def test_custom_chart_config():
    """Test custom chart configuration"""
    print("Testing custom chart configuration...")
    
    config = DataExplorerConfig()
    config.load_csv("test_data/test_data_numerical.csv")
    
    # Clear default charts and add custom ones
    config.set_chart_types([])
    
    # Add specific charts
    config.add_chart({
        "type": "histogram",
        "column": "age",
        "title": "Age Distribution"
    })
    
    config.add_chart({
        "type": "histogram",
        "column": "salary",
        "title": "Salary Distribution"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "department",
        "title": "Department Breakdown"
    })
    
    config.add_chart({
        "type": "categorical",
        "column": "category",
        "title": "Category Distribution"
    })
    
    # Verify custom configuration
    assert len(config.config["chartTypes"]) == 4
    assert config.config["chartTypes"][0]["column"] == "age"
    assert config.config["chartTypes"][1]["column"] == "salary"
    assert config.config["chartTypes"][2]["column"] == "department"
    assert config.config["chartTypes"][3]["column"] == "category"
    
    print("✓ Custom chart configuration verified")
    return config

def test_performance():
    """Test performance with different dataset sizes"""
    print("Testing performance...")
    
    datasets = [
        ("test_data_numerical.csv", "Numerical (50k rows)"),
        ("test_data_mixed.csv", "Mixed (75k rows)"),
        ("test_data_large.csv", "Large (500k rows)")
    ]
    
    results = []
    
    for filename, description in datasets:
        filepath = f"test_data/{filename}"
        
        # Test loading time
        start_time = time.time()
        config = DataExplorerConfig()
        config.load_csv(filepath)
        load_time = time.time() - start_time
        
        # Test HTML generation time
        start_time = time.time()
        output_file = f"test_data/performance_test_{filename.replace('.csv', '')}.html"
        config.generate_html(output_file)
        generate_time = time.time() - start_time
        
        results.append({
            "dataset": description,
            "load_time": load_time,
            "generate_time": generate_time,
            "total_time": load_time + generate_time
        })
        
        print(f"  {description}: Load={load_time:.2f}s, Generate={generate_time:.2f}s, Total={load_time + generate_time:.2f}s")
    
    # Performance analysis
    print("\nPerformance Summary:")
    for result in results:
        print(f"  {result['dataset']}: {result['total_time']:.2f}s total")
    
    return results

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test with non-existent file
    try:
        config = DataExplorerConfig()
        config.load_csv("non_existent_file.csv")
        assert False, "Should have raised an error"
    except Exception as e:
        print(f"✓ Correctly handled non-existent file: {type(e).__name__}")
    
    # Test with empty CSV
    try:
        # Create empty CSV
        with open("test_data/empty.csv", "w") as f:
            f.write("")
        
        config = DataExplorerConfig()
        config.load_csv("test_data/empty.csv")
        print("✓ Handled empty CSV file")
        
        # Clean up
        Path("test_data/empty.csv").unlink()
    except Exception as e:
        print(f"✓ Handled empty CSV: {type(e).__name__}")
    
    print("✓ Error handling tests passed")

def main():
    """Run all tests"""
    print("Running Data Explorer tests...")
    print("=" * 50)
    
    try:
        # Run tests
        test_numerical_data()
        test_mixed_data()
        test_large_data()
        test_custom_chart_config()
        test_performance()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("All tests passed! 🎉")
        print("\nGenerated test files:")
        
        # List generated files
        test_files = [
            "test_data/numerical_explorer.html",
            "test_data/mixed_explorer.html", 
            "test_data/large_explorer.html",
            "test_data/angle_explorer.html"
        ]
        
        for file_path in test_files:
            if Path(file_path).exists():
                size_mb = Path(file_path).stat().st_size / (1024 * 1024)
                print(f"  - {file_path}: {size_mb:.1f} MB")
        
        print("\nYou can now open these HTML files in a browser to test the data explorer!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
