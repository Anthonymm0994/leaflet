#!/usr/bin/env python3
"""
SUPER SIMPLE Data Embedder for V6 Explorer
Just replace the sample data with your CSV data.

Usage: python embed_data.py your_data.csv
"""

import pandas as pd
import json
import sys
import argparse
from pathlib import Path

def embed_csv_data(csv_file, output_file="my_data_explorer.html", title=None):
    """Embed your CSV data directly into the V6 explorer"""
    
    # Load your data
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} rows from {csv_file}")
    
    # Convert to list of dictionaries
    data_rows = df.to_dict('records')
    
    # Read the template
    template_path = Path(__file__).parent / 'data_explorer.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple approach: replace the data generation loop directly
    # Find the data generation section and replace it
    old_section = """for (; i < end; i++) {
                    data.width[i] = Math.max(0.1, normalRandom(50, 15));
                    data.height[i] = Math.max(0.1, normalRandom(5, 2));
                    data.angle[i] = Math.random() * 360;
                    data.strength[i] = Math.max(0, Math.min(100, normalRandom(50, 20)));
                    data.timeSeconds[i] = Math.random() * 86400;
                    data.category_4[i] = Math.floor(Math.random() * 4);
                    data.category_2[i] = Math.random() < 0.5 ? 0 : 1;
                    data.score[i] = Math.max(0, Math.min(100, normalRandom(75, 15)));  // NEW
                    data.department[i] = Math.floor(Math.random() * 8);                // NEW: 8 departments
                    data.status[i] = Math.random() < 0.7 ? 1 : 0;                    // NEW: 70% active, 30% inactive
                }"""
    
    # Create data embedding
    data_js = json.dumps(data_rows, indent=16)
    new_section = f"""// Your CSV data embedded here
                const csvData = {data_js};
                
                for (; i < end; i++) {{
                    if (i < csvData.length) {{
                        const row = csvData[i];
                        data.width[i] = row.width || 50;
                        data.height[i] = row.height || 5;
                        data.angle[i] = row.angle || 0;
                        data.strength[i] = row.strength || 50;
                        data.timeSeconds[i] = row.timeSeconds || 43200;
                        data.category_4[i] = row.category_4 || 0;
                        data.category_2[i] = row.category_2 || 0;
                        data.score[i] = row.score || 75;
                        data.department[i] = row.department || 0;
                        data.status[i] = row.status || 1;
                    }} else {{
                        // Fill remaining with defaults if CSV is smaller than ROWS
                        data.width[i] = 50;
                        data.height[i] = 5;
                        data.angle[i] = Math.random() * 360;
                        data.strength[i] = 50;
                        data.timeSeconds[i] = 43200;
                        data.category_4[i] = 0;
                        data.category_2[i] = 0;
                        data.score[i] = 75;
                        data.department[i] = 0;
                        data.status[i] = 1;
                    }}
                }}"""
    
    # Replace in content
    if old_section in content:
        content = content.replace(old_section, new_section)
        
        # Update the ROWS constant to match your data size
        content = content.replace('const ROWS = 10000000;', f'const ROWS = {max(len(df), 1000)};')
        content = content.replace('10,000,000', f'{len(df):,}')
        
        # Update title if provided
        if title:
            content = content.replace('Extended Data Explorer - 3x3 Grid', title)
        
        print("✅ Successfully embedded your data!")
        
    else:
        print("⚠️  Warning: Could not find exact data generation section")
        print("   Trying alternative approach...")
        # Alternative: just replace the ROWS constant and let it use your data size
        content = content.replace('const ROWS = 10000000;', f'const ROWS = {len(df)};')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\\n✅ Generated: {output_file}")
    print(f"   📊 {len(df):,} rows embedded")
    print(f"   🎯 3x3 grid layout ready")
    print(f"\\n🚀 Open {output_file} in your browser!")
    
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python embed_data.py your_data.csv [--output my_explorer.html] [--title 'My Title']")
        print("\\nYour CSV should have these columns:")
        print("  width, height, angle, strength, timeSeconds, category_4, score, department, status")
        print("\\nSee sample_data.csv for the exact format.")
        return 1
    
    parser = argparse.ArgumentParser(description='Embed your CSV data into V6 explorer')
    parser.add_argument('csv_file', help='Your CSV file')
    parser.add_argument('--output', '-o', default='my_data_explorer.html', help='Output HTML file')
    parser.add_argument('--title', '-t', help='Explorer title')
    
    args = parser.parse_args()
    
    try:
        embed_csv_data(args.csv_file, args.output, args.title)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
