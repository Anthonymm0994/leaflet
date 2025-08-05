#!/usr/bin/env python3
"""
Test script for CSV to Selectable Dashboard converter

This script demonstrates the csv_to_selectable_dashboard.py functionality
by generating test data and creating dashboards.
"""

import subprocess
import os
import sys
import time

def run_command(cmd):
    """Run a command and print output"""
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def main():
    print("CSV to Selectable Dashboard Test Suite")
    print("=" * 50)
    
    # Check if required scripts exist
    if not os.path.exists('generate_test_csv.py'):
        print("Error: generate_test_csv.py not found")
        print("Make sure you're running this from the scripts directory")
        sys.exit(1)
    
    if not os.path.exists('csv_to_selectable_dashboard.py'):
        print("Error: csv_to_selectable_dashboard.py not found")
        sys.exit(1)
    
    # Test 1: Small dataset with auto-detection
    print("\n1. Testing with small dataset (auto-detection)")
    print("-" * 40)
    
    if run_command('python generate_test_csv.py --rows 10000 --pattern mixed --output test_small.csv'):
        if run_command('python csv_to_selectable_dashboard.py test_small.csv test_small_dashboard.html'):
            size = os.path.getsize('test_small_dashboard.html') / (1024 * 1024)
            print(f"✓ Created test_small_dashboard.html ({size:.1f} MB)")
    
    # Test 2: Medium dataset with explicit columns
    print("\n2. Testing with medium dataset (explicit columns)")
    print("-" * 40)
    
    if run_command('python generate_test_csv.py --rows 100000 --pattern realistic --output test_medium.csv'):
        cmd = ('python csv_to_selectable_dashboard.py test_medium.csv test_medium_dashboard.html '
               '--time timestamp --width width_metric --height height_metric '
               '--angle angle_degrees --strength strength_score '
               '--category main_category --category2 status')
        if run_command(cmd):
            size = os.path.getsize('test_medium_dashboard.html') / (1024 * 1024)
            print(f"✓ Created test_medium_dashboard.html ({size:.1f} MB)")
    
    # Test 3: Large dataset with compression
    print("\n3. Testing with large dataset (compressed)")
    print("-" * 40)
    
    if run_command('python generate_test_csv.py --rows 500000 --pattern bimodal --output test_large.csv'):
        cmd = ('python csv_to_selectable_dashboard.py test_large.csv test_large_dashboard.html '
               '--compress --time timestamp --width width_metric --height height_metric '
               '--angle angle_degrees --strength strength_score '
               '--category main_category --category2 status')
        if run_command(cmd):
            size = os.path.getsize('test_large_dashboard.html') / (1024 * 1024)
            print(f"✓ Created test_large_dashboard.html ({size:.1f} MB)")
    
    # Test 4: Edge cases
    print("\n4. Testing edge cases")
    print("-" * 40)
    
    # Create a CSV with minimal data
    import pandas as pd
    import numpy as np
    
    # Minimal dataset
    minimal_data = pd.DataFrame({
        'value': np.random.randn(100),
        'category': ['A', 'B'] * 50,
        'binary': [True, False] * 50
    })
    minimal_data.to_csv('test_minimal.csv', index=False)
    
    if run_command('python csv_to_selectable_dashboard.py test_minimal.csv test_minimal_dashboard.html'):
        print("✓ Handled minimal dataset")
    
    # Dataset with many categories (should use only first 4)
    many_cats_data = pd.DataFrame({
        'metric1': np.random.uniform(0, 100, 1000),
        'metric2': np.random.uniform(0, 200, 1000),
        'categories': np.random.choice(list('ABCDEFGHIJ'), 1000),
        'binary': np.random.choice(['Yes', 'No'], 1000)
    })
    many_cats_data.to_csv('test_many_cats.csv', index=False)
    
    if run_command('python csv_to_selectable_dashboard.py test_many_cats.csv test_many_cats_dashboard.html'):
        print("✓ Handled dataset with many categories")
    
    # Performance test
    print("\n5. Performance test")
    print("-" * 40)
    
    print("Generating 1M row dataset...")
    start_time = time.time()
    
    if run_command('python generate_test_csv.py --rows 1000000 --pattern mixed --output test_performance.csv'):
        gen_time = time.time() - start_time
        print(f"Generation time: {gen_time:.1f}s")
        
        print("\nConverting to dashboard...")
        start_time = time.time()
        
        if run_command('python csv_to_selectable_dashboard.py test_performance.csv test_performance_dashboard.html --compress'):
            conv_time = time.time() - start_time
            size = os.path.getsize('test_performance_dashboard.html') / (1024 * 1024)
            print(f"Conversion time: {conv_time:.1f}s")
            print(f"Output size: {size:.1f} MB")
            print(f"Rows per second: {1000000/conv_time:,.0f}")
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    created_files = []
    for f in os.listdir('.'):
        if f.startswith('test_') and f.endswith('.html'):
            size = os.path.getsize(f) / (1024 * 1024)
            created_files.append(f"{f} ({size:.1f} MB)")
    
    print(f"Created {len(created_files)} dashboard files:")
    for f in created_files:
        print(f"  - {f}")
    
    print("\nYou can now open any of these HTML files in your browser to test the dashboards.")
    print("\nFeatures to test:")
    print("  1. Switch between category_2 and category_4 views")
    print("  2. Click and drag on charts to filter")
    print("  3. Click category bars to select/deselect")
    print("  4. Use Mini/Mega mode to isolate data")
    print("  5. Export filtered data as CSV")
    print("  6. Take snapshots of the dashboard")
    
    # Cleanup option
    print("\nCleanup test files? (y/n): ", end='')
    if input().lower() == 'y':
        for f in os.listdir('.'):
            if f.startswith('test_') and (f.endswith('.csv') or f.endswith('.html')):
                os.remove(f)
                print(f"Removed {f}")

if __name__ == '__main__':
    main()