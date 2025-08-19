#!/usr/bin/env python3
"""
Simple Data Loader for V6 Extended Data Explorer
Easily populate the 3x3 grid with your own data.

Usage:
    python load_your_data.py your_data.csv --output my_explorer.html
"""

import pandas as pd
import json
import argparse
from pathlib import Path

def load_and_generate_explorer(csv_file, output_file="my_data_explorer.html", title=None):
    """
    Load your CSV data and generate a working V6 explorer
    
    Expected CSV columns (rename your columns to match these):
    - width: numerical data for histogram
    - height: numerical data for histogram  
    - angle: angular data (0-360) for radial chart
    - strength: numerical data for histogram
    - timeSeconds: time data in seconds (0-86400 for 24h) for histogram
    - category_4: categorical data with 4 categories (0,1,2,3) for bar chart
    - score: numerical data for histogram (NEW bottom row)
    - department: categorical data with 8 categories (0,1,2,3,4,5,6,7) for bar chart (NEW)
    - status: categorical data with 2 categories (0,1) for bar chart (NEW)
    """
    
    print(f"Loading data from {csv_file}...")
    df = pd.read_csv(csv_file)
    
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    
    # Convert to the format expected by the explorer
    data_rows = df.to_dict('records')
    
    # Read the V6 template
    template_path = Path(__file__).parent / 'data_explorer.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create JavaScript to replace the generateData function
    js_data_replacement = f"""
        // Replace generateData with your actual data
        async function generateData() {{
            // Your data loaded from CSV
            const csvData = {json.dumps(data_rows, indent=4)};
            const numRows = csvData.length;
            
            // Initialize TypedArrays with your data
            data.width = new Float32Array(numRows);
            data.height = new Float32Array(numRows);
            data.angle = new Float32Array(numRows);
            data.strength = new Float32Array(numRows);
            data.timeSeconds = new Float32Array(numRows);
            data.category_4 = new Uint8Array(numRows);
            data.category_2 = new Uint8Array(numRows);
            data.score = new Float32Array(numRows);
            data.department = new Uint8Array(numRows);
            data.status = new Uint8Array(numRows);
            
            // Fill arrays with your data
            for (let i = 0; i < numRows; i++) {{
                const row = csvData[i];
                data.width[i] = row.width || 50;
                data.height[i] = row.height || 5;
                data.angle[i] = row.angle || 0;
                data.strength[i] = row.strength || 50;
                data.timeSeconds[i] = row.timeSeconds || 43200; // default noon
                data.category_4[i] = row.category_4 || 0;
                data.category_2[i] = row.category_2 || 0;
                data.score[i] = row.score || 75;
                data.department[i] = row.department || 0;
                data.status[i] = row.status || 1;
            }}
            
            // Update ROWS constant
            window.ROWS = numRows;
            currentRows = numRows;
            
            // Initialize filtered indices
            filteredIndices = new Uint8Array(numRows);
            filteredIndices.fill(1);
            
            // Process and display
            prebinData();
            createCharts();
            updateStats();
            updateRanges();
            document.getElementById('loading').style.display = 'none';
            document.getElementById('main').style.display = 'block';
        }}
    """
    
    # Replace the original generateData function
    html_content = html_content.replace(
        'async function generateData() {',
        js_data_replacement + '\n        // ORIGINAL FUNCTION REPLACED\n        async function generateData_ORIGINAL() {'
    )
    
    # Update the title
    if title:
        html_content = html_content.replace(
            '<title>Extended Data Explorer - 3x3 Grid</title>',
            f'<title>{title}</title>'
        )
        html_content = html_content.replace(
            '<h3>Extended Data Explorer - 3x3 Grid</h3>',
            f'<h3>{title}</h3>'
        )
    
    # Update the row count display
    html_content = html_content.replace(
        '<span>Total: <strong>10,000,000</strong></span>',
        f'<span>Total: <strong>{len(df):,}</strong></span>'
    )
    html_content = html_content.replace(
        '<span>Filtered: <strong id="filteredCount">10,000,000</strong></span>',
        f'<span>Filtered: <strong id="filteredCount">{len(df):,}</strong></span>'
    )
    html_content = html_content.replace(
        '<div>Generating <strong>10,000,000</strong> rows...</div>',
        f'<div>Loading <strong>{len(df):,}</strong> rows...</div>'
    )
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\\n✅ Generated: {output_file}")
    print(f"   📊 Data: {len(df):,} rows")
    print(f"   🎯 Layout: 3x3 grid with your data")
    print(f"\\n🚀 Open {output_file} in your browser to see your data!")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Load your data into V6 Extended Data Explorer')
    parser.add_argument('csv_file', help='Your CSV file path')
    parser.add_argument('--output', '-o', default='my_data_explorer.html', help='Output HTML file name')
    parser.add_argument('--title', '-t', help='Title for the explorer')
    
    args = parser.parse_args()
    
    try:
        # Check if CSV file exists
        if not Path(args.csv_file).exists():
            print(f"❌ Error: CSV file not found: {args.csv_file}")
            print("\\nMake sure your CSV has these columns:")
            print("  - width, height, angle, strength, timeSeconds, category_4, score, department, status")
            return 1
        
        # Generate the explorer
        output_file = load_and_generate_explorer(
            args.csv_file, 
            args.output, 
            args.title or f"Data Explorer - {Path(args.csv_file).stem}"
        )
        
        print(f"\\n📋 Expected CSV Format:")
        print("   width: numerical (e.g., 10.5, 25.3)")
        print("   height: numerical (e.g., 2.1, 8.7)")
        print("   angle: 0-360 degrees (e.g., 45.2, 180.0)")
        print("   strength: numerical (e.g., 75.5, 42.1)")
        print("   timeSeconds: 0-86400 seconds in day (e.g., 43200 = noon)")
        print("   category_4: integers 0-3 (e.g., 0, 1, 2, 3)")
        print("   score: numerical (e.g., 85.2, 92.1)")
        print("   department: integers 0-7 (e.g., 0, 1, 2, 3, 4, 5, 6, 7)")
        print("   status: integers 0-1 (e.g., 0=inactive, 1=active)")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
