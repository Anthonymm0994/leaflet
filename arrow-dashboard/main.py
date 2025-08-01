#!/usr/bin/env python3
"""
🚀 Arrow Data Explorer - Professional Dashboard
A stunning, feature-rich desktop application for exploring Apache Arrow files.
"""

import os
import sys
import tempfile
import gc
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import logging
import traceback
from datetime import datetime
import json

# Try to import dependencies with graceful fallbacks
try:
    import pyarrow as pa
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    print("⚠️  PyArrow not available. Install with: pip install pyarrow")

try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    print("⚠️  Polars not available. Install with: pip install polars")

try:
    import panel as pn
    PANEL_AVAILABLE = True
except ImportError:
    PANEL_AVAILABLE = False
    print("⚠️  Panel not available. Install with: pip install panel")

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️  Plotly not available. Install with: pip install plotly")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy not available. Install with: pip install numpy")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  psutil not available. Install with: pip install psutil")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Beautiful CSS styling
BEAUTIFUL_CSS = """
<style>
/* Modern Dashboard Styling */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
    --white-color: #ffffff;
    --border-radius: 12px;
    --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.dashboard-container {
    max-width: 1400px;
    margin: 0 auto;
    background: var(--white-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    overflow: hidden;
}

.dashboard-header {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: var(--white-color);
    padding: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.3;
}

.dashboard-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.dashboard-header p {
    font-size: 1.2rem;
    margin: 10px 0 0 0;
    opacity: 0.9;
}

.dashboard-content {
    padding: 30px;
}

.card {
    background: var(--white-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid #e9ecef;
    transition: var(--transition);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #f8f9fa;
}

.card-icon {
    font-size: 1.5rem;
    margin-right: 15px;
    color: var(--primary-color);
}

.card-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--dark-color);
    margin: 0;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.metric-card {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: var(--white-color);
    border-radius: var(--border-radius);
    padding: 25px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: var(--transition);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    transition: var(--transition);
    opacity: 0;
}

.metric-card:hover::before {
    opacity: 1;
    transform: rotate(45deg) translate(50%, 50%);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.metric-label {
    font-size: 0.9rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.control-panel {
    background: var(--light-color);
    border-radius: var(--border-radius);
    padding: 25px;
    margin-bottom: 30px;
}

.control-section {
    margin-bottom: 25px;
}

.control-section h3 {
    color: var(--dark-color);
    margin-bottom: 15px;
    font-size: 1.1rem;
    font-weight: 600;
}

.button-group {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-primary {
    background: var(--primary-color);
    color: var(--white-color);
}

.btn-primary:hover {
    background: #5a6fd8;
    transform: translateY(-1px);
}

.btn-success {
    background: var(--success-color);
    color: var(--white-color);
}

.btn-success:hover {
    background: #218838;
    transform: translateY(-1px);
}

.btn-warning {
    background: var(--warning-color);
    color: var(--dark-color);
}

.btn-warning:hover {
    background: #e0a800;
    transform: translateY(-1px);
}

.btn-danger {
    background: var(--danger-color);
    color: var(--white-color);
}

.btn-danger:hover {
    background: #c82333;
    transform: translateY(-1px);
}

.btn-secondary {
    background: #6c757d;
    color: var(--white-color);
}

.btn-secondary:hover {
    background: #5a6268;
    transform: translateY(-1px);
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
}

.status-success {
    background: rgba(40, 167, 69, 0.1);
    color: var(--success-color);
    border: 1px solid rgba(40, 167, 69, 0.3);
}

.status-warning {
    background: rgba(255, 193, 7, 0.1);
    color: #856404;
    border: 1px solid rgba(255, 193, 7, 0.3);
}

.status-error {
    background: rgba(220, 53, 69, 0.1);
    color: var(--danger-color);
    border: 1px solid rgba(220, 53, 69, 0.3);
}

.status-info {
    background: rgba(23, 162, 184, 0.1);
    color: var(--info-color);
    border: 1px solid rgba(23, 162, 184, 0.3);
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.plot-container {
    background: var(--white-color);
    border-radius: var(--border-radius);
    padding: 25px;
    margin-top: 20px;
    box-shadow: var(--box-shadow);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--box-shadow);
}

.data-table th,
.data-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
}

.data-table th {
    background: var(--light-color);
    font-weight: 600;
    color: var(--dark-color);
}

.data-table tr:hover {
    background: #f8f9fa;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}

.pagination button {
    padding: 8px 16px;
    border: 1px solid #dee2e6;
    background: var(--white-color);
    color: var(--dark-color);
    border-radius: 6px;
    cursor: pointer;
    transition: var(--transition);
}

.pagination button:hover {
    background: var(--light-color);
}

.pagination button.active {
    background: var(--primary-color);
    color: var(--white-color);
    border-color: var(--primary-color);
}

.pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.tab-container {
    background: var(--white-color);
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--box-shadow);
}

.tab-header {
    display: flex;
    background: var(--light-color);
    border-bottom: 1px solid #dee2e6;
}

.tab-button {
    padding: 15px 25px;
    background: none;
    border: none;
    cursor: pointer;
    font-weight: 600;
    color: var(--dark-color);
    transition: var(--transition);
    border-bottom: 3px solid transparent;
}

.tab-button:hover {
    background: rgba(102, 126, 234, 0.1);
}

.tab-button.active {
    background: var(--white-color);
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
}

.tab-content {
    padding: 30px;
}

.alert {
    padding: 15px 20px;
    border-radius: var(--border-radius);
    margin-bottom: 20px;
    border-left: 4px solid;
}

.alert-success {
    background: rgba(40, 167, 69, 0.1);
    border-left-color: var(--success-color);
    color: #155724;
}

.alert-warning {
    background: rgba(255, 193, 7, 0.1);
    border-left-color: var(--warning-color);
    color: #856404;
}

.alert-error {
    background: rgba(220, 53, 69, 0.1);
    border-left-color: var(--danger-color);
    color: #721c24;
}

.alert-info {
    background: rgba(23, 162, 184, 0.1);
    border-left-color: var(--info-color);
    color: #0c5460;
}

/* Responsive Design */
@media (max-width: 768px) {
    .dashboard-content {
        padding: 20px;
    }
    
    .metrics-grid {
        grid-template-columns: 1fr;
    }
    
    .button-group {
        flex-direction: column;
        align-items: stretch;
    }
    
    .btn {
        justify-content: center;
    }
}

/* Animation for file upload */
.file-upload-area {
    border: 2px dashed var(--primary-color);
    border-radius: var(--border-radius);
    padding: 40px;
    text-align: center;
    background: rgba(102, 126, 234, 0.05);
    transition: var(--transition);
    cursor: pointer;
}

.file-upload-area:hover {
    background: rgba(102, 126, 234, 0.1);
    border-color: var(--secondary-color);
}

.file-upload-area.dragover {
    background: rgba(102, 126, 234, 0.2);
    border-color: var(--secondary-color);
    transform: scale(1.02);
}

/* Progress bar */
.progress-bar {
    width: 100%;
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    border-radius: 4px;
    transition: width 0.3s ease;
}

/* Tooltip */
.tooltip {
    position: relative;
    display: inline-block;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: var(--dark-color);
    color: var(--white-color);
    text-align: center;
    border-radius: 6px;
    padding: 8px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
"""

class ArrowDataExplorer:
    """Professional Arrow data exploration dashboard with stunning UI."""
    
    def __init__(self):
        self.df = None
        self.file_path = None
        self.original_df = None
        self.temp_files = []
        self.loading_state = False
        self.current_page = 1
        self.page_size = 10
        
        # Performance tracking
        self.load_times = []
        self.plot_times = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the beautiful dashboard UI."""
        # Header
        self.header = pn.pane.HTML(
            f"""
            {BEAUTIFUL_CSS}
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h1>🚀 Arrow Data Explorer</h1>
                    <p>Professional Apache Arrow File Analysis Dashboard</p>
                </div>
                <div class="dashboard-content">
            """,
            width=800
        )
        
        # File upload area
        self.file_upload = pn.pane.HTML(
            """
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📁</span>
                    <h2 class="card-title">Upload Arrow File</h2>
                </div>
                <div class="file-upload-area" id="file-upload-area">
                    <h3>📂 Drag & Drop Arrow Files Here</h3>
                    <p>or click to browse</p>
                    <p><small>Supports .arrow and .parquet files</small></p>
                </div>
            </div>
            """
        )
        
        # Status and metrics
        self.status_panel = pn.pane.HTML(
            """
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📊</span>
                    <h2 class="card-title">Status & Metrics</h2>
                </div>
                <div class="status-indicator status-info">
                    <span>⏳</span>
                    <span>Ready to load data</span>
                </div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">0</div>
                        <div class="metric-label">Rows</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">0</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">0 MB</div>
                        <div class="metric-label">Size</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">0</div>
                        <div class="metric-label">Null Values</div>
                    </div>
                </div>
            </div>
            """
        )
        
        # File information
        self.file_info = pn.pane.HTML(
            """
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📋</span>
                    <h2 class="card-title">File Information</h2>
                </div>
                <div class="alert alert-info">
                    <strong>ℹ️</strong> No file loaded. Upload an Arrow file to see detailed information.
                </div>
            </div>
            """
        )
        
        # Data preview
        self.data_preview = pn.pane.HTML(
            """
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">👀</span>
                    <h2 class="card-title">Data Preview</h2>
                </div>
                <div class="alert alert-info">
                    <strong>ℹ️</strong> No data to preview. Load a file to see the data.
                </div>
            </div>
            """
        )
        
        # Controls
        self.controls = pn.pane.HTML(
            """
            <div class="control-panel">
                <div class="control-section">
                    <h3>🎨 Visualization Controls</h3>
                    <div class="button-group">
                        <button class="btn btn-primary" onclick="createHistogram()">
                            📊 Histogram
                        </button>
                        <button class="btn btn-primary" onclick="createScatter()">
                            📈 Scatter Plot
                        </button>
                        <button class="btn btn-primary" onclick="createBoxPlot()">
                            📦 Box Plot
                        </button>
                        <button class="btn btn-primary" onclick="createBarPlot()">
                            📊 Bar Chart
                        </button>
                        <button class="btn btn-success" onclick="createAutoPlots()">
                            🚀 Auto Plots
                        </button>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>🔍 Data Filtering</h3>
                    <div class="button-group">
                        <button class="btn btn-warning" onclick="applyFilter()">
                            🔍 Apply Filter
                        </button>
                        <button class="btn btn-secondary" onclick="resetFilter()">
                            🔄 Reset Filter
                        </button>
                        <button class="btn btn-success" onclick="exportData()">
                            💾 Export CSV
                        </button>
                        <button class="btn btn-info" onclick="generateReport()">
                            📄 Generate Report
                        </button>
                    </div>
                </div>
            </div>
            """
        )
        
        # Plot area
        self.plot_area = pn.pane.HTML(
            """
            <div class="plot-container">
                <div class="card-header">
                    <span class="card-icon">📈</span>
                    <h2 class="card-title">Visualizations</h2>
                </div>
                <div class="alert alert-info">
                    <strong>ℹ️</strong> No plots available. Load data and create visualizations.
                </div>
            </div>
            """
        )
        
        # Footer
        self.footer = pn.pane.HTML(
            """
                </div>
            </div>
            <script>
                // Add interactive JavaScript here
                console.log('🚀 Arrow Data Explorer loaded successfully!');
            </script>
            """
        )
        
        # Create layout
        self.layout = pn.Column(
            self.header,
            self.file_upload,
            self.status_panel,
            self.file_info,
            self.data_preview,
            self.controls,
            self.plot_area,
            self.footer,
            sizing_mode='stretch_width'
        )
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status with beautiful styling."""
        status_classes = {
            "success": "status-success",
            "warning": "status-warning", 
            "error": "status-error",
            "info": "status-info"
        }
        
        icons = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "ℹ️"
        }
        
        status_class = status_classes.get(status_type, "status-info")
        icon = icons.get(status_type, "ℹ️")
        
        status_html = f"""
        <div class="status-indicator {status_class}">
            <span>{icon}</span>
            <span>{message}</span>
        </div>
        """
        
        # Update the status panel
        self.status_panel.object = f"""
        <div class="card">
            <div class="card-header">
                <span class="card-icon">📊</span>
                <h2 class="card-title">Status & Metrics</h2>
            </div>
            {status_html}
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{len(self.df) if self.df else 0}</div>
                    <div class="metric-label">Rows</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(self.df.columns) if self.df else 0}</div>
                    <div class="metric-label">Columns</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{self.get_file_size() if self.file_path else '0 MB'}</div>
                    <div class="metric-label">Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{self.get_null_count() if self.df else 0}</div>
                    <div class="metric-label">Null Values</div>
                </div>
            </div>
        </div>
        """
    
    def get_file_size(self) -> str:
        """Get formatted file size."""
        if not self.file_path or not os.path.exists(self.file_path):
            return "0 MB"
        
        size = os.path.getsize(self.file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def get_null_count(self) -> int:
        """Get total null count in dataframe."""
        if not self.df:
            return 0
        
        try:
            total_nulls = 0
            for col in self.df.columns:
                null_count = self.df.select(pl.col(col).null_count()).item()
                total_nulls += null_count
            return total_nulls
        except:
            return 0
    
    def load_file(self, file_data):
        """Load Arrow file with beautiful progress indication."""
        if not file_data:
            return
        
        self.loading_state = True
        self.update_status("🔄 Loading file...", "info")
        
        try:
            start_time = time.time()
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.arrow')
            temp_file.write(file_data)
            temp_file.close()
            self.temp_files.append(temp_file.name)
            
            # Load with pyarrow
            if PYARROW_AVAILABLE and POLARS_AVAILABLE:
                table = pa.ipc.open_file(temp_file.name).read_all()
                self.df = pl.from_arrow(table)
                self.original_df = self.df.clone()
                self.file_path = temp_file.name
                
                load_time = time.time() - start_time
                self.load_times.append(load_time)
                
                self.update_status(f"✅ File loaded successfully in {load_time:.2f}s", "success")
                self.update_file_info()
                self.update_data_preview()
            else:
                self.update_status("❌ Required dependencies not available", "error")
                
        except Exception as e:
            self.update_status(f"❌ Failed to load file: {str(e)}", "error")
        finally:
            self.loading_state = False
            gc.collect()
    
    def update_file_info(self):
        """Update file information with beautiful display."""
        if not self.df:
            return
        
        try:
            rows, cols = self.df.shape
            file_size = self.get_file_size()
            
            # Schema info
            schema_info = []
            for field in self.df.schema:
                null_count = self.df.select(pl.col(field.name).null_count()).item()
                schema_info.append(f"<tr><td><strong>{field.name}</strong></td><td>{field.dtype}</td><td>{null_count}</td></tr>")
            
            info_html = f"""
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📋</span>
                    <h2 class="card-title">File Information</h2>
                </div>
                <div class="alert alert-success">
                    <strong>✅</strong> File loaded successfully!
                </div>
                <table class="data-table">
                    <tr><th>Property</th><th>Value</th></tr>
                    <tr><td><strong>Rows</strong></td><td>{rows:,}</td></tr>
                    <tr><td><strong>Columns</strong></td><td>{cols}</td></tr>
                    <tr><td><strong>File Size</strong></td><td>{file_size}</td></tr>
                    <tr><td><strong>Memory Usage</strong></td><td>{self.df.estimated_size() / (1024 * 1024):.2f} MB</td></tr>
                </table>
                <h3>Schema Information</h3>
                <table class="data-table">
                    <tr><th>Column</th><th>Data Type</th><th>Null Count</th></tr>
                    {chr(10).join(schema_info)}
                </table>
            </div>
            """
            
            self.file_info.object = info_html
            
        except Exception as e:
            self.file_info.object = f"""
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📋</span>
                    <h2 class="card-title">File Information</h2>
                </div>
                <div class="alert alert-error">
                    <strong>❌</strong> Error updating file info: {str(e)}
                </div>
            </div>
            """
    
    def update_data_preview(self):
        """Update data preview with pagination."""
        if not self.df:
            return
        
        try:
            start_idx = (self.current_page - 1) * self.page_size
            end_idx = start_idx + self.page_size
            
            # Get preview data
            preview_df = self.df.slice(start_idx, self.page_size)
            
            # Convert to pandas for display
            if POLARS_AVAILABLE:
                preview_pandas = preview_df.to_pandas()
                
                # Create HTML table
                html_table = preview_pandas.to_html(
                    classes='data-table',
                    index=False,
                    float_format='%.3f'
                )
                
                total_pages = (len(self.df) + self.page_size - 1) // self.page_size
                
                preview_html = f"""
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">👀</span>
                        <h2 class="card-title">Data Preview</h2>
                    </div>
                    <div class="alert alert-success">
                        <strong>✅</strong> Showing rows {start_idx + 1}-{min(end_idx, len(self.df))} of {len(self.df):,}
                    </div>
                    {html_table}
                    <div class="pagination">
                        <button onclick="changePage({max(1, self.current_page - 1)})" {'disabled' if self.current_page == 1 else ''}>
                            ← Previous
                        </button>
                        <span>Page {self.current_page} of {total_pages}</span>
                        <button onclick="changePage({min(total_pages, self.current_page + 1)})" {'disabled' if self.current_page == total_pages else ''}>
                            Next →
                        </button>
                    </div>
                </div>
                """
                
                self.data_preview.object = preview_html
                
        except Exception as e:
            self.data_preview.object = f"""
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">👀</span>
                    <h2 class="card-title">Data Preview</h2>
                </div>
                <div class="alert alert-error">
                    <strong>❌</strong> Error updating data preview: {str(e)}
                </div>
            </div>
            """
    
    def create_plot(self, plot_type: str):
        """Create beautiful plots."""
        if not self.df:
            self.update_status("❌ No data loaded", "error")
            return
        
        try:
            start_time = time.time()
            
            # Get numeric columns for plotting
            numeric_cols = self.get_numeric_columns()
            if not numeric_cols:
                self.update_status("❌ No numeric columns found for plotting", "error")
                return
            
            # Create plot based on type
            if plot_type == "histogram":
                self.create_histogram_plot(numeric_cols[0])
            elif plot_type == "scatter":
                if len(numeric_cols) >= 2:
                    self.create_scatter_plot(numeric_cols[0], numeric_cols[1])
                else:
                    self.update_status("❌ Need at least 2 numeric columns for scatter plot", "error")
            elif plot_type == "box":
                self.create_box_plot(numeric_cols[0])
            elif plot_type == "bar":
                self.create_bar_plot(numeric_cols[0])
            else:
                self.update_status(f"❌ Unknown plot type: {plot_type}", "error")
                return
            
            plot_time = time.time() - start_time
            self.plot_times.append(plot_time)
            self.update_status(f"✅ {plot_type.title()} plot created in {plot_time:.2f}s", "success")
            
        except Exception as e:
            self.update_status(f"❌ Failed to create plot: {str(e)}", "error")
    
    def get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns."""
        if not self.df:
            return []
        
        numeric_types = ['Int64', 'Float64', 'Int32', 'Float32', 'Int16', 'Float16', 'Int8']
        return [col for col in self.df.columns if str(self.df.schema[col]) in numeric_types]
    
    def create_histogram_plot(self, column: str):
        """Create histogram plot."""
        if not PLOTLY_AVAILABLE:
            self.update_status("❌ Plotly not available for plotting", "error")
            return
        
        try:
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
                template="plotly_white",
                height=500
            )
            
            plot_html = f"""
            <div class="plot-container">
                <div class="card-header">
                    <span class="card-icon">📈</span>
                    <h2 class="card-title">Histogram: {column}</h2>
                </div>
                <div>{fig.to_html(full_html=False)}</div>
            </div>
            """
            
            self.plot_area.object = plot_html
            
        except Exception as e:
            self.update_status(f"❌ Failed to create histogram: {str(e)}", "error")
    
    def create_scatter_plot(self, x_col: str, y_col: str):
        """Create scatter plot."""
        if not PLOTLY_AVAILABLE:
            self.update_status("❌ Plotly not available for plotting", "error")
            return
        
        try:
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
                template="plotly_white",
                height=500
            )
            
            plot_html = f"""
            <div class="plot-container">
                <div class="card-header">
                    <span class="card-icon">📈</span>
                    <h2 class="card-title">Scatter Plot: {x_col} vs {y_col}</h2>
                </div>
                <div>{fig.to_html(full_html=False)}</div>
            </div>
            """
            
            self.plot_area.object = plot_html
            
        except Exception as e:
            self.update_status(f"❌ Failed to create scatter plot: {str(e)}", "error")
    
    def create_box_plot(self, column: str):
        """Create box plot."""
        if not PLOTLY_AVAILABLE:
            self.update_status("❌ Plotly not available for plotting", "error")
            return
        
        try:
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
                template="plotly_white",
                height=500
            )
            
            plot_html = f"""
            <div class="plot-container">
                <div class="card-header">
                    <span class="card-icon">📈</span>
                    <h2 class="card-title">Box Plot: {column}</h2>
                </div>
                <div>{fig.to_html(full_html=False)}</div>
            </div>
            """
            
            self.plot_area.object = plot_html
            
        except Exception as e:
            self.update_status(f"❌ Failed to create box plot: {str(e)}", "error")
    
    def create_bar_plot(self, column: str):
        """Create bar plot."""
        if not PLOTLY_AVAILABLE:
            self.update_status("❌ Plotly not available for plotting", "error")
            return
        
        try:
            # Count values for bar plot
            counts = self.df.group_by(column).count().to_pandas()
            
            fig = go.Figure()
            fig.add_bar(
                x=counts[column],
                y=counts['count'],
                marker_color='#667eea'
            )
            
            fig.update_layout(
                title=f"Value Counts: {column}",
                xaxis_title=column,
                yaxis_title="Count",
                template="plotly_white",
                height=500
            )
            
            plot_html = f"""
            <div class="plot-container">
                <div class="card-header">
                    <span class="card-icon">📈</span>
                    <h2 class="card-title">Bar Chart: {column}</h2>
                </div>
                <div>{fig.to_html(full_html=False)}</div>
            </div>
            """
            
            self.plot_area.object = plot_html
            
        except Exception as e:
            self.update_status(f"❌ Failed to create bar plot: {str(e)}", "error")
    
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
    
    def serve(self, port: int = 8080):
        """Serve the beautiful dashboard."""
        try:
            print("🚀 Starting Arrow Data Explorer - Professional Dashboard")
            print("=" * 60)
            print("📊 Dashboard will open in your browser")
            print("🎨 Beautiful UI with professional styling")
            print("📈 Interactive visualizations and analytics")
            print("=" * 60)
            
            # Configure Panel
            if PANEL_AVAILABLE:
                pn.extension('plotly', sizing_mode='stretch_width')
                
                # Serve the application
                pn.serve(
                    self.layout,
                    port=port,
                    show=True,
                    title="Arrow Data Explorer - Professional Edition",
                    favicon="📊",
                    address="localhost",
                    allow_websocket_origin=["localhost", "127.0.0.1"]
                )
            else:
                print("❌ Panel not available. Install with: pip install panel")
                
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            print(f"❌ Failed to start server: {e}")
    
    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup_temp_files()

def main():
    """Main function to run the professional dashboard."""
    print("🚀 Arrow Data Explorer - Professional Edition")
    print("=" * 60)
    
    # Check dependencies
    missing_deps = []
    if not PYARROW_AVAILABLE:
        missing_deps.append("pyarrow")
    if not POLARS_AVAILABLE:
        missing_deps.append("polars")
    if not PANEL_AVAILABLE:
        missing_deps.append("panel")
    if not PLOTLY_AVAILABLE:
        missing_deps.append("plotly")
    if not NUMPY_AVAILABLE:
        missing_deps.append("numpy")
    if not PSUTIL_AVAILABLE:
        missing_deps.append("psutil")
    
    if missing_deps:
        print("⚠️  Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n📦 Install with:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("\n🔄 Or install all requirements:")
        print("   pip install -r requirements.txt")
        return
    
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