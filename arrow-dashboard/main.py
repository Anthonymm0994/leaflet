#!/usr/bin/env python3
"""
Arrow Data Explorer Dashboard - Professional Edition
A standalone desktop application for exploring Apache Arrow files using polars and panel.
Enhanced with professional UI, advanced analytics, and robust data handling.
"""

import os
import sys
import tempfile
import gc
import psutil
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union
import logging
import traceback
from datetime import datetime
import json

import pyarrow as pa
import polars as pl
import panel as pn
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Panel with enhanced styling
pn.extension('plotly', sizing_mode='stretch_width', notifications=True)

# Custom CSS for professional styling
CUSTOM_CSS = """
<style>
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.status-card {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}

.info-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.plot-container {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.control-panel {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    padding: 15px;
    margin: 5px;
    text-align: center;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

.metric-label {
    font-size: 12px;
    opacity: 0.9;
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.error-message {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}

.success-message {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}

.tab-content {
    padding: 20px;
}

.advanced-controls {
    background: #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}
</style>
"""

class ArrowDataExplorer:
    """Enhanced Arrow data exploration dashboard with professional UI and advanced features."""
    
    def __init__(self):
        self.df: Optional[pl.DataFrame] = None
        self.file_path: Optional[str] = None
        self.original_df: Optional[pl.DataFrame] = None
        self.temp_files: List[str] = []
        self.loading_state = False
        self.last_plot_time = 0
        self.plot_cache = {}
        
        # Performance tracking
        self.load_times = []
        self.plot_times = []
        
        self.setup_ui()
        self.setup_advanced_features()
    
    def setup_ui(self):
        """Initialize the enhanced dashboard UI components."""
        # Header
        self.header = pn.pane.HTML(
            f"""
            {CUSTOM_CSS}
            <div class="dashboard-header">
                <h1>🚀 Arrow Data Explorer - Professional Edition</h1>
                <p>Advanced Apache Arrow file analysis and visualization</p>
            </div>
            """,
            width=800
        )
        
        # File upload with drag & drop
        self.file_input = pn.widgets.FileInput(
            name='📁 Upload Arrow File',
            accept='.arrow,.parquet',
            width=400,
            height=60
        )
        self.file_input.param.watch(self.load_file, 'value')
        
        # Status and metrics
        self.status_panel = pn.Column(
            pn.pane.HTML('<div class="status-card"><h3>📊 Status</h3><p>No file loaded</p></div>'),
            pn.Row(
                pn.pane.HTML('<div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Rows</div></div>'),
                pn.pane.HTML('<div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Columns</div></div>'),
                pn.pane.HTML('<div class="metric-card"><div class="metric-value">0 MB</div><div class="metric-label">Size</div></div>'),
                pn.pane.HTML('<div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Nulls</div></div>')
            )
        )
        
        # File information
        self.file_info = pn.pane.HTML('<div class="info-card"><h3>📋 File Information</h3><p>No file loaded</p></div>')
        
        # Data preview with pagination
        self.preview_page = pn.widgets.IntSlider(name='Preview Page', start=1, end=1, value=1, step=1)
        self.preview_page.param.watch(self.update_data_preview, 'value')
        self.data_preview = pn.pane.HTML('<div class="info-card"><h3>👀 Data Preview</h3><p>No data to display</p></div>')
        
        # Advanced column selectors
        self.x_column = pn.widgets.Select(name='📈 X Axis Column', options=[], width=200)
        self.y_column = pn.widgets.Select(name='📊 Y Axis Column', options=[], width=200)
        self.plot_type = pn.widgets.Select(
            name='🎨 Plot Type',
            options=['histogram', 'scatter', 'box', 'line', 'bar', 'violin', 'heatmap', '3d_scatter', 'surface'],
            value='histogram',
            width=200
        )
        
        # Advanced filtering
        self.filter_panel = pn.Column(
            pn.pane.HTML('<div class="advanced-controls"><h4>🔍 Advanced Filtering</h4></div>'),
            pn.Row(
                pn.widgets.Select(name='Filter Column', options=[], width=150),
                pn.widgets.Select(name='Filter Operator', options=['==', '!=', '>', '<', '>=', '<=', 'contains', 'starts_with'], value='==', width=100),
                pn.widgets.TextInput(name='Filter Value', placeholder='Enter value', width=150),
                pn.widgets.Button(name='Apply Filter', button_type='warning', width=100),
                pn.widgets.Button(name='Reset Filter', button_type='secondary', width=100)
            )
        )
        
        # Plot controls
        self.plot_controls = pn.Column(
            pn.pane.HTML('<div class="advanced-controls"><h4>📊 Visualization Controls</h4></div>'),
            pn.Row(
                self.x_column,
                self.y_column,
                self.plot_type,
                pn.widgets.Button(name='Create Plot', button_type='primary', width=120),
                pn.widgets.Button(name='Auto Plots', button_type='success', width=120)
            )
        )
        
        # Export and analysis
        self.export_panel = pn.Column(
            pn.pane.HTML('<div class="advanced-controls"><h4>💾 Export & Analysis</h4></div>'),
            pn.Row(
                pn.widgets.Button(name='Export to CSV', button_type='success', width=120),
                pn.widgets.Button(name='Generate Report', button_type='primary', width=120),
                pn.widgets.Button(name='Memory Analysis', button_type='secondary', width=120)
            )
        )
        
        # Memory and performance
        self.performance_panel = pn.Column(
            pn.pane.HTML('<div class="advanced-controls"><h4>⚡ Performance Metrics</h4></div>'),
            pn.pane.HTML('<div class="info-card"><p>Memory Usage: Not available</p><p>Load Time: Not available</p><p>Plot Time: Not available</p></div>')
        )
        
        # Plot area with enhanced styling
        self.plot_area = pn.pane.Plotly({}, sizing_mode='stretch_width', height=600)
        
        # Create tabs for better organization
        self.create_tabbed_layout()
    
    def setup_advanced_features(self):
        """Setup advanced features and event handlers."""
        # Connect event handlers
        self.filter_panel[1][3].on_click(self.apply_advanced_filter)
        self.filter_panel[1][4].on_click(self.reset_filter)
        self.plot_controls[1][3].on_click(self.create_plot)
        self.plot_controls[1][4].on_click(self.create_auto_plots)
        self.export_panel[1][0].on_click(self.export_data)
        self.export_panel[1][1].on_click(self.generate_report)
        self.export_panel[1][2].on_click(self.analyze_memory)
    
    def create_tabbed_layout(self):
        """Create a professional tabbed layout."""
        # Main dashboard tab
        dashboard_tab = pn.Column(
            self.header,
            self.file_input,
            self.status_panel,
            self.file_info,
            pn.Row(self.preview_page, self.data_preview),
            self.plot_area
        )
        
        # Controls tab
        controls_tab = pn.Column(
            pn.pane.HTML('<h2>🎛️ Advanced Controls</h2>'),
            self.filter_panel,
            self.plot_controls,
            self.export_panel
        )
        
        # Analysis tab
        analysis_tab = pn.Column(
            pn.pane.HTML('<h2>📈 Data Analysis</h2>'),
            self.performance_panel,
            pn.pane.HTML('<div class="info-card"><h3>📊 Statistical Summary</h3><p>No data loaded</p></div>'),
            pn.pane.HTML('<div class="info-card"><h3>🔍 Data Quality</h3><p>No data loaded</p></div>')
        )
        
        # Create tabs
        self.tabs = pn.Tabs(
            ('📊 Dashboard', dashboard_tab),
            ('🎛️ Controls', controls_tab),
            ('📈 Analysis', analysis_tab)
        )
        
        # Main layout
        self.layout = pn.Column(
            self.tabs,
            sizing_mode='stretch_width'
        )
    
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.info(f"Cleaned up temp file: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up {temp_file}: {e}")
        self.temp_files.clear()
    
    def load_file(self, event):
        """Enhanced file loading with progress tracking and error handling."""
        if not event.value:
            return
        
        self.loading_state = True
        self.update_status("🔄 Loading file...", "loading")
        
        try:
            start_time = time.time()
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.arrow')
            temp_file.write(event.value)
            temp_file.close()
            self.temp_files.append(temp_file.name)
            
            # Load with pyarrow
            table = pa.ipc.open_file(temp_file.name).read_all()
            self.df = pl.from_arrow(table)
            self.original_df = self.df.clone()
            
            # Update file path
            self.file_path = temp_file.name
            
            # Track performance
            load_time = time.time() - start_time
            self.load_times.append(load_time)
            
            # Update UI
            self.update_file_info()
            self.update_status(f"✅ File loaded successfully in {load_time:.2f}s", "success")
            self.update_column_selectors()
            self.update_data_preview()
            self.update_performance_metrics()
            
            # Enable controls
            self.enable_controls()
            
            # Create initial plots
            self.create_auto_plots()
            
        except Exception as e:
            error_msg = f"❌ Failed to load file: {str(e)}"
            logger.error(error_msg)
            self.update_status(error_msg, "error")
            self.show_error(f"File loading failed: {str(e)}")
        finally:
            self.loading_state = False
            gc.collect()
    
    def update_file_info(self):
        """Update file information display with enhanced details."""
        if not self.df:
            return
        
        try:
            # Basic info
            rows, cols = self.df.shape
            file_size = self.get_file_size()
            
            # Schema info
            schema_info = []
            for field in self.df.schema:
                null_count = self.df.select(pl.col(field.name).null_count()).item()
                schema_info.append(f"- **{field.name}**: {field.dtype} ({null_count} nulls)")
            
            # Memory usage
            memory_usage = self.df.estimated_size() / (1024 * 1024)  # MB
            
            # Data types summary
            dtype_counts = {}
            for field in self.df.schema:
                dtype = str(field.dtype)
                dtype_counts[dtype] = dtype_counts.get(dtype, 0) + 1
            
            dtype_summary = ", ".join([f"{dtype}: {count}" for dtype, count in dtype_counts.items()])
            
            info_html = f"""
            <div class="info-card">
                <h3>📋 File Information</h3>
                <p><strong>Rows:</strong> {rows:,}</p>
                <p><strong>Columns:</strong> {cols}</p>
                <p><strong>File Size:</strong> {file_size}</p>
                <p><strong>Memory Usage:</strong> {memory_usage:.2f} MB</p>
                <p><strong>Data Types:</strong> {dtype_summary}</p>
                <h4>Schema:</h4>
                <ul>
                    {chr(10).join(schema_info)}
                </ul>
            </div>
            """
            
            self.file_info.object = info_html
            
        except Exception as e:
            logger.error(f"Failed to update file info: {e}")
    
    def get_file_size(self) -> str:
        """Get formatted file size."""
        if not self.file_path or not os.path.exists(self.file_path):
            return "Unknown"
        
        size = os.path.getsize(self.file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def update_performance_metrics(self):
        """Update performance metrics display."""
        if not self.df:
            return
        
        try:
            # Memory usage
            process = psutil.Process()
            memory_mb = process.memory_info().rss / (1024 * 1024)
            
            # Load time
            avg_load_time = np.mean(self.load_times) if self.load_times else 0
            
            # Plot time
            avg_plot_time = np.mean(self.plot_times) if self.plot_times else 0
            
            metrics_html = f"""
            <div class="info-card">
                <h3>⚡ Performance Metrics</h3>
                <p><strong>Memory Usage:</strong> {memory_mb:.2f} MB</p>
                <p><strong>Average Load Time:</strong> {avg_load_time:.3f}s</p>
                <p><strong>Average Plot Time:</strong> {avg_plot_time:.3f}s</p>
                <p><strong>DataFrame Size:</strong> {self.df.estimated_size() / (1024 * 1024):.2f} MB</p>
            </div>
            """
            
            self.performance_panel[1].object = metrics_html
            
        except Exception as e:
            logger.error(f"Failed to update performance metrics: {e}")
    
    def update_data_preview(self, event=None):
        """Update data preview with pagination."""
        if not self.df:
            return
        
        try:
            page = self.preview_page.value if event is None else event.new
            page_size = 10
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            
            # Get preview data
            preview_df = self.df.slice(start_idx, page_size)
            
            # Convert to pandas for display
            preview_pandas = preview_df.to_pandas()
            
            # Create HTML table
            html_table = preview_pandas.to_html(
                classes='table table-striped table-hover',
                index=False,
                float_format='%.3f'
            )
            
            preview_html = f"""
            <div class="info-card">
                <h3>👀 Data Preview (Page {page})</h3>
                <p>Showing rows {start_idx + 1}-{min(end_idx, len(self.df))} of {len(self.df):,}</p>
                {html_table}
            </div>
            """
            
            self.data_preview.object = preview_html
            
            # Update pagination
            total_pages = (len(self.df) + page_size - 1) // page_size
            self.preview_page.end = total_pages
            
        except Exception as e:
            logger.error(f"Failed to update data preview: {e}")
    
    def update_column_selectors(self):
        """Update column selectors with enhanced categorization."""
        if not self.df:
            return
        
        try:
            columns = self.df.columns
            
            # Categorize columns
            numeric_cols = self.get_numeric_columns()
            categorical_cols = self.get_categorical_columns()
            datetime_cols = self.get_datetime_columns()
            
            # Update selectors with categorized options
            self.x_column.options = columns
            self.y_column.options = columns
            
            # Update filter column selector
            self.filter_panel[1][0].options = columns
            
        except Exception as e:
            logger.error(f"Failed to update column selectors: {e}")
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status display with enhanced styling."""
        status_classes = {
            "loading": "loading-spinner",
            "success": "success-message",
            "error": "error-message",
            "info": "status-card"
        }
        
        status_class = status_classes.get(status_type, "status-card")
        
        status_html = f"""
        <div class="{status_class}">
            <h3>📊 Status</h3>
            <p>{message}</p>
        </div>
        """
        
        self.status_panel[0].object = status_html
    
    def apply_advanced_filter(self, event):
        """Apply advanced filtering with multiple operators."""
        if not self.df or not self.filter_panel[1][0].value:
            return
        
        try:
            column = self.filter_panel[1][0].value
            operator = self.filter_panel[1][1].value
            value = self.filter_panel[1][2].value
            
            if not value:
                self.show_error("Please enter a filter value")
                return
            
            # Apply filter based on operator
            if operator == '==':
                self.df = self.df.filter(pl.col(column) == value)
            elif operator == '!=':
                self.df = self.df.filter(pl.col(column) != value)
            elif operator == '>':
                self.df = self.df.filter(pl.col(column) > float(value))
            elif operator == '<':
                self.df = self.df.filter(pl.col(column) < float(value))
            elif operator == '>=':
                self.df = self.df.filter(pl.col(column) >= float(value))
            elif operator == '<=':
                self.df = self.df.filter(pl.col(column) <= float(value))
            elif operator == 'contains':
                self.df = self.df.filter(pl.col(column).str.contains(value))
            elif operator == 'starts_with':
                self.df = self.df.filter(pl.col(column).str.starts_with(value))
            
            self.update_status(f"✅ Filter applied: {column} {operator} {value} ({len(self.df)} rows remaining)")
            self.update_data_preview()
            self.update_column_selectors()
            
        except Exception as e:
            self.show_error(f"Filter application failed: {str(e)}")
    
    def reset_filter(self, event):
        """Reset filter to original data."""
        if self.original_df is not None:
            self.df = self.original_df.clone()
            self.update_status("✅ Filter reset to original data")
            self.update_data_preview()
            self.update_column_selectors()
    
    def create_auto_plots(self, event=None):
        """Create automatic plots for data exploration."""
        if not self.df:
            return
        
        try:
            start_time = time.time()
            
            # Create subplots
            numeric_cols = self.get_numeric_columns()
            categorical_cols = self.get_categorical_columns()
            datetime_cols = self.get_datetime_columns()
            
            # Determine layout
            n_plots = len(numeric_cols) + len(categorical_cols) + len(datetime_cols)
            if n_plots == 0:
                self.show_error("No suitable columns found for automatic plotting")
                return
            
            cols = min(3, n_plots)
            rows = (n_plots + cols - 1) // cols
            
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=[f"Auto Plot {i+1}" for i in range(n_plots)],
                specs=[[{"secondary_y": False}] * cols] * rows
            )
            
            plot_idx = 0
            for col in numeric_cols[:n_plots]:
                row = plot_idx // cols + 1
                col_idx = plot_idx % cols + 1
                
                # Create histogram for numeric columns
                hist_data = self.df.select(pl.col(col)).to_pandas()[col].dropna()
                fig.add_histogram(
                    x=hist_data,
                    name=col,
                    row=row, col=col_idx
                )
                plot_idx += 1
            
            fig.update_layout(
                title="Automatic Data Exploration",
                height=400 * rows,
                showlegend=False
            )
            
            self.plot_area.object = fig
            self.plot_times.append(time.time() - start_time)
            self.update_status(f"✅ Auto plots created in {time.time() - start_time:.2f}s")
            
        except Exception as e:
            self.show_error(f"Auto plot creation failed: {str(e)}")
    
    def create_plot(self, event):
        """Create custom plot based on user selection."""
        if not self.df or not self.x_column.value:
            self.show_error("Please select at least an X-axis column")
            return
        
        try:
            start_time = time.time()
            
            x_col = self.x_column.value
            y_col = self.y_column.value
            plot_type = self.plot_type.value
            
            # Create plot based on type
            if plot_type == 'histogram':
                fig = self.create_histogram_plot(x_col)
            elif plot_type == 'scatter':
                if not y_col:
                    self.show_error("Scatter plot requires both X and Y columns")
                    return
                fig = self.create_scatter_plot(x_col, y_col)
            elif plot_type == 'box':
                fig = self.create_box_plot(x_col)
            elif plot_type == 'line':
                if not y_col:
                    self.show_error("Line plot requires both X and Y columns")
                    return
                fig = self.create_line_plot(x_col, y_col)
            elif plot_type == 'bar':
                fig = self.create_bar_plot(x_col, y_col)
            elif plot_type == 'violin':
                fig = self.create_violin_plot(x_col)
            elif plot_type == 'heatmap':
                if not y_col:
                    self.show_error("Heatmap requires both X and Y columns")
                    return
                fig = self.create_heatmap_plot(x_col, y_col)
            elif plot_type == '3d_scatter':
                if not y_col:
                    self.show_error("3D scatter plot requires both X and Y columns")
                    return
                fig = self.create_3d_scatter_plot(x_col, y_col)
            elif plot_type == 'surface':
                if not y_col:
                    self.show_error("Surface plot requires both X and Y columns")
                    return
                fig = self.create_surface_plot(x_col, y_col)
            else:
                self.show_error(f"Unknown plot type: {plot_type}")
                return
            
            self.plot_area.object = fig
            self.plot_times.append(time.time() - start_time)
            self.update_status(f"✅ {plot_type.title()} plot created in {time.time() - start_time:.2f}s")
            
        except Exception as e:
            self.show_error(f"Plot creation failed: {str(e)}")
    
    def get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns."""
        if not self.df:
            return []
        
        numeric_types = ['Int64', 'Float64', 'Int32', 'Float32', 'Int16', 'Float16', 'Int8']
        return [col for col in self.df.columns if str(self.df.schema[col]) in numeric_types]
    
    def get_categorical_columns(self) -> List[str]:
        """Get list of categorical columns."""
        if not self.df:
            return []
        
        categorical_types = ['Utf8', 'Categorical']
        return [col for col in self.df.columns if str(self.df.schema[col]) in categorical_types]
    
    def get_datetime_columns(self) -> List[str]:
        """Get list of datetime columns."""
        if not self.df:
            return []
        
        datetime_types = ['Datetime', 'Date', 'Time']
        return [col for col in self.df.columns if str(self.df.schema[col]) in datetime_types]
    
    def create_histogram_plot(self, column: str) -> go.Figure:
        """Create enhanced histogram plot."""
        data = self.df.select(pl.col(column)).to_pandas()[column].dropna()
        
        fig = go.Figure()
        fig.add_histogram(
            x=data,
            nbinsx=min(50, len(data) // 10),
            name=column,
            marker_color='#667eea'
        )
        
        fig.update_layout(
            title=f"Distribution of {column}",
            xaxis_title=column,
            yaxis_title="Frequency",
            template="plotly_white"
        )
        
        return fig
    
    def create_scatter_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create enhanced scatter plot."""
        data = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
        
        fig = go.Figure()
        fig.add_scatter(
            x=data[x_col],
            y=data[y_col],
            mode='markers',
            marker=dict(
                size=8,
                color=data[y_col],
                colorscale='Viridis',
                showscale=True
            ),
            name=f"{x_col} vs {y_col}"
        )
        
        fig.update_layout(
            title=f"{x_col} vs {y_col}",
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white"
        )
        
        return fig
    
    def create_box_plot(self, column: str) -> go.Figure:
        """Create enhanced box plot."""
        data = self.df.select(pl.col(column)).to_pandas()[column].dropna()
        
        fig = go.Figure()
        fig.add_box(
            y=data,
            name=column,
            marker_color='#667eea'
        )
        
        fig.update_layout(
            title=f"Box Plot of {column}",
            yaxis_title=column,
            template="plotly_white"
        )
        
        return fig
    
    def create_line_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create enhanced line plot."""
        data = self.df.select([pl.col(x_col), pl.col(y_col)]).sort(x_col).to_pandas()
        
        fig = go.Figure()
        fig.add_scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines+markers',
            name=f"{x_col} vs {y_col}",
            line=dict(color='#667eea', width=2)
        )
        
        fig.update_layout(
            title=f"Line Plot: {x_col} vs {y_col}",
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white"
        )
        
        return fig
    
    def create_bar_plot(self, x_col: str, y_col: str = None) -> go.Figure:
        """Create enhanced bar plot."""
        if y_col:
            data = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
            fig = go.Figure()
            fig.add_bar(
                x=data[x_col],
                y=data[y_col],
                marker_color='#667eea'
            )
            fig.update_layout(
                title=f"Bar Plot: {x_col} vs {y_col}",
                xaxis_title=x_col,
                yaxis_title=y_col
            )
        else:
            # Count plot
            counts = self.df.group_by(x_col).count().to_pandas()
            fig = go.Figure()
            fig.add_bar(
                x=counts[x_col],
                y=counts['count'],
                marker_color='#667eea'
            )
            fig.update_layout(
                title=f"Count Plot: {x_col}",
                xaxis_title=x_col,
                yaxis_title="Count"
            )
        
        fig.update_layout(template="plotly_white")
        return fig
    
    def create_violin_plot(self, column: str) -> go.Figure:
        """Create enhanced violin plot."""
        data = self.df.select(pl.col(column)).to_pandas()[column].dropna()
        
        fig = go.Figure()
        fig.add_violin(
            y=data,
            name=column,
            marker_color='#667eea'
        )
        
        fig.update_layout(
            title=f"Violin Plot of {column}",
            yaxis_title=column,
            template="plotly_white"
        )
        
        return fig
    
    def create_heatmap_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create enhanced heatmap plot."""
        # Create pivot table for heatmap
        pivot_data = self.df.group_by([x_col, y_col]).count().to_pandas()
        
        # Pivot to matrix format
        pivot_matrix = pivot_data.pivot(index=y_col, columns=x_col, values='count').fillna(0)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_matrix.values,
            x=pivot_matrix.columns,
            y=pivot_matrix.index,
            colorscale='Viridis'
        ))
        
        fig.update_layout(
            title=f"Heatmap: {x_col} vs {y_col}",
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white"
        )
        
        return fig
    
    def create_3d_scatter_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create 3D scatter plot."""
        # For 3D, we'll use a third column if available, otherwise use index
        numeric_cols = self.get_numeric_columns()
        z_col = None
        for col in numeric_cols:
            if col not in [x_col, y_col]:
                z_col = col
                break
        
        if z_col:
            data = self.df.select([pl.col(x_col), pl.col(y_col), pl.col(z_col)]).to_pandas()
            fig = go.Figure(data=go.Scatter3d(
                x=data[x_col],
                y=data[y_col],
                z=data[z_col],
                mode='markers',
                marker=dict(
                    size=5,
                    color=data[z_col],
                    colorscale='Viridis'
                )
            ))
            fig.update_layout(
                title=f"3D Scatter: {x_col} vs {y_col} vs {z_col}",
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title=z_col
                )
            )
        else:
            # Use index as Z-axis
            data = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
            fig = go.Figure(data=go.Scatter3d(
                x=data[x_col],
                y=data[y_col],
                z=list(range(len(data))),
                mode='markers',
                marker=dict(
                    size=5,
                    color=data[y_col],
                    colorscale='Viridis'
                )
            ))
            fig.update_layout(
                title=f"3D Scatter: {x_col} vs {y_col} vs Index",
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title="Index"
                )
            )
        
        return fig
    
    def create_surface_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create surface plot."""
        # Create a grid for surface plot
        data = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
        
        # Create meshgrid
        x_unique = sorted(data[x_col].unique())
        y_unique = sorted(data[y_col].unique())
        
        # For surface plot, we need a Z value - let's use count or mean
        pivot_data = data.groupby([x_col, y_col]).size().reset_index(name='count')
        pivot_matrix = pivot_data.pivot(index=y_col, columns=x_col, values='count').fillna(0)
        
        fig = go.Figure(data=go.Surface(
            z=pivot_matrix.values,
            x=pivot_matrix.columns,
            y=pivot_matrix.index,
            colorscale='Viridis'
        ))
        
        fig.update_layout(
            title=f"Surface Plot: {x_col} vs {y_col}",
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title="Count"
            )
        )
        
        return fig
    
    def export_data(self, event):
        """Export filtered data to CSV."""
        if not self.df:
            self.show_error("No data to export")
            return
        
        try:
            # Create export filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arrow_export_{timestamp}.csv"
            
            # Export to CSV
            self.df.write_csv(filename)
            
            self.update_status(f"✅ Data exported to {filename}")
            
        except Exception as e:
            self.show_error(f"Export failed: {str(e)}")
    
    def generate_report(self, event):
        """Generate comprehensive data report."""
        if not self.df:
            self.show_error("No data to analyze")
            return
        
        try:
            # Create report
            report = {
                "timestamp": datetime.now().isoformat(),
                "file_info": {
                    "rows": len(self.df),
                    "columns": len(self.df.columns),
                    "memory_usage_mb": self.df.estimated_size() / (1024 * 1024)
                },
                "schema": {},
                "statistics": {},
                "data_quality": {}
            }
            
            # Schema information
            for field in self.df.schema:
                report["schema"][field.name] = {
                    "dtype": str(field.dtype),
                    "null_count": self.df.select(pl.col(field.name).null_count()).item()
                }
            
            # Basic statistics for numeric columns
            numeric_cols = self.get_numeric_columns()
            for col in numeric_cols:
                stats = self.df.select([
                    pl.col(col).mean().alias("mean"),
                    pl.col(col).std().alias("std"),
                    pl.col(col).min().alias("min"),
                    pl.col(col).max().alias("max"),
                    pl.col(col).median().alias("median")
                ]).to_pandas()
                
                report["statistics"][col] = stats.iloc[0].to_dict()
            
            # Data quality metrics
            for col in self.df.columns:
                null_count = self.df.select(pl.col(col).null_count()).item()
                total_count = len(self.df)
                report["data_quality"][col] = {
                    "null_percentage": (null_count / total_count) * 100,
                    "completeness": ((total_count - null_count) / total_count) * 100
                }
            
            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"data_report_{timestamp}.json"
            
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.update_status(f"✅ Report generated: {report_filename}")
            
        except Exception as e:
            self.show_error(f"Report generation failed: {str(e)}")
    
    def analyze_memory(self, event):
        """Analyze memory usage and performance."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            analysis_html = f"""
            <div class="info-card">
                <h3>💾 Memory Analysis</h3>
                <p><strong>RSS Memory:</strong> {memory_info.rss / (1024 * 1024):.2f} MB</p>
                <p><strong>VMS Memory:</strong> {memory_info.vms / (1024 * 1024):.2f} MB</p>
                <p><strong>CPU Usage:</strong> {process.cpu_percent():.1f}%</p>
                <p><strong>Load Times:</strong> {len(self.load_times)} operations, avg: {np.mean(self.load_times):.3f}s</p>
                <p><strong>Plot Times:</strong> {len(self.plot_times)} operations, avg: {np.mean(self.plot_times):.3f}s</p>
            </div>
            """
            
            # Update the analysis tab
            self.tabs[2][1].object = analysis_html
            
            self.update_status("✅ Memory analysis completed")
            
        except Exception as e:
            self.show_error(f"Memory analysis failed: {str(e)}")
    
    def enable_controls(self):
        """Enable all controls after data is loaded."""
        self.export_panel[1][0].disabled = False
        self.export_panel[1][1].disabled = False
        self.export_panel[1][2].disabled = False
        self.filter_panel[1][4].disabled = False
    
    def show_error(self, message: str):
        """Show error message with styling."""
        error_html = f"""
        <div class="error-message">
            <strong>❌ Error:</strong> {message}
        </div>
        """
        
        # Show notification
        pn.state.notifications.error(message, duration=5000)
    
    def serve(self, port: int = 8080):
        """Serve the dashboard with enhanced configuration."""
        try:
            # Configure server
            pn.serve(
                self.layout,
                port=port,
                show=True,
                title="Arrow Data Explorer - Professional Edition",
                favicon="📊",
                address="localhost",
                allow_websocket_origin=["localhost", "127.0.0.1"],
                show_error_details=True
            )
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            print(f"❌ Failed to start server: {e}")
    
    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup_temp_files()

def main():
    """Main function to run the enhanced dashboard."""
    print("🚀 Starting Arrow Data Explorer - Professional Edition")
    print("=" * 60)
    
    try:
        # Create and run dashboard
        dashboard = ArrowDataExplorer()
        dashboard.serve(port=8080)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        logger.error(f"Dashboard startup failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 