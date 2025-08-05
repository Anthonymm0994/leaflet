#!/usr/bin/env python3
"""
CSV to Selectable Category Dashboard Converter

This script converts any CSV file into an interactive HTML dashboard with selectable
category distributions (switch between 2-category and 4-category views).

Based on the selectable_category_dashboard.html template.
"""

import argparse
import pandas as pd
import numpy as np
import base64
import os
import sys
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Convert CSV to interactive dashboard with selectable categories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with automatic column detection
  python csv_to_selectable_dashboard.py data.csv output.html

  # Specify column mappings
  python csv_to_selectable_dashboard.py data.csv output.html \\
      --time timestamp --width sales --height quantity \\
      --angle direction --strength score \\
      --category department --category2 status

  # Compress output
  python csv_to_selectable_dashboard.py data.csv output.html --compress
        """
    )
    
    parser.add_argument('input_csv', help='Input CSV file path')
    parser.add_argument('output_html', help='Output HTML file path')
    
    # Column mapping arguments
    parser.add_argument('--time', help='Column name for time data (HH:MM:SS format)')
    parser.add_argument('--width', help='Column name for width metric')
    parser.add_argument('--height', help='Column name for height metric')
    parser.add_argument('--angle', help='Column name for angle data (0-360 degrees)')
    parser.add_argument('--strength', help='Column name for strength metric')
    parser.add_argument('--category', help='Column name for main category (up to 4 unique values)')
    parser.add_argument('--category2', help='Column name for binary category')
    
    parser.add_argument('--compress', action='store_true', help='Compress the output HTML')
    parser.add_argument('--sample', type=int, help='Sample N rows from the CSV (for testing)')
    
    return parser.parse_args()

def detect_columns(df):
    """Auto-detect appropriate columns based on data characteristics"""
    detected = {}
    
    for col in df.columns:
        if col in detected.values():
            continue
            
        sample = df[col].dropna().head(1000)
        
        # Skip if too few values
        if len(sample) < 10:
            continue
        
        # Check for time format (HH:MM:SS)
        if df[col].dtype == 'object':
            try:
                # Check if it matches time pattern
                time_pattern = sample.astype(str).str.match(r'^\d{1,2}:\d{2}:\d{2}')
                if time_pattern.mean() > 0.9:
                    detected['time'] = col
                    continue
            except:
                pass
        
        # Check for numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            col_min = sample.min()
            col_max = sample.max()
            col_mean = sample.mean()
            
            # Angle detection (0-360 range)
            if not detected.get('angle') and col_min >= 0 and col_max <= 360:
                detected['angle'] = col
            # Strength detection (0-100 range typical)
            elif not detected.get('strength') and col_min >= 0 and col_max <= 100:
                detected['strength'] = col
            # Width/Height detection (positive values)
            elif col_min >= 0:
                if not detected.get('width'):
                    detected['width'] = col
                elif not detected.get('height'):
                    detected['height'] = col
        
        # Check for categorical columns
        elif df[col].dtype == 'object' or df[col].dtype.name == 'category':
            unique_values = df[col].nunique()
            
            # Binary category
            if not detected.get('category2') and unique_values == 2:
                detected['category2'] = col
            # Main category (up to 4 values)
            elif not detected.get('category') and unique_values <= 4:
                detected['category'] = col
    
    return detected

def prepare_data(df, args):
    """Prepare data arrays for embedding"""
    print(f"Preparing {len(df):,} rows of data...")
    
    # Auto-detect columns if not specified
    detected = detect_columns(df)
    
    # Use specified columns or fall back to detected ones
    time_col = args.time or detected.get('time')
    width_col = args.width or detected.get('width')
    height_col = args.height or detected.get('height')
    angle_col = args.angle or detected.get('angle')
    strength_col = args.strength or detected.get('strength')
    category_col = args.category or detected.get('category')
    category2_col = args.category2 or detected.get('category2')
    
    print("\nColumn mappings:")
    print(f"  Time: {time_col or 'Not found - will generate random'}")
    print(f"  Width: {width_col or 'Not found - will generate random'}")
    print(f"  Height: {height_col or 'Not found - will generate random'}")
    print(f"  Angle: {angle_col or 'Not found - will generate random'}")
    print(f"  Strength: {strength_col or 'Not found - will generate random'}")
    print(f"  Category: {category_col or 'Not found - will generate random'}")
    print(f"  Category2: {category2_col or 'Not found - will generate random'}")
    
    # Convert time to seconds
    if time_col and time_col in df.columns:
        time_series = df[time_col].astype(str)
        time_seconds = []
        for t in time_series:
            try:
                parts = t.split(':')
                if len(parts) >= 3:
                    h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
                    time_seconds.append(h * 3600 + m * 60 + s)
                else:
                    time_seconds.append(np.random.uniform(0, 86400))
            except:
                time_seconds.append(np.random.uniform(0, 86400))
        time_seconds = np.array(time_seconds)
    else:
        time_seconds = np.random.uniform(0, 86400, len(df))
    
    # Prepare numeric columns
    if width_col and width_col in df.columns:
        width = df[width_col].fillna(df[width_col].mean()).values.astype(np.float32)
    else:
        width = np.random.normal(100, 20, len(df)).astype(np.float32)
    
    if height_col and height_col in df.columns:
        height = df[height_col].fillna(df[height_col].mean()).values.astype(np.float32)
    else:
        height = np.random.lognormal(0.5, 0.5, len(df)).astype(np.float32)
    
    if angle_col and angle_col in df.columns:
        angle = df[angle_col].fillna(df[angle_col].mean()).values.astype(np.float32) % 360
    else:
        angle = np.random.uniform(0, 360, len(df)).astype(np.float32)
    
    if strength_col and strength_col in df.columns:
        strength = df[strength_col].fillna(df[strength_col].mean()).values.astype(np.float32)
    else:
        strength = np.random.exponential(20, len(df)).astype(np.float32)
        strength = np.clip(strength, 0, 100)
    
    # Prepare categorical columns
    if category_col and category_col in df.columns:
        categories = df[category_col].fillna('Unknown')
        unique_cats = categories.unique()[:4]  # Max 4 categories
        cat_map = {cat: i for i, cat in enumerate(unique_cats)}
        category_indices = categories.map(cat_map).fillna(0).values.astype(np.uint8)
    else:
        category_indices = np.random.choice([0, 1, 2, 3], len(df), p=[0.4, 0.3, 0.2, 0.1]).astype(np.uint8)
    
    if category2_col and category2_col in df.columns:
        category2_series = df[category2_col]
        unique_vals = category2_series.unique()
        if len(unique_vals) >= 2:
            # Map first unique value to 0, second to 1
            category2_binary = (category2_series == unique_vals[1]).astype(int).values
        else:
            category2_binary = np.zeros(len(df), dtype=int)
    else:
        category2_binary = np.random.choice([0, 1], len(df), p=[0.45, 0.55])
    
    # Create data dictionary
    data = {
        'width': width.astype(np.float32),
        'height': height.astype(np.float32),
        'angle': angle.astype(np.float32),
        'strength': strength.astype(np.float32),
        'category_4': category_indices.astype(np.uint8),
        'category_2': category2_binary.astype(np.uint8),
        'timeSeconds': time_seconds.astype(np.float32)
    }
    
    return data

def create_html_template(data, row_count, compress=False):
    """Create HTML with embedded data"""
    
    # Read the template
    template_path = os.path.join(os.path.dirname(__file__), '..', 'builds', 'selectable_category_dashboard.html')
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        print("Make sure selectable_category_dashboard.html exists in the builds directory")
        sys.exit(1)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Encode data as base64
    encoded_data = {}
    for key, array in data.items():
        if key != 'good_time':  # Skip good_time as it will be generated in JS
            encoded_data[key] = base64.b64encode(array.tobytes()).decode('ascii')
    
    # Create the data loading section
    data_section = f'''
        // Data embedding section
        // Embedded data
        const embeddedData = {{
            width: "{encoded_data['width']}",
            height: "{encoded_data['height']}",
            angle: "{encoded_data['angle']}",
            strength: "{encoded_data['strength']}",
            category_4: "{encoded_data['category_4']}",
            category_2: "{encoded_data['category_2']}",
            timeSeconds: "{encoded_data['timeSeconds']}"
        }};
        
        // Load embedded data
        function loadEmbeddedData() {{
            const startTime = performance.now();
            
            // Decode base64 data
            for (const [key, base64Str] of Object.entries(embeddedData)) {{
                const binaryStr = atob(base64Str);
                const bytes = new Uint8Array(binaryStr.length);
                for (let i = 0; i < binaryStr.length; i++) {{
                    bytes[i] = binaryStr.charCodeAt(i);
                }}
                
                if (key === 'category_4' || key === 'category_2') {{
                    data[key] = new Uint8Array(bytes.buffer);
                }} else {{
                    data[key] = new Float32Array(bytes.buffer);
                }}
            }}
            
            // Generate good_time from timeSeconds
            data.good_time = new Array(ROWS);
            for (let i = 0; i < ROWS; i++) {{
                const totalSeconds = data.timeSeconds[i];
                const h = Math.floor(totalSeconds / 3600);
                const m = Math.floor((totalSeconds % 3600) / 60);
                const s = Math.floor(totalSeconds % 60);
                const ms = Math.floor((totalSeconds % 1) * 1000);
                data.good_time[i] = `${{h.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}.${{ms.toString().padStart(3,'0')}}`;
            }}
            
            // Initialize filtered indices (already defined in template)
            filteredIndices = new Uint8Array(ROWS);
            filteredIndices.fill(1);
            
            const elapsed = performance.now() - startTime;
            console.log(`Data loaded in ${{elapsed.toFixed(1)}}ms`);
            
            // Initialize visualization
            prebinData();
            document.getElementById('loading').style.display = 'none';
            document.getElementById('main').style.display = 'block';
            initCharts();
        }}
        
        // Replace generateData with loadEmbeddedData
        loadEmbeddedData();
    '''
    
    # Replace the ROWS constant
    template = template.replace('const ROWS = 10000000;', f'const ROWS = {row_count};')
    
    # Find and replace the generateData function
    gen_data_start = template.find('// Generate 10M rows')
    if gen_data_start == -1:
        gen_data_start = template.find('function generateData()')
    
    if gen_data_start != -1:
        # Find the end of the generateData call
        gen_data_end = template.find('generateData();')
        if gen_data_end != -1:
            # Find the actual end of the function call
            gen_data_end = template.find('\n', gen_data_end) + 1
            # Replace everything from generateData to its call
            template = template[:gen_data_start] + data_section + template[gen_data_end:]
    else:
        print("Warning: Could not find generateData function to replace")
    
    # Update title and header
    template = template.replace('10M Row Data Explorer', f'{row_count:,} Row Data Explorer')
    template = template.replace('Data Explorer - 10M Rows', f'Data Explorer - {row_count:,} Rows')
    template = template.replace('Generating <strong>10,000,000</strong> rows', f'Loading <strong>{row_count:,}</strong> rows')
    template = template.replace('<strong>10,000,000</strong>', f'<strong>{row_count:,}</strong>')
    
    if compress:
        try:
            import htmlmin
            template = htmlmin.minify(template, 
                                    remove_comments=True, 
                                    remove_empty_space=True,
                                    remove_all_empty_space=False,
                                    reduce_boolean_attributes=True)
            print("HTML compressed successfully")
        except ImportError:
            print("Warning: htmlmin not installed. Install with: pip install htmlmin")
            print("Skipping compression...")
    
    return template

def main():
    args = parse_arguments()
    
    # Read CSV
    print(f"Reading {args.input_csv}...")
    try:
        if args.sample:
            df = pd.read_csv(args.input_csv, nrows=args.sample)
            print(f"Sampled {len(df):,} rows")
        else:
            df = pd.read_csv(args.input_csv)
            print(f"Loaded {len(df):,} rows")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
    
    # Prepare data
    data = prepare_data(df, args)
    
    # Create HTML
    print("\nGenerating HTML dashboard...")
    html_content = create_html_template(data, len(df), args.compress)
    
    # Write output
    with open(args.output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = os.path.getsize(args.output_html) / (1024 * 1024)
    print(f"\nDashboard created successfully!")
    print(f"Output: {args.output_html} ({file_size:.1f} MB)")
    print(f"\nFeatures:")
    print(f"  - {len(df):,} rows of interactive data")
    print(f"  - Selectable category distribution (2 or 4 categories)")
    print(f"  - Cross-filtering between all charts")
    print(f"  - Mini/Mega mode for data isolation")
    print(f"  - CSV export of filtered data")
    print(f"  - Snapshot functionality")

if __name__ == '__main__':
    main()