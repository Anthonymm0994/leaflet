#!/usr/bin/env python3
"""
Generate Test CSV Files for Dashboard

This script generates CSV files with various data patterns suitable for testing
the interactive dashboard. It can create realistic datasets with different
distributions and patterns.

Usage:
    python generate_test_csv.py [options]
    
Examples:
    python generate_test_csv.py --rows 1000000 --pattern normal
    python generate_test_csv.py --rows 5000000 --pattern realistic --output sales_data.csv
"""

import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate test CSV data for dashboard')
    parser.add_argument('--rows', type=int, default=100000, help='Number of rows to generate')
    parser.add_argument('--output', default='test_data.csv', help='Output CSV filename')
    parser.add_argument('--pattern', default='mixed', 
                       choices=['normal', 'skewed', 'bimodal', 'realistic', 'mixed', 'timeseries'],
                       help='Data distribution pattern')
    parser.add_argument('--categories', type=int, default=4, help='Number of categories')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    
    return parser.parse_args()

def generate_time_column(n_rows, pattern='uniform'):
    """Generate time data in HH:MM:SS format"""
    if pattern == 'uniform':
        # Uniform distribution across 24 hours
        seconds = np.random.uniform(0, 86400, n_rows)
    elif pattern == 'business_hours':
        # Peak during business hours (9-17)
        hours = np.random.choice(range(24), n_rows, 
                                p=[0.02, 0.02, 0.02, 0.02, 0.03, 0.04, 0.05, 0.06,  # 0-7
                                   0.08, 0.10, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05,  # 8-15
                                   0.04, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]) # 16-23
        minutes = np.random.randint(0, 60, n_rows)
        seconds = np.random.randint(0, 60, n_rows)
        seconds = hours * 3600 + minutes * 60 + seconds
    else:  # peaks
        # Multiple peaks throughout the day
        peak_hours = [9, 12, 15, 18, 21]
        hours = []
        for _ in range(n_rows):
            if np.random.random() < 0.7:  # 70% chance of peak time
                peak = np.random.choice(peak_hours)
                hour = np.clip(np.random.normal(peak, 1), 0, 23)
            else:
                hour = np.random.randint(0, 24)
            hours.append(int(hour))
        
        minutes = np.random.randint(0, 60, n_rows)
        secs = np.random.randint(0, 60, n_rows)
        seconds = np.array(hours) * 3600 + minutes * 60 + secs
    
    # Convert to HH:MM:SS format
    time_strings = []
    for s in seconds:
        h = int(s // 3600) % 24
        m = int((s % 3600) // 60)
        sec = int(s % 60)
        time_strings.append(f"{h:02d}:{m:02d}:{sec:02d}")
    
    return time_strings

def generate_normal_pattern(n_rows):
    """Generate data with normal distributions"""
    return {
        'time': generate_time_column(n_rows, 'uniform'),
        'width': np.random.normal(100, 20, n_rows),
        'height': np.random.normal(50, 10, n_rows),
        'angle': np.random.uniform(0, 360, n_rows),
        'strength': np.random.normal(50, 15, n_rows),
    }

def generate_skewed_pattern(n_rows):
    """Generate data with skewed distributions"""
    return {
        'time': generate_time_column(n_rows, 'business_hours'),
        'width': np.random.lognormal(4.5, 0.5, n_rows),  # Right-skewed
        'height': np.random.exponential(20, n_rows),     # Exponential decay
        'angle': np.random.beta(2, 5, n_rows) * 360,     # Left-skewed
        'strength': np.random.gamma(2, 10, n_rows),      # Gamma distribution
    }

def generate_bimodal_pattern(n_rows):
    """Generate data with bimodal distributions"""
    # Width: Two peaks
    width1 = np.random.normal(50, 10, n_rows // 2)
    width2 = np.random.normal(150, 20, n_rows - n_rows // 2)
    width = np.concatenate([width1, width2])
    np.random.shuffle(width)
    
    # Height: Three peaks
    height1 = np.random.normal(20, 5, n_rows // 3)
    height2 = np.random.normal(50, 8, n_rows // 3)
    height3 = np.random.normal(80, 10, n_rows - 2 * (n_rows // 3))
    height = np.concatenate([height1, height2, height3])
    np.random.shuffle(height)
    
    # Angle: Concentrated at cardinal directions
    angles = []
    cardinal = [0, 90, 180, 270]
    for _ in range(n_rows):
        if np.random.random() < 0.8:  # 80% near cardinal directions
            base = np.random.choice(cardinal)
            angle = (base + np.random.normal(0, 15)) % 360
        else:
            angle = np.random.uniform(0, 360)
        angles.append(angle)
    
    return {
        'time': generate_time_column(n_rows, 'peaks'),
        'width': width,
        'height': height,
        'angle': np.array(angles),
        'strength': np.abs(np.random.normal(50, 30, n_rows)),  # Half-normal
    }

def generate_realistic_pattern(n_rows):
    """Generate realistic business/sensor data patterns"""
    # Simulate daily business metrics
    
    # Time: Business hours with lunch break dip
    time_data = generate_time_column(n_rows, 'business_hours')
    
    # Width: Sales amount (log-normal with daily pattern)
    base_sales = np.random.lognormal(4, 1, n_rows)
    time_factor = []
    for t in time_data:
        h = int(t.split(':')[0])
        if 9 <= h <= 11 or 14 <= h <= 16:  # Peak hours
            factor = 1.5
        elif 12 <= h <= 13:  # Lunch dip
            factor = 0.7
        elif 6 <= h <= 20:  # Normal hours
            factor = 1.0
        else:  # Off hours
            factor = 0.3
        time_factor.append(factor)
    width = base_sales * np.array(time_factor)
    
    # Height: Quantity (correlated with sales)
    height = np.maximum(1, width / 20 + np.random.normal(0, 5, n_rows))
    
    # Angle: Direction/Department (0-360 mapped to departments)
    # Certain departments more active
    dept_weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # 5 main departments
    angles = []
    for _ in range(n_rows):
        dept = np.random.choice(5, p=dept_weights)
        angle = dept * 72 + np.random.uniform(-36, 36)  # 72 degrees per dept
        angles.append(angle % 360)
    
    # Strength: Customer satisfaction (slightly correlated with time)
    base_satisfaction = np.random.beta(7, 3, n_rows) * 100  # Skewed positive
    rush_penalty = []
    for t in time_data:
        h = int(t.split(':')[0])
        if h in [12, 13, 17, 18]:  # Rush hours
            penalty = np.random.uniform(0.8, 1.0)
        else:
            penalty = np.random.uniform(0.95, 1.05)
        rush_penalty.append(penalty)
    strength = np.clip(base_satisfaction * np.array(rush_penalty), 0, 100)
    
    return {
        'time': time_data,
        'width': width,
        'height': height,
        'angle': np.array(angles),
        'strength': strength,
    }

def generate_timeseries_pattern(n_rows):
    """Generate time series data with trends and seasonality"""
    # Create sequential time data
    seconds = np.linspace(0, 86400, n_rows)
    time_data = []
    for s in seconds:
        h = int(s // 3600) % 24
        m = int((s % 3600) // 60)
        sec = int(s % 60)
        time_data.append(f"{h:02d}:{m:02d}:{sec:02d}")
    
    # Width: Trending upward with daily seasonality
    trend = np.linspace(50, 150, n_rows)
    seasonal = 20 * np.sin(2 * np.pi * seconds / 86400)
    noise = np.random.normal(0, 10, n_rows)
    width = trend + seasonal + noise
    
    # Height: Inverse correlation with width + random walk
    random_walk = np.cumsum(np.random.normal(0, 1, n_rows))
    height = 100 - width/3 + random_walk/10
    
    # Angle: Rotating with acceleration/deceleration
    base_rotation = (seconds / 86400) * 720  # 2 full rotations
    acceleration = 50 * np.sin(4 * np.pi * seconds / 86400)
    angle = (base_rotation + acceleration) % 360
    
    # Strength: Multiple frequency components
    strength = (
        50 +
        15 * np.sin(2 * np.pi * seconds / 86400) +  # Daily
        10 * np.sin(8 * np.pi * seconds / 86400) +  # 3-hour
        5 * np.sin(24 * np.pi * seconds / 86400) +  # Hourly
        np.random.normal(0, 5, n_rows)              # Noise
    )
    
    return {
        'time': time_data,
        'width': width,
        'height': height,
        'angle': angle,
        'strength': np.clip(strength, 0, 100),
    }

def generate_mixed_pattern(n_rows):
    """Mix of all patterns for comprehensive testing"""
    n_segment = n_rows // 5
    
    # Generate each pattern for a segment
    normal = generate_normal_pattern(n_segment)
    skewed = generate_skewed_pattern(n_segment)
    bimodal = generate_bimodal_pattern(n_segment)
    realistic = generate_realistic_pattern(n_segment)
    timeseries = generate_timeseries_pattern(n_rows - 4 * n_segment)
    
    # Combine all patterns
    data = {}
    for key in ['time', 'width', 'height', 'angle', 'strength']:
        data[key] = np.concatenate([
            normal[key][:n_segment],
            skewed[key][:n_segment],
            bimodal[key][:n_segment],
            realistic[key][:n_segment],
            timeseries[key]
        ])
    
    # Shuffle to mix patterns (except time series portion)
    shuffle_idx = np.arange(4 * n_segment)
    np.random.shuffle(shuffle_idx)
    
    for key in data:
        if key != 'time':  # Preserve some time structure
            shuffled = data[key][:4 * n_segment][shuffle_idx]
            data[key] = np.concatenate([shuffled, data[key][4 * n_segment:]])
    
    return data

def generate_categories(n_rows, n_categories):
    """Generate categorical data"""
    if n_categories <= 4:
        categories = ['Category_A', 'Category_B', 'Category_C', 'Category_D'][:n_categories]
        # Uneven distribution
        weights = np.random.dirichlet(np.ones(n_categories) * 2)
    else:
        categories = [f'Category_{chr(65 + i)}' for i in range(n_categories)]
        # Power law distribution for many categories
        weights = 1 / (np.arange(1, n_categories + 1) ** 0.8)
        weights = weights / weights.sum()
    
    category_data = np.random.choice(categories, n_rows, p=weights)
    
    # Binary category
    binary_data = np.random.choice(['Active', 'Inactive'], n_rows, p=[0.65, 0.35])
    
    return category_data, binary_data

def add_correlations(data):
    """Add some realistic correlations between variables"""
    n_rows = len(data['width'])
    
    # Make height somewhat correlated with width
    correlation = 0.6
    data['height'] = (
        correlation * (data['width'] - data['width'].mean()) / data['width'].std() * 15 + 
        data['height'] * (1 - correlation) + 
        50
    )
    
    # Make strength influenced by time (fatigue effect)
    time_seconds = []
    for t in data['time']:
        h, m, s = map(int, t.split(':'))
        time_seconds.append(h * 3600 + m * 60 + s)
    time_seconds = np.array(time_seconds)
    
    fatigue = 1 - (time_seconds / 86400) * 0.2  # 20% decline over day
    data['strength'] = data['strength'] * fatigue
    
    return data

def main():
    args = parse_arguments()
    
    # Set random seed
    np.random.seed(args.seed)
    
    print(f"Generating {args.rows:,} rows with '{args.pattern}' pattern...")
    
    # Generate base data
    if args.pattern == 'normal':
        data = generate_normal_pattern(args.rows)
    elif args.pattern == 'skewed':
        data = generate_skewed_pattern(args.rows)
    elif args.pattern == 'bimodal':
        data = generate_bimodal_pattern(args.rows)
    elif args.pattern == 'realistic':
        data = generate_realistic_pattern(args.rows)
    elif args.pattern == 'timeseries':
        data = generate_timeseries_pattern(args.rows)
    else:  # mixed
        data = generate_mixed_pattern(args.rows)
    
    # Add correlations
    data = add_correlations(data)
    
    # Generate categories
    category_data, binary_data = generate_categories(args.rows, args.categories)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': data['time'],
        'width_metric': np.clip(data['width'], 0.1, None),
        'height_metric': np.clip(data['height'], 0.1, None),
        'angle_degrees': data['angle'] % 360,
        'strength_score': np.clip(data['strength'], 0, 100),
        'main_category': category_data,
        'status': binary_data
    })
    
    # Add some derived columns for richer data
    df['width_height_ratio'] = df['width_metric'] / df['height_metric']
    df['composite_score'] = (df['width_metric'] * 0.3 + 
                            df['height_metric'] * 0.3 + 
                            df['strength_score'] * 0.4)
    
    # Save to CSV
    df.to_csv(args.output, index=False)
    
    # Print summary
    file_size = os.path.getsize(args.output) / (1024 * 1024)
    print(f"\nGenerated {args.output}")
    print(f"File size: {file_size:.1f} MB")
    print(f"\nData summary:")
    print(df.describe())
    print(f"\nCategory distribution:")
    print(df['main_category'].value_counts())
    print(f"\nStatus distribution:")
    print(df['status'].value_counts())
    
    print(f"\nYou can now use this with the dashboard converter:")
    print(f"python csv_to_dashboard.py {args.output} output.html \\")
    print(f"    --time timestamp --width width_metric --height height_metric \\")
    print(f"    --angle angle_degrees --strength strength_score \\")
    print(f"    --category main_category --category2 status")

if __name__ == '__main__':
    main()