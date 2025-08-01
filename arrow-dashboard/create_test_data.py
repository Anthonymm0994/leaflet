#!/usr/bin/env python3
"""
Create test Arrow files for the dashboard demonstration.
"""

import pyarrow as pa
import polars as pl
import numpy as np
from datetime import datetime, timedelta

def create_sales_data():
    """Create sample sales data."""
    np.random.seed(42)
    
    # Generate sample data
    n_rows = 1000
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
    
    # Generate data
    data = {
        'id': list(range(1, n_rows + 1)),
        'product_name': [f'Product_{i}' for i in range(1, n_rows + 1)],
        'category': np.random.choice(categories, n_rows),
        'price': np.random.uniform(10, 500, n_rows).round(2),
        'quantity': np.random.randint(1, 50, n_rows),
        'revenue': np.random.uniform(100, 5000, n_rows).round(2),
        'rating': np.random.uniform(1, 5, n_rows).round(1),
        'customer_id': np.random.randint(1, 200, n_rows),
        'date': [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)]
    }
    
    # Create Polars DataFrame
    df = pl.DataFrame(data)
    
    # Save as Arrow file
    df.write_ipc('sales_data.arrow')
    print(f"✅ Created sales_data.arrow with {len(df)} rows")
    
    return df

def create_sensor_data():
    """Create sample sensor data."""
    np.random.seed(42)
    
    # Generate sample data
    n_rows = 2000
    
    # Generate time series data
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(n_rows)]
    
    data = {
        'timestamp': timestamps,
        'temperature': np.random.normal(25, 5, n_rows).round(2),
        'humidity': np.random.uniform(30, 80, n_rows).round(2),
        'pressure': np.random.normal(1013, 10, n_rows).round(2),
        'voltage': np.random.uniform(3.0, 5.0, n_rows).round(3),
        'current': np.random.uniform(0.1, 2.0, n_rows).round(3),
        'sensor_id': np.random.randint(1, 11, n_rows),
        'status': np.random.choice(['active', 'inactive', 'error'], n_rows)
    }
    
    # Create Polars DataFrame
    df = pl.DataFrame(data)
    
    # Save as Arrow file
    df.write_ipc('sensor_data.arrow')
    print(f"✅ Created sensor_data.arrow with {len(df)} rows")
    
    return df

def create_customer_data():
    """Create sample customer data."""
    np.random.seed(42)
    
    # Generate sample data
    n_rows = 500
    
    # Customer data
    names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    data = {
        'customer_id': list(range(1, n_rows + 1)),
        'name': np.random.choice(names, n_rows),
        'age': np.random.randint(18, 80, n_rows),
        'city': np.random.choice(cities, n_rows),
        'income': np.random.uniform(30000, 150000, n_rows).round(0),
        'spending_score': np.random.randint(1, 100, n_rows),
        'loyalty_years': np.random.uniform(0, 10, n_rows).round(1),
        'is_premium': np.random.choice([True, False], n_rows, p=[0.3, 0.7])
    }
    
    # Create Polars DataFrame
    df = pl.DataFrame(data)
    
    # Save as Arrow file
    df.write_ipc('customer_data.arrow')
    print(f"✅ Created customer_data.arrow with {len(df)} rows")
    
    return df

def main():
    """Create all test data files."""
    print("🚀 Creating test Arrow files for dashboard demonstration...")
    print("=" * 60)
    
    try:
        # Create different types of test data
        sales_df = create_sales_data()
        sensor_df = create_sensor_data()
        customer_df = create_customer_data()
        
        print("\n📊 Test Data Summary:")
        print(f"Sales Data: {len(sales_df)} rows, {len(sales_df.columns)} columns")
        print(f"Sensor Data: {len(sensor_df)} rows, {len(sensor_df.columns)} columns")
        print(f"Customer Data: {len(customer_df)} rows, {len(customer_df.columns)} columns")
        
        print("\n🎯 Files created:")
        print("   - sales_data.arrow (Product sales data)")
        print("   - sensor_data.arrow (IoT sensor readings)")
        print("   - customer_data.arrow (Customer profiles)")
        
        print("\n✅ All test files created successfully!")
        print("📁 You can now upload these files to the dashboard")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")

if __name__ == "__main__":
    main() 