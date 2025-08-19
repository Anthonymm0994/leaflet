#!/usr/bin/env python3
"""
Generate test datasets for the Data Explorer

This script creates various CSV files with fake data to test
different chart types and data characteristics.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import datetime, timedelta

def generate_numerical_dataset():
    """Generate a dataset with various numerical columns"""
    np.random.seed(42)
    n_rows = 50000
    
    data = {
        'id': range(1, n_rows + 1),
        'age': np.random.normal(35, 12, n_rows).astype(int),
        'salary': np.random.lognormal(10.5, 0.4, n_rows).astype(int),
        'height': np.random.normal(170, 10, n_rows),
        'weight': np.random.normal(70, 15, n_rows),
        'score': np.random.uniform(0, 100, n_rows),
        'rating': np.random.choice([1, 2, 3, 4, 5], n_rows, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_rows, p=[0.3, 0.25, 0.25, 0.2]),
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], n_rows),
        'experience_years': np.random.exponential(5, n_rows).astype(int)
    }
    
    # Clean up negative values
    data['age'] = np.abs(data['age'])
    data['height'] = np.abs(data['height'])
    data['weight'] = np.abs(data['weight'])
    data['experience_years'] = np.clip(data['experience_years'], 0, 30)
    
    df = pd.DataFrame(data)
    df.to_csv('test_data_numerical.csv', index=False)
    print(f"Generated numerical dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def generate_time_dataset():
    """Generate a dataset with time-based data"""
    np.random.seed(42)
    n_rows = 30000
    
    # Generate base datetime
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(n_rows)]
    
    # Generate time data
    times = []
    for _ in range(n_rows):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        times.append(time_str)
    
    data = {
        'id': range(1, n_rows + 1),
        'date': [d.strftime('%Y-%m-%d') for d in dates],
        'time': times,
        'hour': [int(t.split(':')[0]) for t in times],
        'minute': [int(t.split(':')[1]) for t in times],
        'duration_minutes': np.random.exponential(30, n_rows).astype(int),
        'wait_time': np.random.poisson(15, n_rows),
        'session_length': np.random.normal(45, 20, n_rows).astype(int),
        'category': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], n_rows),
        'day_of_week': [d.strftime('%A') for d in dates],
        'month': [d.strftime('%B') for d in dates]
    }
    
    # Clean up negative values
    data['duration_minutes'] = np.clip(data['duration_minutes'], 1, 300)
    data['session_length'] = np.clip(data['session_length'], 1, 120)
    
    df = pd.DataFrame(data)
    df.to_csv('test_data_time.csv', index=False)
    print(f"Generated time dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def generate_categorical_dataset():
    """Generate a dataset with categorical data"""
    np.random.seed(42)
    n_rows = 40000
    
    # Generate categorical data with various cardinalities
    data = {
        'id': range(1, n_rows + 1),
        'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia'], n_rows),
        'city': np.random.choice(['New York', 'London', 'Tokyo', 'Paris', 'Berlin', 'Toronto', 'Sydney'], n_rows),
        'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Education', 'Retail', 'Manufacturing'], n_rows),
        'job_title': np.random.choice(['Engineer', 'Manager', 'Analyst', 'Designer', 'Developer', 'Consultant'], n_rows),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_rows),
        'marital_status': np.random.choice(['Single', 'Married', 'Divorced', 'Widowed'], n_rows),
        'blood_type': np.random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], n_rows),
        'favorite_color': np.random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink'], n_rows),
        'preferred_language': np.random.choice(['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese'], n_rows),
        'subscription_type': np.random.choice(['Free', 'Basic', 'Premium', 'Enterprise'], n_rows)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('test_data_categorical.csv', index=False)
    print(f"Generated categorical dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def generate_mixed_dataset():
    """Generate a comprehensive dataset with mixed data types"""
    np.random.seed(42)
    n_rows = 75000
    
    # Generate base datetime
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(n_rows)]
    
    # Generate time data
    times = []
    for _ in range(n_rows):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        times.append(time_str)
    
    data = {
        'id': range(1, n_rows + 1),
        'customer_name': [f"Customer_{i:05d}" for i in range(1, n_rows + 1)],
        'age': np.random.normal(35, 12, n_rows).astype(int),
        'income': np.random.lognormal(10.5, 0.4, n_rows).astype(int),
        'purchase_amount': np.random.exponential(50, n_rows),
        'visit_date': [d.strftime('%Y-%m-%d') for d in dates],
        'visit_time': times,
        'store_location': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_rows),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Food', 'Home'], n_rows),
        'customer_type': np.random.choice(['New', 'Returning', 'VIP', 'Premium'], n_rows),
        'satisfaction_score': np.random.choice([1, 2, 3, 4, 5], n_rows, p=[0.05, 0.1, 0.2, 0.4, 0.25]),
        'days_since_last_visit': np.random.poisson(30, n_rows),
        'total_purchases': np.random.poisson(15, n_rows),
        'average_order_value': np.random.normal(75, 25, n_rows),
        'preferred_payment': np.random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet'], n_rows),
        'loyalty_points': np.random.poisson(500, n_rows),
        'marketing_emails_opened': np.random.binomial(10, 0.3, n_rows),
        'website_visits': np.random.poisson(8, n_rows),
        'mobile_app_usage': np.random.choice(['High', 'Medium', 'Low', 'None'], n_rows),
        'season': [d.strftime('%B') for d in dates],
        'weekend_visit': [d.weekday() >= 5 for d in dates]
    }
    
    # Clean up negative values
    data['age'] = np.abs(data['age'])
    data['income'] = np.abs(data['income'])
    data['purchase_amount'] = np.abs(data['purchase_amount'])
    data['average_order_value'] = np.abs(data['average_order_value'])
    
    df = pd.DataFrame(data)
    df.to_csv('test_data_mixed.csv', index=False)
    print(f"Generated mixed dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def generate_large_dataset():
    """Generate a very large dataset to test performance"""
    np.random.seed(42)
    n_rows = 500000  # 500k rows
    
    data = {
        'id': range(1, n_rows + 1),
        'value': np.random.normal(100, 25, n_rows),
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n_rows),
        'score': np.random.uniform(0, 1000, n_rows),
        'timestamp': [f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}" for _ in range(n_rows)],
        'group': np.random.choice(['Group1', 'Group2', 'Group3', 'Group4', 'Group5'], n_rows),
        'status': np.random.choice(['Active', 'Inactive', 'Pending', 'Completed'], n_rows)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('test_data_large.csv', index=False)
    print(f"Generated large dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def generate_angle_dataset():
    """Generate a dataset with angular data for testing angle charts"""
    np.random.seed(42)
    n_rows = 25000
    
    # Generate angles in degrees (0-360)
    angles = np.random.uniform(0, 360, n_rows)
    
    data = {
        'id': range(1, n_rows + 1),
        'angle_degrees': angles,
        'angle_radians': np.radians(angles),
        'wind_direction': [f"{int(angle)}°" for angle in angles],
        'compass_direction': [get_compass_direction(angle) for angle in angles],
        'wind_speed': np.random.exponential(10, n_rows),
        'temperature': np.random.normal(20, 10, n_rows),
        'humidity': np.random.uniform(30, 90, n_rows),
        'pressure': np.random.normal(1013, 20, n_rows),
        'season': np.random.choice(['Spring', 'Summer', 'Fall', 'Winter'], n_rows),
        'time_of_day': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], n_rows)
    }
    
    # Clean up values
    data['wind_speed'] = np.clip(data['wind_speed'], 0, 100)
    data['temperature'] = np.clip(data['temperature'], -20, 50)
    data['humidity'] = np.clip(data['humidity'], 0, 100)
    data['pressure'] = np.clip(data['pressure'], 950, 1070)
    
    df = pd.DataFrame(data)
    df.to_csv('test_data_angle.csv', index=False)
    print(f"Generated angle dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def get_compass_direction(angle):
    """Convert angle to compass direction"""
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = int((angle + 11.25) / 22.5) % 16
    return directions[index]

def main():
    """Generate all test datasets"""
    print("Generating test datasets for Data Explorer...")
    print("=" * 50)
    
    # Create test data directory
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    # Change to test data directory
    import os
    os.chdir(test_dir)
    
    try:
        # Generate various datasets
        generate_numerical_dataset()
        generate_time_dataset()
        generate_categorical_dataset()
        generate_mixed_dataset()
        generate_large_dataset()
        generate_angle_dataset()
        
        print("\n" + "=" * 50)
        print("All test datasets generated successfully!")
        print("\nFiles created:")
        for file in Path(".").glob("*.csv"):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  - {file.name}: {size_mb:.1f} MB")
        
        print(f"\nTest data directory: {test_dir.absolute()}")
        print("\nYou can now test the data explorer with:")
        print("  python ../data_loader.py test_data_numerical.csv --title 'Numerical Data Test'")
        print("  python ../data_loader.py test_data_mixed.csv --title 'Mixed Data Test'")
        print("  python ../data_loader.py test_data_large.csv --title 'Large Dataset Test'")
        
    except Exception as e:
        print(f"Error generating test data: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
