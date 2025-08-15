#!/usr/bin/env python3
"""
Data Loader for Generic Data Explorer

This script loads data from various sources and generates the configuration
needed for the modular data explorer.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import argparse
from typing import Dict, List, Any, Union
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExplorerConfig:
    """Configuration generator for the Data Explorer"""
    
    def __init__(self):
        self.config = {
            "title": "Generic Data Explorer",
            "columns": [],
            "data": [],
            "columnTypes": {},
            "chartTypes": [],
            "miniMetrics": []
        }
    
    def load_csv(self, file_path: str, **kwargs) -> 'DataExplorerConfig':
        """Load data from CSV file"""
        logger.info(f"Loading CSV from {file_path}")
        
        try:
            df = pd.read_csv(file_path, **kwargs)
            return self.load_dataframe(df)
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
    
    def load_dataframe(self, df: pd.DataFrame) -> 'DataExplorerConfig':
        """Load data from pandas DataFrame"""
        logger.info(f"Loading DataFrame with {len(df)} rows and {len(df.columns)} columns")
        
        # Convert DataFrame to list of dictionaries
        self.config["data"] = df.to_dict('records')
        self.config["columns"] = df.columns.tolist()
        
        # Infer column types
        self.config["columnTypes"] = self._infer_column_types(df)
        
        # Generate default chart configurations
        self.config["chartTypes"] = self._generate_chart_configs(df)
        
        # Generate mini metrics
        self.config["miniMetrics"] = self._generate_mini_metrics(df)
        
        return self
    
    def load_json(self, file_path: str) -> 'DataExplorerConfig':
        """Load data from JSON file"""
        logger.info(f"Loading JSON from {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                # List of objects
                self.config["data"] = data
                if data:
                    self.config["columns"] = list(data[0].keys())
            elif isinstance(data, dict):
                # Single object or nested structure
                if "data" in data:
                    self.config.update(data)
                else:
                    # Assume it's a single record
                    self.config["data"] = [data]
                    self.config["columns"] = list(data.keys())
            
            # Infer types if not provided
            if not self.config.get("columnTypes"):
                df = pd.DataFrame(self.config["data"])
                self.config["columnTypes"] = self._infer_column_types(df)
            
            # Generate chart configs if not provided
            if not self.config.get("chartTypes"):
                df = pd.DataFrame(self.config["data"])
                self.config["chartTypes"] = self._generate_chart_configs(df)
            
            return self
            
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            raise
    
    def _infer_column_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """Infer column types from DataFrame"""
        column_types = {}
        
        for col in df.columns:
            dtype = df[col].dtype
            
            if pd.api.types.is_numeric_dtype(dtype):
                if pd.api.types.is_integer_dtype(dtype):
                    column_types[col] = "integer"
                else:
                    column_types[col] = "number"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_types[col] = "time"
            elif pd.api.types.is_string_dtype(dtype):
                # Check if it's time-like
                if self._is_time_column(df[col]):
                    column_types[col] = "time"
                else:
                    column_types[col] = "string"
            else:
                column_types[col] = "string"
        
        return column_types
    
    def _is_time_column(self, series: pd.Series) -> bool:
        """Check if a column contains time-like data"""
        if len(series) == 0:
            return False
        
        # Sample some values to check
        sample = series.dropna().head(100)
        if len(sample) == 0:
            return False
        
        # Check for time patterns (HH:MM:SS, HH:MM, etc.)
        time_patterns = [
            r'^\d{1,2}:\d{2}(:\d{2})?(\.\d+)?$',  # HH:MM:SS or HH:MM
            r'^\d{1,2}:\d{2}$',  # HH:MM
            r'^\d{1,2}:\d{2}:\d{2}$',  # HH:MM:SS
        ]
        
        import re
        for pattern in time_patterns:
            if sample.astype(str).str.match(pattern).all():
                return True
        
        return False
    
    def _generate_chart_configs(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate chart configurations based on data types"""
        chart_configs = []
        
        for col in df.columns:
            col_type = self.config["columnTypes"].get(col, "string")
            
            if col_type in ["number", "integer"]:
                # Histogram for numerical data
                chart_configs.append({
                    "type": "histogram",
                    "column": col,
                    "title": f"{col} Distribution"
                })
            elif col_type == "time":
                # Time chart for time data
                chart_configs.append({
                    "type": "time",
                    "column": col,
                    "title": f"{col} Distribution"
                })
            elif col_type == "string":
                # Categorical chart for string data
                unique_count = df[col].nunique()
                if unique_count <= 20:  # Only show categorical for reasonable number of categories
                    chart_configs.append({
                        "type": "categorical",
                        "column": col,
                        "title": f"{col} Distribution"
                    })
        
        # Limit to 6 charts for grid layout
        return chart_configs[:6]
    
    def _generate_mini_metrics(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate mini metrics configuration"""
        metrics = [
            {"id": "filtered", "label": "Filtered Rows"},
            {"id": "percent", "label": "of Total"}
        ]
        
        # Add some numerical column averages
        numerical_cols = [col for col, type_ in self.config["columnTypes"].items() 
                         if type_ in ["number", "integer"]]
        
        for col in numerical_cols[:2]:  # Limit to 2 additional metrics
            metrics.append({
                "id": f"avg_{col}",
                "label": f"Avg {col}"
            })
        
        return metrics
    
    def set_title(self, title: str) -> 'DataExplorerConfig':
        """Set the explorer title"""
        self.config["title"] = title
        return self
    
    def add_chart(self, chart_config: Dict[str, Any]) -> 'DataExplorerConfig':
        """Add a custom chart configuration"""
        self.config["chartTypes"].append(chart_config)
        return self
    
    def set_chart_types(self, chart_types: List[Dict[str, Any]]) -> 'DataExplorerConfig':
        """Set custom chart types"""
        self.config["chartTypes"] = chart_types
        return self
    
    def set_mini_metrics(self, metrics: List[Dict[str, str]]) -> 'DataExplorerConfig':
        """Set custom mini metrics"""
        self.config["miniMetrics"] = metrics
        return self
    
    def get_config(self) -> Dict[str, Any]:
        """Get the configuration dictionary"""
        return self.config.copy()
    
    def save_config(self, file_path: str) -> None:
        """Save configuration to JSON file"""
        logger.info(f"Saving configuration to {file_path}")
        
        with open(file_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def generate_html(self, output_path: str, template_path: str = None) -> None:
        """Generate a complete HTML file with embedded data"""
        logger.info(f"Generating HTML to {output_path}")
        
        if template_path and Path(template_path).exists():
            # Use custom template
            with open(template_path, 'r') as f:
                html_content = f.read()
        else:
            # Use default template
            html_content = self._get_default_template()
        
        # Embed the configuration
        config_script = f"""
        <script>
            window.DataExplorerConfig = {json.dumps(self.config, indent=2)};
        </script>
        """
        
        # Insert configuration before the closing </body> tag
        html_content = html_content.replace('</body>', f'{config_script}\n</body>')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _get_default_template(self) -> str:
        """Get default HTML template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Explorer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #e0e0e0; overflow: hidden; }
        #loading { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
        .progress { width: 400px; height: 6px; background: #333; margin-top: 10px; border-radius: 3px; }
        .progress-bar { height: 100%; background: #4a9eff; transition: width 0.1s; border-radius: 3px; }
        #main { display: none; height: 100vh; padding: 8px; }
        .header { background: #1a1a1a; padding: 8px 16px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .stats { display: flex; gap: 15px; font-size: 13px; }
        .stats span { display: flex; align-items: center; gap: 5px; }
        .stats strong { color: #4a9eff; }
        button { background: #4a9eff; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
        button:hover { background: #3a8eef; }
        button:active { transform: scale(0.95); }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(2, 1fr); gap: 8px; height: calc(100% - 140px); }
        .panel { background: #1a1a1a; border-radius: 4px; padding: 8px; position: relative; }
        .panel-title { font-size: 13px; margin-bottom: 4px; font-weight: 500; }
        canvas { position: absolute; top: 28px; left: 8px; right: 8px; bottom: 20px; cursor: crosshair; }
        select { background: #333; color: #e0e0e0; border: 1px solid #555; padding: 3px 6px; border-radius: 3px; position: absolute; top: 4px; right: 8px; font-size: 11px; }
        #tooltip { position: fixed; background: rgba(0,0,0,0.95); padding: 6px 10px; border-radius: 3px; font-size: 11px; pointer-events: none; display: none; z-index: 1000; border: 1px solid #333; }
        .mini-mode { display: none; }
        .mini-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; }
        .mini-panel { background: #1a1a1a; border-radius: 4px; padding: 12px; text-align: center; }
        .mini-value { font-size: 24px; font-weight: 600; color: #4a9eff; }
        .mini-label { font-size: 11px; color: #999; margin-top: 4px; }
        #statsPanel { position: absolute; top: 60px; right: 16px; background: rgba(26,26,26,0.95); border: 1px solid #333; border-radius: 4px; padding: 12px; font-size: 12px; display: none; z-index: 100; }
        #statsPanel div { margin-bottom: 4px; }
        #statsPanel strong { color: #4a9eff; margin-left: 4px; }
        .range-display { 
            background: #1a1a1a; 
            padding: 12px 16px; 
            border-radius: 4px; 
            margin-bottom: 8px;
            display: flex; 
            gap: 24px; 
            flex-wrap: wrap;
        }
        .mini-mode .range-display { display: none; }
        .range-item { 
            display: flex; 
            flex-direction: column; 
            min-width: 120px;
        }
        .range-label { 
            font-size: 11px; 
            color: #888; 
            margin-bottom: 2px; 
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .range-value { 
            font-size: 13px; 
            color: #4a9eff; 
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div id="loading">
        <div>Loading data...</div>
        <div class="progress"><div class="progress-bar" id="progress"></div></div>
        <div id="loadingStatus" style="margin-top: 8px; font-size: 12px; color: #999;"></div>
    </div>
    
    <div id="main">
        <div class="header">
            <h3 id="title">Data Explorer</h3>
            <div class="stats">
                <span>Total: <strong id="totalCount">0</strong></span>
                <span>Filtered: <strong id="filteredCount">0</strong></span>
                <span>Selected: <strong id="percentFiltered">0%</strong></span>
            </div>
            <div style="display: flex; gap: 8px;">
                <button onclick="DataExplorer.toggleStats()">📊 Stats</button>
                <button id="miniModeBtn" onclick="DataExplorer.toggleMiniMode()">📱 Mini</button>
                <button onclick="DataExplorer.resetAll()">🔄 Reset</button>
                <button onclick="DataExplorer.exportCSV()">💾 CSV</button>
                <button onclick="DataExplorer.saveSnapshot()">📷 Snapshot</button>
            </div>
        </div>
        
        <div class="range-display" id="rangeDisplay"></div>
        
        <div class="grid" id="chartGrid"></div>
        
        <div class="mini-mode" id="miniMode">
            <div class="mini-grid" id="miniGrid"></div>
        </div>
    </div>
    
    <div id="tooltip"></div>
    <div id="statsPanel"></div>
    
         <!-- Core Modules -->
     <script src="../modules/DataManager.js"></script>
     <script src="../modules/ChartManager.js"></script>
     <script src="../modules/FilterManager.js"></script>
     <script src="../modules/DataExplorer.js"></script>
    
    <script>
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            DataExplorer.init();
        });
    </script>
</body>
</html>"""

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='Generate Data Explorer configuration')
    parser.add_argument('input', help='Input file (CSV, JSON, or Excel)')
    parser.add_argument('--output', '-o', help='Output HTML file')
    parser.add_argument('--config', '-c', help='Output configuration JSON file')
    parser.add_argument('--title', '-t', help='Explorer title')
    parser.add_argument('--format', '-f', choices=['csv', 'json', 'excel'], help='Input file format')
    
    args = parser.parse_args()
    
    # Determine file format
    if args.format:
        file_format = args.format
    else:
        file_format = Path(args.input).suffix.lower().lstrip('.')
        if file_format == 'xlsx' or file_format == 'xls':
            file_format = 'excel'
    
    # Create configuration
    config = DataExplorerConfig()
    
    try:
        if file_format == 'csv':
            config.load_csv(args.input)
        elif file_format == 'json':
            config.load_json(args.input)
        elif file_format == 'excel':
            df = pd.read_excel(args.input)
            config.load_dataframe(df)
        else:
            logger.error(f"Unsupported file format: {file_format}")
            return 1
        
        # Set title if provided
        if args.title:
            config.set_title(args.title)
        
        # Save configuration if requested
        if args.config:
            config.save_config(args.config)
            logger.info(f"Configuration saved to {args.config}")
        
        # Generate HTML
        if args.output:
            config.generate_html(args.output)
            logger.info(f"HTML generated to {args.output}")
        else:
            # Default output
            output_file = Path(args.input).stem + '_explorer.html'
            config.generate_html(output_file)
            logger.info(f"HTML generated to {output_file}")
        
        # Print summary
        data_count = len(config.config["data"])
        column_count = len(config.config["columns"])
        chart_count = len(config.config["chartTypes"])
        
        logger.info(f"Configuration generated successfully:")
        logger.info(f"  - Data: {data_count:,} rows, {column_count} columns")
        logger.info(f"  - Charts: {chart_count} charts")
        logger.info(f"  - Title: {config.config['title']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
