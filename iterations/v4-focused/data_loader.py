#!/usr/bin/env python3
"""
Simple Data Loader for High-Performance Data Explorer
Easily embed your data into the focused chart system.
"""

import pandas as pd
import json
import argparse
from pathlib import Path

class SimpleDataLoader:
    def __init__(self):
        self.data = []
        self.columns = []
        self.title = "Data Explorer"
    
    def load_csv(self, file_path, **kwargs):
        """Load data from CSV file"""
        df = pd.read_csv(file_path, **kwargs)
        self.data = df.to_dict('records')
        self.columns = self._infer_columns(df)
        print(f"Loaded {len(self.data)} rows with {len(self.columns)} columns")
        return self
    
    def load_json(self, file_path):
        """Load data from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            self.data = data
        else:
            self.data = [data]
        
        if self.data:
            df = pd.DataFrame(self.data)
            self.columns = self._infer_columns(df)
        
        print(f"Loaded {len(self.data)} rows with {len(self.columns)} columns")
        return self
    
    def load_excel(self, file_path, **kwargs):
        """Load data from Excel file"""
        df = pd.read_excel(file_path, **kwargs)
        self.data = df.to_dict('records')
        self.columns = self._infer_columns(df)
        print(f"Loaded {len(self.data)} rows with {len(self.columns)} columns")
        return self
    
    def _infer_columns(self, df):
        """Infer column types for optimal chart selection"""
        columns = []
        
        for col in df.columns:
            values = df[col].dropna()
            if len(values) == 0:
                continue
                
            # Infer type
            col_type = self._infer_type(values)
            columns.append({
                'name': col,
                'type': col_type
            })
        
        return columns
    
    def _infer_type(self, values):
        """Infer the best type for a column"""
        sample = values.head(1000)
        
        # Check for time patterns
        if sample.dtype == 'object':
            time_patterns = sample.astype(str).str.match(r'^\d{1,2}:\d{2}(:\d{2})?$')
            if time_patterns.sum() > len(sample) * 0.8:
                return 'time'
        
        # Check for numeric types
        if pd.api.types.is_numeric_dtype(sample):
            # Check for angles (0-360 range)
            if sample.min() >= 0 and sample.max() <= 360 and len(sample.unique()) > 10:
                return 'angle'
            
            # Check for integers
            if sample.dtype in ['int64', 'int32'] or (sample % 1 == 0).all():
                return 'integer'
            
            return 'number'
        
        # Check for categorical (strings with limited unique values)
        if sample.dtype == 'object' and sample.nunique() <= 20:
            return 'string'
        
        return 'string'
    
    def set_title(self, title):
        """Set the explorer title"""
        self.title = title
        return self
    
    def generate_html(self, output_path):
        """Generate the HTML explorer with embedded data"""
        
        # Create configuration
        config = {
            'title': self.title,
            'data': self.data,
            'columns': self.columns,
            'charts': [
                {
                    'column': col['name'],
                    'title': col['name'].replace('_', ' ').title() + ' Distribution'
                }
                for col in self.columns
            ]
        }
        
        # Read template
        template_path = Path(__file__).parent / 'data_explorer.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Embed configuration
        config_js = f"window.DataConfig = {json.dumps(config, indent=2)};"
        
        # Replace the default config
        html_content = html_content.replace(
            'window.DataConfig = {\n            title: "Sample Data Explorer",\n            data: [], // Your data goes here\n            columns: [], // Column definitions\n            charts: [] // Chart configurations\n        };',
            config_js
        )
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated HTML explorer: {output_path}")
        print(f"  - Data: {len(self.data):,} rows, {len(self.columns)} columns")
        print(f"  - Charts: {len(config['charts'])} charts")
        print(f"  - Title: {self.title}")
        
        return self

def main():
    parser = argparse.ArgumentParser(description='Generate high-performance data explorer')
    parser.add_argument('input_file', help='Input data file (CSV, JSON, or Excel)')
    parser.add_argument('--output', '-o', default='explorer.html', help='Output HTML file')
    parser.add_argument('--title', '-t', help='Explorer title')
    parser.add_argument('--sheet', help='Excel sheet name (for Excel files)')
    
    args = parser.parse_args()
    
    # Determine file type and load
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    loader = SimpleDataLoader()
    
    try:
        if input_path.suffix.lower() == '.csv':
            loader.load_csv(input_path)
        elif input_path.suffix.lower() == '.json':
            loader.load_json(input_path)
        elif input_path.suffix.lower() in ['.xlsx', '.xls']:
            kwargs = {'sheet_name': args.sheet} if args.sheet else {}
            loader.load_excel(input_path, **kwargs)
        else:
            print(f"Error: Unsupported file type: {input_path.suffix}")
            return 1
        
        # Set title
        if args.title:
            loader.set_title(args.title)
        else:
            loader.set_title(f"{input_path.stem} Explorer")
        
        # Generate HTML
        loader.generate_html(args.output)
        
        print(f"\n✅ Success! Open {args.output} in your browser to explore your data.")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
