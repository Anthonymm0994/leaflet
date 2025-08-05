#!/usr/bin/env python3
"""Test the CSV to dashboard conversion with a sample dataset"""

import os
import subprocess
import pandas as pd
import numpy as np

def create_test_csv(filename='test_data.csv', rows=100000):
    """Create a test CSV with specified number of rows"""
    print(f"Creating {filename} with {rows:,} rows...")
    
    np.random.seed(42)
    
    # Generate varied data
    data = {
        'timestamp': [f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}:{np.random.randint(0,60):02d}" 
                     for _ in range(rows)],
        'width': np.random.normal(100, 20, rows),
        'height': np.random.exponential(2, rows),
        'angle': np.random.uniform(0, 360, rows),
        'strength': np.random.gamma(2, 2, rows) * 10,
        'category': np.random.choice(['Category_A', 'Category_B', 'Category_C', 'Category_D'], rows, p=[0.4, 0.3, 0.2, 0.1]),
        'active': np.random.choice(['Yes', 'No'], rows, p=[0.7, 0.3])
    }
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)
    print(f"Created {filename} ({file_size:.1f} MB)")
    return filename

def test_conversion(csv_file, output_file='test_dashboard.html'):
    """Test the CSV to dashboard conversion"""
    cmd = [
        'python', 'csv_to_dashboard.py',
        csv_file, output_file,
        '--time', 'timestamp',
        '--width', 'width',
        '--height', 'height',
        '--angle', 'angle',
        '--strength', 'strength',
        '--category', 'category',
        '--category2', 'active',
        '--compress'
    ]
    
    print(f"\nConverting {csv_file} to {output_file}...")
    print("Command:", ' '.join(cmd))
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    print(result.stdout)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\nGenerated {output_file} ({size:.1f} MB)")
        print(f"Open {output_file} in your browser to view the dashboard")
    
    return True

def main():
    """Run the test"""
    print("CSV to Dashboard Test")
    print("=" * 50)
    
    # Change to scripts directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create test data
    csv_file = create_test_csv('test_data_100k.csv', 100000)
    
    # Convert to dashboard
    if test_conversion(csv_file, 'test_dashboard_100k.html'):
        print("\n✓ Test successful!")
        print("\nYou can now use the script with your own CSV files:")
        print("python csv_to_dashboard.py your_data.csv output.html --time ... --width ... etc.")
    else:
        print("\n✗ Test failed")
    
    # Clean up CSV file
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"\nCleaned up {csv_file}")

if __name__ == '__main__':
    main()