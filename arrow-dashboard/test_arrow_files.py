#!/usr/bin/env python3
"""
Comprehensive Arrow File Testing Script
Tests various Arrow file formats, sizes, and edge cases.
"""

import os
import sys
import tempfile
import time
import gc
from pathlib import Path
from typing import Dict, Any, List

import pyarrow as pa
import polars as pl
import numpy as np

def create_test_arrow_files():
    """Create various test Arrow files for comprehensive testing."""
    test_files = {}
    
    print("🔧 Creating test Arrow files...")
    
    # 1. Small dataset with mixed types
    small_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000.0, 60000.0, 70000.0, 55000.0, 65000.0],
        'department': ['HR', 'IT', 'Sales', 'HR', 'IT'],
        'active': [True, True, False, True, True]
    }
    
    test_files['small_mixed'] = create_arrow_file(small_data, "small_mixed.arrow")
    
    # 2. Large numeric dataset
    large_numeric = {
        'id': list(range(10000)),
        'value1': np.random.randn(10000),
        'value2': np.random.randint(0, 1000, 10000),
        'value3': np.random.uniform(0, 100, 10000)
    }
    
    test_files['large_numeric'] = create_arrow_file(large_numeric, "large_numeric.arrow")
    
    # 3. Dataset with null values
    null_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', None, 'Charlie', 'Diana', None],
        'age': [25, 30, None, 28, 32],
        'score': [85.5, None, 92.0, 78.5, None]
    }
    
    test_files['with_nulls'] = create_arrow_file(null_data, "with_nulls.arrow")
    
    # 4. Dataset with datetime columns
    import datetime
    datetime_data = {
        'id': list(range(100)),
        'date': [datetime.date(2023, 1, 1) + datetime.timedelta(days=i) for i in range(100)],
        'timestamp': [datetime.datetime(2023, 1, 1) + datetime.timedelta(hours=i) for i in range(100)],
        'value': np.random.randn(100)
    }
    
    test_files['datetime'] = create_arrow_file(datetime_data, "datetime.arrow")
    
    # 5. Categorical dataset
    categorical_data = {
        'id': list(range(1000)),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 1000),
        'subcategory': np.random.choice(['X', 'Y', 'Z'], 1000),
        'count': np.random.randint(1, 100, 1000)
    }
    
    test_files['categorical'] = create_arrow_file(categorical_data, "categorical.arrow")
    
    # 6. Very large dataset (stress test)
    if os.environ.get('STRESS_TEST', 'false').lower() == 'true':
        print("⚠️  Creating stress test dataset (this may take a while)...")
        stress_data = {
            'id': list(range(100000)),
            'value': np.random.randn(100000),
            'category': np.random.choice(['A', 'B', 'C'], 100000)
        }
        test_files['stress_test'] = create_arrow_file(stress_data, "stress_test.arrow")
    
    return test_files

def create_arrow_file(data: Dict[str, Any], filename: str) -> str:
    """Create an Arrow file from data dictionary."""
    try:
        # Create polars DataFrame
        df = pl.DataFrame(data)
        
        # Convert to Arrow table
        table = df.to_arrow()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.arrow', delete=False) as tmp_file:
            with pa.ipc.new_file(tmp_file.name, table.schema) as writer:
                writer.write_table(table)
            file_path = tmp_file.name
        
        # Rename to descriptive name
        new_path = os.path.join(os.path.dirname(file_path), filename)
        os.rename(file_path, new_path)
        
        print(f"✅ Created {filename} ({df.height:,} rows, {df.width} cols)")
        return new_path
        
    except Exception as e:
        print(f"❌ Failed to create {filename}: {e}")
        return None

def test_arrow_file_loading():
    """Test loading various Arrow files."""
    print("\n🧪 Testing Arrow file loading...")
    
    test_files = create_test_arrow_files()
    results = {}
    
    for test_name, file_path in test_files.items():
        if not file_path:
            continue
            
        try:
            print(f"\n📁 Testing {test_name}...")
            
            # Test pyarrow loading
            start_time = time.time()
            table = pa.ipc.open_file(file_path).read_all()
            pyarrow_time = time.time() - start_time
            
            # Test polars loading
            start_time = time.time()
            df = pl.from_arrow(table)
            polars_time = time.time() - start_time
            
            # Test basic operations
            row_count = df.height
            col_count = df.width
            memory_estimate = df.estimated_size() / (1024 * 1024)  # MB
            
            results[test_name] = {
                'success': True,
                'rows': row_count,
                'cols': col_count,
                'memory_mb': memory_estimate,
                'pyarrow_time': pyarrow_time,
                'polars_time': polars_time,
                'file_size_mb': os.path.getsize(file_path) / (1024 * 1024)
            }
            
            print(f"  ✅ Loaded: {row_count:,} rows, {col_count} cols")
            print(f"  📊 Memory: {memory_estimate:.1f} MB")
            print(f"  ⏱️  Times: pyarrow={pyarrow_time:.3f}s, polars={polars_time:.3f}s")
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results[test_name] = {'success': False, 'error': str(e)}
        
        # Clean up
        try:
            os.unlink(file_path)
        except:
            pass
    
    return results

def test_edge_cases():
    """Test edge cases and error conditions."""
    print("\n🧪 Testing edge cases...")
    
    edge_cases = []
    
    # 1. Empty dataset
    try:
        empty_df = pl.DataFrame({})
        empty_table = empty_df.to_arrow()
        with tempfile.NamedTemporaryFile(suffix='.arrow', delete=False) as tmp_file:
            with pa.ipc.new_file(tmp_file.name, empty_table.schema) as writer:
                writer.write_table(empty_table)
            edge_cases.append(('empty', tmp_file.name))
        print("✅ Empty dataset created")
    except Exception as e:
        print(f"❌ Empty dataset failed: {e}")
    
    # 2. Single column dataset
    try:
        single_col_df = pl.DataFrame({'value': [1, 2, 3]})
        single_col_table = single_col_df.to_arrow()
        with tempfile.NamedTemporaryFile(suffix='.arrow', delete=False) as tmp_file:
            with pa.ipc.new_file(tmp_file.name, single_col_table.schema) as writer:
                writer.write_table(single_col_table)
            edge_cases.append(('single_column', tmp_file.name))
        print("✅ Single column dataset created")
    except Exception as e:
        print(f"❌ Single column dataset failed: {e}")
    
    # 3. Very wide dataset
    try:
        wide_data = {f'col_{i}': list(range(10)) for i in range(100)}
        wide_df = pl.DataFrame(wide_data)
        wide_table = wide_df.to_arrow()
        with tempfile.NamedTemporaryFile(suffix='.arrow', delete=False) as tmp_file:
            with pa.ipc.new_file(tmp_file.name, wide_table.schema) as writer:
                writer.write_table(wide_table)
            edge_cases.append(('wide', tmp_file.name))
        print("✅ Wide dataset created")
    except Exception as e:
        print(f"❌ Wide dataset failed: {e}")
    
    # Test loading edge cases
    for case_name, file_path in edge_cases:
        try:
            table = pa.ipc.open_file(file_path).read_all()
            df = pl.from_arrow(table)
            print(f"✅ {case_name}: {df.height} rows, {df.width} cols")
        except Exception as e:
            print(f"❌ {case_name} loading failed: {e}")
        finally:
            try:
                os.unlink(file_path)
            except:
                pass

def test_performance_benchmarks():
    """Run performance benchmarks."""
    print("\n📊 Performance benchmarks...")
    
    # Create test data
    sizes = [1000, 10000, 100000]
    results = {}
    
    for size in sizes:
        print(f"\n🔍 Testing dataset size: {size:,}")
        
        data = {
            'id': list(range(size)),
            'value1': np.random.randn(size),
            'value2': np.random.randint(0, 1000, size),
            'category': np.random.choice(['A', 'B', 'C'], size)
        }
        
        try:
            # Create Arrow file
            file_path = create_arrow_file(data, f"benchmark_{size}.arrow")
            if not file_path:
                continue
            
            # Measure loading time
            start_time = time.time()
            table = pa.ipc.open_file(file_path).read_all()
            df = pl.from_arrow(table)
            load_time = time.time() - start_time
            
            # Measure basic operations
            start_time = time.time()
            df.select(pl.col('value1').mean()).collect()
            mean_time = time.time() - start_time
            
            start_time = time.time()
            df.group_by('category').agg(pl.col('value2').sum()).collect()
            group_time = time.time() - start_time
            
            results[size] = {
                'load_time': load_time,
                'mean_time': mean_time,
                'group_time': group_time,
                'memory_mb': df.estimated_size() / (1024 * 1024)
            }
            
            print(f"  ⏱️  Load: {load_time:.3f}s")
            print(f"  📊 Mean: {mean_time:.3f}s")
            print(f"  🔢 Group: {group_time:.3f}s")
            print(f"  💾 Memory: {results[size]['memory_mb']:.1f} MB")
            
            # Clean up
            os.unlink(file_path)
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
    
    return results

def test_memory_management():
    """Test memory management and garbage collection."""
    print("\n🧠 Memory management test...")
    
    # Create large dataset
    large_data = {
        'id': list(range(50000)),
        'value': np.random.randn(50000),
        'category': np.random.choice(['A', 'B', 'C'], 50000)
    }
    
    file_path = create_arrow_file(large_data, "memory_test.arrow")
    if not file_path:
        return
    
    try:
        # Test multiple loads
        for i in range(5):
            print(f"  🔄 Load {i+1}/5...")
            
            # Force garbage collection before load
            gc.collect()
            
            start_time = time.time()
            table = pa.ipc.open_file(file_path).read_all()
            df = pl.from_arrow(table)
            load_time = time.time() - start_time
            
            print(f"    ⏱️  Time: {load_time:.3f}s")
            print(f"    💾 Memory: {df.estimated_size() / (1024 * 1024):.1f} MB")
            
            # Clear references
            del table
            del df
            gc.collect()
            
    except Exception as e:
        print(f"  ❌ Memory test failed: {e}")
    finally:
        try:
            os.unlink(file_path)
        except:
            pass

def main():
    """Main test function."""
    print("🌿 Arrow Data Explorer - Comprehensive Arrow File Testing")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the arrow-dashboard directory.")
        return False
    
    try:
        # Test basic Arrow file loading
        loading_results = test_arrow_file_loading()
        
        # Test edge cases
        test_edge_cases()
        
        # Test performance
        performance_results = test_performance_benchmarks()
        
        # Test memory management
        test_memory_management()
        
        # Summary
        print("\n📋 Test Summary:")
        print("=" * 40)
        
        successful_tests = sum(1 for r in loading_results.values() if r.get('success', False))
        total_tests = len(loading_results)
        
        print(f"✅ Arrow file loading: {successful_tests}/{total_tests} successful")
        
        if performance_results:
            print(f"📊 Performance benchmarks: {len(performance_results)} datasets tested")
        
        print("\n🎉 All tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 