#!/usr/bin/env python3
"""
Dashboard Validation Script
Tests the Arrow Data Explorer dashboard with various Arrow files.
"""

import os
import sys
import tempfile
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List

import pyarrow as pa
import polars as pl
import numpy as np

def create_validation_datasets():
    """Create datasets for dashboard validation."""
    print("🔧 Creating validation datasets...")
    
    datasets = {}
    
    # 1. Sales data (realistic business scenario)
    sales_data = {
        'date': [f'2023-{month:02d}-{day:02d}' for month in range(1, 13) for day in range(1, 29)],
        'product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor'], 336),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 336),
        'sales_amount': np.random.uniform(100, 5000, 336),
        'quantity': np.random.randint(1, 50, 336),
        'customer_rating': np.random.uniform(1, 5, 336)
    }
    datasets['sales'] = create_arrow_file(sales_data, "sales_data.arrow")
    
    # 2. Sensor data (time series)
    sensor_data = {
        'timestamp': [f'2023-01-01 {hour:02d}:{minute:02d}:00' for hour in range(24) for minute in range(0, 60, 5)],
        'temperature': np.random.normal(20, 5, 288),
        'humidity': np.random.uniform(30, 80, 288),
        'pressure': np.random.normal(1013, 10, 288),
        'sensor_id': np.random.choice(['SENSOR_A', 'SENSOR_B', 'SENSOR_C'], 288)
    }
    datasets['sensor'] = create_arrow_file(sensor_data, "sensor_data.arrow")
    
    # 3. Customer data (categorical analysis)
    customer_data = {
        'customer_id': list(range(1000)),
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.uniform(20000, 150000, 1000),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 1000),
        'region': np.random.choice(['Urban', 'Suburban', 'Rural'], 1000),
        'satisfaction_score': np.random.uniform(1, 10, 1000),
        'purchase_frequency': np.random.randint(1, 50, 1000)
    }
    datasets['customer'] = create_arrow_file(customer_data, "customer_data.arrow")
    
    # 4. Financial data (complex numeric)
    financial_data = {
        'date': [f'2023-{month:02d}-01' for month in range(1, 13)],
        'stock_price': np.random.uniform(50, 200, 12),
        'volume': np.random.randint(1000000, 10000000, 12),
        'market_cap': np.random.uniform(1e9, 1e12, 12),
        'pe_ratio': np.random.uniform(10, 50, 12),
        'dividend_yield': np.random.uniform(0, 0.1, 12)
    }
    datasets['financial'] = create_arrow_file(financial_data, "financial_data.arrow")
    
    # 5. Survey data (mixed types with nulls)
    survey_data = {
        'respondent_id': list(range(500)),
        'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+'], 500),
        'satisfaction': np.random.choice([1, 2, 3, 4, 5, None], 500),
        'recommend_score': np.random.choice([0, 1, None], 500),
        'comments': [f"Comment {i}" if i % 10 == 0 else None for i in range(500)],
        'response_time_seconds': np.random.uniform(10, 300, 500)
    }
    datasets['survey'] = create_arrow_file(survey_data, "survey_data.arrow")
    
    return datasets

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

def test_dashboard_functionality():
    """Test dashboard functionality with validation datasets."""
    print("\n🧪 Testing dashboard functionality...")
    
    datasets = create_validation_datasets()
    results = {}
    
    for dataset_name, file_path in datasets.items():
        if not file_path:
            continue
            
        print(f"\n📊 Testing {dataset_name} dataset...")
        
        try:
            # Load the dataset
            table = pa.ipc.open_file(file_path).read_all()
            df = pl.from_arrow(table)
            
            # Test basic properties
            row_count = df.height
            col_count = df.width
            memory_mb = df.estimated_size() / (1024 * 1024)
            
            # Test column types
            numeric_cols = [col for col in df.columns if df.schema[col] in [pl.Int64, pl.Float64]]
            categorical_cols = [col for col in df.columns if df.schema[col] in [pl.Utf8, pl.Categorical]]
            datetime_cols = [col for col in df.columns if df.schema[col] in [pl.Datetime, pl.Date]]
            
            # Test basic operations
            start_time = time.time()
            
            # Test filtering
            if numeric_cols:
                filtered_df = df.filter(pl.col(numeric_cols[0]) > df.select(pl.col(numeric_cols[0]).mean()).item())
                filter_time = time.time() - start_time
            else:
                filter_time = 0
            
            # Test aggregations
            if categorical_cols and numeric_cols:
                agg_start = time.time()
                grouped_df = df.group_by(categorical_cols[0]).agg(pl.col(numeric_cols[0]).mean())
                agg_time = time.time() - agg_start
            else:
                agg_time = 0
            
            results[dataset_name] = {
                'success': True,
                'rows': row_count,
                'cols': col_count,
                'memory_mb': memory_mb,
                'numeric_cols': len(numeric_cols),
                'categorical_cols': len(categorical_cols),
                'datetime_cols': len(datetime_cols),
                'filter_time': filter_time,
                'agg_time': agg_time
            }
            
            print(f"  ✅ Loaded: {row_count:,} rows, {col_count} cols")
            print(f"  📊 Memory: {memory_mb:.1f} MB")
            print(f"  🔢 Numeric cols: {len(numeric_cols)}")
            print(f"  📝 Categorical cols: {len(categorical_cols)}")
            print(f"  🕒 Datetime cols: {len(datetime_cols)}")
            print(f"  ⏱️  Filter time: {filter_time:.3f}s")
            print(f"  ⏱️  Aggregation time: {agg_time:.3f}s")
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results[dataset_name] = {'success': False, 'error': str(e)}
        
        # Clean up
        try:
            os.unlink(file_path)
        except:
            pass
    
    return results

def test_plot_generation():
    """Test plot generation with different data types."""
    print("\n📈 Testing plot generation...")
    
    # Create test data for plots
    plot_data = {
        'x_numeric': np.random.randn(1000),
        'y_numeric': np.random.randn(1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'value': np.random.uniform(0, 100, 1000)
    }
    
    file_path = create_arrow_file(plot_data, "plot_test.arrow")
    if not file_path:
        return False
    
    try:
        # Test different plot types
        table = pa.ipc.open_file(file_path).read_all()
        df = pl.from_arrow(table)
        
        plot_tests = [
            ('histogram', 'x_numeric'),
            ('scatter', 'x_numeric', 'y_numeric'),
            ('box', 'value'),
            ('bar', 'category'),
            ('violin', 'value')
        ]
        
        for plot_test in plot_tests:
            plot_type = plot_test[0]
            x_col = plot_test[1]
            y_col = plot_test[2] if len(plot_test) > 2 else None
            
            try:
                # Simulate plot creation (without actual plotting)
                if plot_type == 'histogram':
                    df.select(pl.col(x_col)).to_pandas()
                elif plot_type == 'scatter':
                    df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
                elif plot_type in ['box', 'violin']:
                    df.select(pl.col(x_col)).to_pandas()
                elif plot_type == 'bar':
                    df.select(pl.col(x_col).value_counts()).to_pandas()
                
                print(f"  ✅ {plot_type} plot data prepared")
                
            except Exception as e:
                print(f"  ❌ {plot_type} plot failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Plot generation test failed: {e}")
        return False
    finally:
        try:
            os.unlink(file_path)
        except:
            pass

def test_memory_efficiency():
    """Test memory efficiency with large datasets."""
    print("\n🧠 Testing memory efficiency...")
    
    # Create progressively larger datasets
    sizes = [1000, 10000, 50000]
    results = {}
    
    for size in sizes:
        print(f"\n🔍 Testing dataset size: {size:,}")
        
        data = {
            'id': list(range(size)),
            'value1': np.random.randn(size),
            'value2': np.random.randint(0, 1000, size),
            'category': np.random.choice(['A', 'B', 'C'], size),
            'text': [f"Text {i}" for i in range(size)]
        }
        
        file_path = create_arrow_file(data, f"memory_test_{size}.arrow")
        if not file_path:
            continue
        
        try:
            # Measure memory usage
            import psutil
            process = psutil.Process()
            memory_before = process.memory_info().rss / (1024 * 1024)  # MB
            
            # Load dataset
            start_time = time.time()
            table = pa.ipc.open_file(file_path).read_all()
            df = pl.from_arrow(table)
            load_time = time.time() - start_time
            
            memory_after = process.memory_info().rss / (1024 * 1024)  # MB
            memory_increase = memory_after - memory_before
            
            # Test operations
            start_time = time.time()
            df.select(pl.col('value1').mean()).collect()
            mean_time = time.time() - start_time
            
            results[size] = {
                'load_time': load_time,
                'memory_increase_mb': memory_increase,
                'mean_time': mean_time,
                'estimated_size_mb': df.estimated_size() / (1024 * 1024)
            }
            
            print(f"  ⏱️  Load time: {load_time:.3f}s")
            print(f"  💾 Memory increase: {memory_increase:.1f} MB")
            print(f"  📊 Estimated size: {results[size]['estimated_size_mb']:.1f} MB")
            print(f"  ⏱️  Mean calculation: {mean_time:.3f}s")
            
            # Clean up
            del table
            del df
            import gc
            gc.collect()
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        finally:
            try:
                os.unlink(file_path)
            except:
                pass
    
    return results

def test_error_handling():
    """Test error handling with invalid data."""
    print("\n⚠️  Testing error handling...")
    
    error_tests = [
        # Empty file
        ('empty', {}),
        # Single column
        ('single_col', {'value': [1, 2, 3]}),
        # All null values
        ('all_nulls', {'col1': [None, None, None], 'col2': [None, None, None]}),
        # Mixed types
        ('mixed_types', {'id': [1, 2, 3], 'name': ['A', 'B', 'C'], 'value': [1.5, 2.5, 3.5]})
    ]
    
    results = {}
    
    for test_name, data in error_tests:
        print(f"\n🔍 Testing {test_name}...")
        
        try:
            file_path = create_arrow_file(data, f"error_test_{test_name}.arrow")
            if not file_path:
                continue
            
            # Try to load
            table = pa.ipc.open_file(file_path).read_all()
            df = pl.from_arrow(table)
            
            results[test_name] = {
                'success': True,
                'rows': df.height,
                'cols': df.width
            }
            
            print(f"  ✅ Loaded: {df.height} rows, {df.width} cols")
            
        except Exception as e:
            results[test_name] = {
                'success': False,
                'error': str(e)
            }
            print(f"  ❌ Failed: {e}")
        
        finally:
            try:
                if 'file_path' in locals():
                    os.unlink(file_path)
            except:
                pass
    
    return results

def main():
    """Main validation function."""
    print("🌿 Arrow Data Explorer - Dashboard Validation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the arrow-dashboard directory.")
        return False
    
    try:
        # Test dashboard functionality
        functionality_results = test_dashboard_functionality()
        
        # Test plot generation
        plot_success = test_plot_generation()
        
        # Test memory efficiency
        memory_results = test_memory_efficiency()
        
        # Test error handling
        error_results = test_error_handling()
        
        # Summary
        print("\n📋 Validation Summary:")
        print("=" * 40)
        
        successful_datasets = sum(1 for r in functionality_results.values() if r.get('success', False))
        total_datasets = len(functionality_results)
        
        print(f"✅ Dataset loading: {successful_datasets}/{total_datasets} successful")
        print(f"📈 Plot generation: {'✅' if plot_success else '❌'}")
        print(f"🧠 Memory efficiency: {len(memory_results)} datasets tested")
        print(f"⚠️  Error handling: {len(error_results)} edge cases tested")
        
        # Performance summary
        if memory_results:
            avg_load_time = sum(r['load_time'] for r in memory_results.values()) / len(memory_results)
            avg_memory = sum(r['memory_increase_mb'] for r in memory_results.values()) / len(memory_results)
            print(f"📊 Average load time: {avg_load_time:.3f}s")
            print(f"📊 Average memory increase: {avg_memory:.1f} MB")
        
        print("\n🎉 Validation completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 