#!/usr/bin/env python3
"""
Production Data Loader for 3x3 Grid Explorer
Automatically maps your data to the optimal 3x3 layout.
"""

import pandas as pd
import json
import argparse
from pathlib import Path

def load_and_generate(input_file, output_file="explorer.html", title=None):
    """Load data and generate 3x3 grid explorer"""
    
    # Load data
    input_path = Path(input_file)
    if input_path.suffix.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif input_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(input_path)
    elif input_path.suffix.lower() == '.json':
        df = pd.read_json(input_path)
    else:
        raise ValueError(f"Unsupported file type: {input_path.suffix}")
    
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    
    # Infer column types
    columns = {}
    for col in df.columns:
        values = df[col].dropna()
        if len(values) == 0:
            continue
            
        # Infer type
        if pd.api.types.is_numeric_dtype(values):
            if values.min() >= 0 and values.max() <= 360 and values.nunique() > 20:
                columns[col] = 'angle'
            elif values.dtype in ['int64', 'int32'] or (values % 1 == 0).all():
                columns[col] = 'integer'
            else:
                columns[col] = 'number'
        elif values.dtype == 'object' and values.nunique() <= 20:
            columns[col] = 'string'
        else:
            columns[col] = 'number'  # fallback
    
    # Separate columns by type
    hist_cols = [col for col, typ in columns.items() if typ in ['integer', 'number']]
    angle_cols = [col for col, typ in columns.items() if typ == 'angle']
    bar_cols = [col for col, typ in columns.items() if typ == 'string']
    
    # Ensure we have enough columns
    while len(hist_cols) < 6:
        if bar_cols:
            hist_cols.append(bar_cols.pop(0))
        else:
            hist_cols.append(hist_cols[0] if hist_cols else df.columns[0])
    
    while len(angle_cols) < 1:
        if hist_cols:
            angle_cols.append(hist_cols.pop())
        else:
            angle_cols.append(df.columns[0])
    
    while len(bar_cols) < 3:
        if hist_cols:
            bar_cols.append(hist_cols.pop())
        else:
            bar_cols.append(df.columns[0])
    
    # Create chart layout
    chart_layout = [
        # Row 1: hist, hist, angle
        {'id': 'chart1', 'type': 'histogram', 'column': hist_cols[0], 'title': hist_cols[0].replace('_', ' ').upper()},
        {'id': 'chart2', 'type': 'histogram', 'column': hist_cols[1], 'title': hist_cols[1].replace('_', ' ').upper()},
        {'id': 'chart3', 'type': 'angle', 'column': angle_cols[0], 'title': angle_cols[0].replace('_', ' ').upper()},
        # Row 2: hist, hist, bar
        {'id': 'chart4', 'type': 'histogram', 'column': hist_cols[2], 'title': hist_cols[2].replace('_', ' ').upper()},
        {'id': 'chart5', 'type': 'histogram', 'column': hist_cols[3], 'title': hist_cols[3].replace('_', ' ').upper()},
        {'id': 'chart6', 'type': 'bar', 'column': bar_cols[0], 'title': bar_cols[0].replace('_', ' ').upper()},
        # Row 3: hist, bar, bar
        {'id': 'chart7', 'type': 'histogram', 'column': hist_cols[4], 'title': hist_cols[4].replace('_', ' ').upper()},
        {'id': 'chart8', 'type': 'bar', 'column': bar_cols[1], 'title': bar_cols[1].replace('_', ' ').upper()},
        {'id': 'chart9', 'type': 'bar', 'column': bar_cols[2], 'title': bar_cols[2].replace('_', ' ').upper()}
    ]
    
    # Create configuration
    config = {
        'title': title or f"{input_path.stem} - Production Explorer",
        'data': df.to_dict('records'),
        'chartLayout': chart_layout
    }
    
    # Read template
    template_path = Path(__file__).parent / 'data_explorer.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Embed configuration
    config_js = f"window.DataConfig = {json.dumps(config, indent=2)};"
    
    # Replace the default config
    html_content = html_content.replace(
        '''window.DataConfig = {
            title: "Production Data Explorer",
            data: [], // Your data goes here
            chartLayout: [
                // Row 1: hist, hist, angle
                { id: 'chart1', type: 'histogram', column: '', title: '' },
                { id: 'chart2', type: 'histogram', column: '', title: '' },
                { id: 'chart3', type: 'angle', column: '', title: '' },
                // Row 2: hist, hist, bar
                { id: 'chart4', type: 'histogram', column: '', title: '' },
                { id: 'chart5', type: 'histogram', column: '', title: '' },
                { id: 'chart6', type: 'bar', column: '', title: '' },
                // Row 3: hist, bar, bar
                { id: 'chart7', type: 'histogram', column: '', title: '' },
                { id: 'chart8', type: 'bar', column: '', title: '' },
                { id: 'chart9', type: 'bar', column: '', title: '' }
            ]
        };''',
        config_js
    )
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Generated: {output_file}")
    print(f"   📊 Data: {len(df):,} rows")
    print(f"   🎯 Layout: 3x3 grid with optimal chart mapping")
    print(f"   📈 Charts: {len([c for c in chart_layout if c['type'] == 'histogram'])} histograms, {len([c for c in chart_layout if c['type'] == 'angle'])} angle, {len([c for c in chart_layout if c['type'] == 'bar'])} bar charts")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate production 3x3 data explorer')
    parser.add_argument('input_file', help='Input data file (CSV, JSON, or Excel)')
    parser.add_argument('--output', '-o', default='production_explorer.html', help='Output HTML file')
    parser.add_argument('--title', '-t', help='Explorer title')
    
    args = parser.parse_args()
    
    try:
        output_file = load_and_generate(args.input_file, args.output, args.title)
        print(f"\n🚀 Ready! Open {output_file} in your browser.")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
