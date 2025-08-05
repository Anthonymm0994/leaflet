#!/usr/bin/env python3
"""
CSV to Interactive Dashboard Generator

This script takes a CSV file and generates an interactive dashboard HTML file
with the same visualizations as real_next_best_yet.html.

Usage:
    python csv_to_dashboard.py input.csv output.html \
        --time time_column \
        --width width_column \
        --height height_column \
        --angle angle_column \
        --strength strength_column \
        --category category_column \
        --category2 category2_column
"""

import argparse
import pandas as pd
import numpy as np
import base64
import json
import os
import sys
from datetime import datetime
import htmlmin

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate interactive dashboard from CSV')
    parser.add_argument('input_csv', help='Input CSV file')
    parser.add_argument('output_html', help='Output HTML file')
    parser.add_argument('--time', required=True, help='Column name for time (24h format)')
    parser.add_argument('--width', required=True, help='Column name for width')
    parser.add_argument('--height', required=True, help='Column name for height')
    parser.add_argument('--angle', required=True, help='Column name for angle (0-360)')
    parser.add_argument('--strength', required=True, help='Column name for strength')
    parser.add_argument('--category', required=True, help='Column name for main category')
    parser.add_argument('--category2', help='Column name for secondary category (optional)')
    parser.add_argument('--compress', action='store_true', help='Create compressed version')
    parser.add_argument('--sample-size', type=int, help='Sample N rows for testing')
    
    return parser.parse_args()

def time_to_seconds(time_val):
    """Convert time string (HH:MM:SS or similar) to seconds since midnight"""
    if pd.isna(time_val):
        return 0
    
    if isinstance(time_val, (int, float)):
        return float(time_val)
    
    try:
        # Try parsing as time
        if ':' in str(time_val):
            parts = str(time_val).split(':')
            hours = int(parts[0]) if len(parts) > 0 else 0
            minutes = int(parts[1]) if len(parts) > 1 else 0
            seconds = float(parts[2]) if len(parts) > 2 else 0
            return hours * 3600 + minutes * 60 + seconds
        else:
            # Assume it's already in seconds
            return float(time_val)
    except:
        return 0

def prepare_data(df, args):
    """Prepare data for embedding"""
    # Sample if requested
    if args.sample_size and len(df) > args.sample_size:
        df = df.sample(n=args.sample_size, random_state=42)
    
    # Get columns
    time_col = df[args.time]
    width_col = pd.to_numeric(df[args.width], errors='coerce')
    height_col = pd.to_numeric(df[args.height], errors='coerce')
    angle_col = pd.to_numeric(df[args.angle], errors='coerce')
    strength_col = pd.to_numeric(df[args.strength], errors='coerce')
    
    # Handle categories
    category_col = df[args.category]
    unique_categories = category_col.unique()
    category_map = {cat: i for i, cat in enumerate(unique_categories)}
    category_indices = category_col.map(category_map).values
    
    # Handle optional category2
    if args.category2 and args.category2 in df.columns:
        category2_col = df[args.category2]
        # Convert to binary (0/1)
        category2_binary = (category2_col == category2_col.unique()[0]).astype(int).values
    else:
        category2_binary = np.zeros(len(df), dtype=int)
    
    # Convert time to seconds
    time_seconds = time_col.apply(time_to_seconds)
    
    # Create good_time strings
    good_time = []
    for ts in time_seconds:
        hours = int(ts // 3600)
        minutes = int((ts % 3600) // 60)
        seconds = ts % 60
        milliseconds = int((seconds % 1) * 1000)
        good_time.append(f"{hours:02d}:{minutes:02d}:{int(seconds):02d}.{milliseconds:03d}")
    
    # Prepare arrays
    data = {
        'good_time': good_time,
        'width': width_col.fillna(width_col.mean()).values.astype(np.float32),
        'height': height_col.fillna(height_col.mean()).values.astype(np.float32),
        'angle': angle_col.fillna(0).values.astype(np.float32) % 360,  # Ensure 0-360
        'strength': strength_col.fillna(strength_col.mean()).values.astype(np.float32),
        'category_4': category_indices.astype(np.uint8),
        'category_2': category2_binary.astype(np.uint8),
        'timeSeconds': time_seconds.values.astype(np.float32)
    }
    
    # Calculate ranges for display
    ranges = {
        'width': {'min': float(data['width'].min()), 'max': float(data['width'].max())},
        'height': {'min': float(data['height'].min()), 'max': float(data['height'].max())},
        'strength': {'min': float(data['strength'].min()), 'max': float(data['strength'].max())},
        'time': {'min': float(data['timeSeconds'].min()), 'max': float(data['timeSeconds'].max())},
        'categories': list(unique_categories)
    }
    
    return data, ranges, len(df)

def create_html_template(data, ranges, row_count):
    """Create the HTML template with embedded data"""
    
    # Convert arrays to base64
    width_b64 = base64.b64encode(data['width'].tobytes()).decode('utf-8')
    height_b64 = base64.b64encode(data['height'].tobytes()).decode('utf-8')
    angle_b64 = base64.b64encode(data['angle'].tobytes()).decode('utf-8')
    strength_b64 = base64.b64encode(data['strength'].tobytes()).decode('utf-8')
    category_4_b64 = base64.b64encode(data['category_4'].tobytes()).decode('utf-8')
    category_2_b64 = base64.b64encode(data['category_2'].tobytes()).decode('utf-8')
    timeSeconds_b64 = base64.b64encode(data['timeSeconds'].tobytes()).decode('utf-8')
    
    # Read the template from real_next_best_yet.html
    template_path = os.path.join(os.path.dirname(__file__), '..', 'builds', 'test_ag_2', 'real_next_best_yet.html')
    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace the data generation section with our embedded data
    data_section = f'''
        // Data embedding section
        const BATCH_SIZE = 100000;
        
        let data = {{
            good_time: null,
            width: null,
            height: null,
            angle: null,
            strength: null,
            category_4: null,
            category_2: null,
            timeSeconds: null
        }};
        
        let originalData = null;
        let currentRows = ROWS;
        
        let binCache = {{}};
        let filters = {{ width: null, height: null, angle: null, time: null, strength: null, category: new Set() }};
        let filteredIndices = new Uint8Array(ROWS);
        let charts = {{}};
        let statsVisible = false;
        let miniMode = false;
        
        // Load embedded data
        function loadEmbeddedData() {{
            console.log('Loading embedded data...');
            const startTime = performance.now();
            
            // Decode base64 to typed arrays
            data.width = new Float32Array(Uint8Array.from(atob('{width_b64}'), c => c.charCodeAt(0)).buffer);
            data.height = new Float32Array(Uint8Array.from(atob('{height_b64}'), c => c.charCodeAt(0)).buffer);
            data.angle = new Float32Array(Uint8Array.from(atob('{angle_b64}'), c => c.charCodeAt(0)).buffer);
            data.strength = new Float32Array(Uint8Array.from(atob('{strength_b64}'), c => c.charCodeAt(0)).buffer);
            data.category_4 = new Uint8Array(Uint8Array.from(atob('{category_4_b64}'), c => c.charCodeAt(0)).buffer);
            data.category_2 = new Uint8Array(Uint8Array.from(atob('{category_2_b64}'), c => c.charCodeAt(0)).buffer);
            data.timeSeconds = new Float32Array(Uint8Array.from(atob('{timeSeconds_b64}'), c => c.charCodeAt(0)).buffer);
            
            // Generate good_time from timeSeconds
            data.good_time = new Array(ROWS);
            for (let i = 0; i < ROWS; i++) {{
                const totalSeconds = data.timeSeconds[i];
                const hours = Math.floor(totalSeconds / 3600);
                const minutes = Math.floor((totalSeconds % 3600) / 60);
                const seconds = Math.floor(totalSeconds % 60);
                const ms = Math.floor((totalSeconds % 1) * 1000);
                data.good_time[i] = `${{hours.toString().padStart(2, '0')}}:${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}.${{ms.toString().padStart(3, '0')}}`;
            }}
            
            filteredIndices.fill(1);
            
            const loadTime = performance.now() - startTime;
            console.log(`Loaded ${{ROWS.toLocaleString()}} rows in ${{loadTime.toFixed(1)}}ms`);
            
            // Update category display
            const categories = {json.dumps(ranges['categories'])};
            if (categories.length !== 4) {{
                // Update category labels if not exactly 4
                const categoryElements = document.querySelectorAll('[id^="statsCat4"]');
                categoryElements.forEach((el, i) => {{
                    if (i < categories.length) {{
                        el.parentElement.style.display = 'block';
                        el.parentElement.querySelector('span').textContent = categories[i] + ':';
                    }} else {{
                        el.parentElement.style.display = 'none';
                    }}
                }});
            }}
        }}
        
        // Replace generateData with loadEmbeddedData
        window.addEventListener('load', () => {{
            loadEmbeddedData();
            prebinData();
            initCharts();
            updateStats();
        }});
    '''
    
    # Replace the ROWS constant
    template = template.replace('const ROWS = 10000000;', f'const ROWS = {row_count};')
    
    # Find and replace the generateData function
    gen_data_start = template.find('// Generate 10M rows')
    if gen_data_start == -1:
        gen_data_start = template.find('function generateData()')
    
    if gen_data_start != -1:
        # Find the end of the generateData call
        gen_data_end = template.find('prebinData();', gen_data_start)
        if gen_data_end != -1:
            # Replace everything from generateData to just before prebinData
            template = template[:gen_data_start] + data_section + '\n        ' + template[gen_data_end:]
    else:
        print("Warning: Could not find generateData function to replace")
    
    # Update the fixed ranges in prebinData for normal mode
    template = template.replace(
        'binCache.width = binData(data.width, 1, 200, 100);',
        f'binCache.width = binData(data.width, {ranges["width"]["min"]}, {ranges["width"]["max"]}, 100);'
    )
    template = template.replace(
        'binCache.height = binData(data.height, 0.2, 4.8, 100);',
        f'binCache.height = binData(data.height, {ranges["height"]["min"]}, {ranges["height"]["max"]}, 100);'
    )
    template = template.replace(
        'binCache.strength = binData(data.strength, 0, 100, 100);',
        f'binCache.strength = binData(data.strength, {ranges["strength"]["min"]}, {ranges["strength"]["max"]}, 100);'
    )
    template = template.replace(
        'binCache.time = binData(data.timeSeconds, 0, 86400, 96);',
        f'binCache.time = binData(data.timeSeconds, {ranges["time"]["min"]}, {ranges["time"]["max"]}, 96);'
    )
    
    return template

def main():
    args = parse_arguments()
    
    print(f"Reading CSV file: {args.input_csv}")
    df = pd.read_csv(args.input_csv)
    print(f"Loaded {len(df):,} rows")
    
    print("Preparing data...")
    data, ranges, row_count = prepare_data(df, args)
    
    print("Creating HTML template...")
    html_content = create_html_template(data, ranges, row_count)
    
    # Write uncompressed version
    output_path = args.output_html
    print(f"Writing HTML to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    uncompressed_size = os.path.getsize(output_path)
    print(f"Uncompressed size: {uncompressed_size:,} bytes ({uncompressed_size/1024/1024:.2f} MB)")
    
    # Create compressed version if requested
    if args.compress:
        compressed_path = output_path.replace('.html', '-compressed.html')
        print(f"Creating compressed version: {compressed_path}")
        
        # Minify HTML
        minified = htmlmin.minify(html_content, 
                                 remove_comments=True,
                                 remove_empty_space=True,
                                 remove_all_empty_space=True,
                                 reduce_boolean_attributes=True,
                                 remove_optional_attribute_quotes=False)
        
        with open(compressed_path, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        compressed_size = os.path.getsize(compressed_path)
        print(f"Compressed size: {compressed_size:,} bytes ({compressed_size/1024/1024:.2f} MB)")
        print(f"Compression ratio: {(1 - compressed_size/uncompressed_size)*100:.1f}%")
    
    print("Done!")

if __name__ == '__main__':
    main()