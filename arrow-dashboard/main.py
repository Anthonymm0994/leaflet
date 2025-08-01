#!/usr/bin/env python3
"""
Arrow Data Explorer Dashboard
A standalone desktop application for exploring Apache Arrow files using polars and panel.
"""

import os
import sys
import tempfile
import gc
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import logging
import traceback

import pyarrow as pa
import polars as pl
import panel as pn
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Panel
pn.extension('plotly', sizing_mode='stretch_width')

class ArrowDataExplorer:
    """Main application class for Arrow data exploration dashboard."""
    
    def __init__(self):
        self.df: Optional[pl.DataFrame] = None
        self.file_path: Optional[str] = None
        self.original_df: Optional[pl.DataFrame] = None  # Keep original for reset
        self.temp_files: List[str] = []  # Track temp files for cleanup
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the dashboard UI components."""
        # File upload widget
        self.file_input = pn.widgets.FileInput(
            name='Upload Arrow File',
            accept='.arrow',
            width=300
        )
        self.file_input.param.watch(self.load_file, 'value')
        
        # Status display
        self.status_text = pn.pane.Markdown("## Status\nNo file loaded")
        
        # File info panel
        self.file_info = pn.pane.Markdown("### File Information\nNo file loaded")
        
        # Data preview
        self.data_preview = pn.pane.Markdown("### Data Preview\nNo data to display")
        
        # Column selector for plots
        self.x_column = pn.widgets.Select(name='X Axis Column', options=[])
        self.y_column = pn.widgets.Select(name='Y Axis Column', options=[])
        self.plot_type = pn.widgets.Select(
            name='Plot Type',
            options=['histogram', 'scatter', 'box', 'line', 'bar', 'violin', 'heatmap'],
            value='histogram'
        )
        
        # Filter controls
        self.filter_column = pn.widgets.Select(name='Filter Column', options=[])
        self.filter_value = pn.widgets.TextInput(name='Filter Value', placeholder='Enter value to filter')
        self.apply_filter_btn = pn.widgets.Button(name='Apply Filter', button_type='warning')
        self.apply_filter_btn.on_click(self.apply_filter)
        
        self.reset_filter_btn = pn.widgets.Button(name='Reset Filter', button_type='secondary')
        self.reset_filter_btn.on_click(self.reset_filter)
        self.reset_filter_btn.disabled = True
        
        # Plot controls
        self.plot_button = pn.widgets.Button(name='Create Plot', button_type='primary')
        self.plot_button.on_click(self.create_plot)
        
        # Export button
        self.export_button = pn.widgets.Button(name='Export to CSV', button_type='success')
        self.export_button.on_click(self.export_data)
        self.export_button.disabled = True
        
        # Memory usage display
        self.memory_info = pn.pane.Markdown("### Memory Usage\nNo data loaded")
        
        # Plot area
        self.plot_area = pn.pane.Plotly({})
        
        # Layout
        self.create_layout()
    
    def create_layout(self):
        """Create the main dashboard layout."""
        # Sidebar
        sidebar = pn.Column(
            pn.pane.Markdown("# 🌿 Arrow Data Explorer"),
            self.file_input,
            self.status_text,
            self.file_info,
            self.memory_info,
            pn.pane.Markdown("### Filter Controls"),
            self.filter_column,
            self.filter_value,
            pn.Row(self.apply_filter_btn, self.reset_filter_btn),
            pn.pane.Markdown("### Plot Controls"),
            self.x_column,
            self.y_column,
            self.plot_type,
            self.plot_button,
            self.export_button,
            width=350
        )
        
        # Main content area
        main_content = pn.Column(
            pn.pane.Markdown("## Data Preview"),
            self.data_preview,
            pn.pane.Markdown("## Visualizations"),
            self.plot_area,
            sizing_mode='stretch_width'
        )
        
        # Combine layout
        self.dashboard = pn.Row(sidebar, main_content)
    
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.info(f"Cleaned up temp file: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp file {temp_file}: {e}")
        self.temp_files.clear()
    
    def load_file(self, event):
        """Load an Arrow file and update the dashboard."""
        try:
            if not event.new:
                return
            
            self.update_status("Loading file...")
            
            # Clean up previous temp files
            self.cleanup_temp_files()
            
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(suffix='.arrow', delete=False) as tmp_file:
                tmp_file.write(event.new)
                self.file_path = tmp_file.name
                self.temp_files.append(tmp_file.name)
            
            # Load with pyarrow first
            logger.info(f"Loading Arrow file: {self.file_path}")
            table = pa.ipc.open_file(self.file_path).read_all()
            
            # Convert to polars DataFrame
            self.df = pl.from_arrow(table)
            self.original_df = self.df.clone()  # Keep original for reset
            
            # Update UI
            self.update_file_info()
            self.update_data_preview()
            self.update_column_selectors()
            self.update_memory_info()
            self.update_status("File loaded successfully!")
            self.export_button.disabled = False
            self.reset_filter_btn.disabled = True
            
            # Create initial plots
            self.create_auto_plots()
            
            # Force garbage collection
            gc.collect()
            
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            logger.error(traceback.format_exc())
            self.update_status(f"Error loading file: {str(e)}")
            self.cleanup_temp_files()
    
    def update_file_info(self):
        """Update the file information display."""
        if self.df is None:
            self.file_info.object = "### File Information\nNo file loaded"
            return
        
        try:
            info = f"""
### File Information
- **Rows**: {self.df.height:,}
- **Columns**: {self.df.width}
- **File**: {Path(self.file_path).name if self.file_path else 'Unknown'}
- **File Size**: {self.get_file_size()}

### Column Information
"""
            
            # Add column details
            for col in self.df.columns:
                col_info = self.df.select(pl.col(col))
                null_count = col_info.select(pl.col(col).null_count()).item()
                unique_count = col_info.select(pl.col(col).n_unique()).item()
                
                # Get data type info
                dtype = self.df.schema[col]
                dtype_str = str(dtype)
                
                info += f"- **{col}**: {dtype_str} (nulls: {null_count:,}, unique: {unique_count:,})\n"
            
            self.file_info.object = info
            
        except Exception as e:
            logger.error(f"Error updating file info: {e}")
            self.file_info.object = f"### File Information\nError: {str(e)}"
    
    def get_file_size(self) -> str:
        """Get file size in human readable format."""
        if not self.file_path or not os.path.exists(self.file_path):
            return "Unknown"
        
        size_bytes = os.path.getsize(self.file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def update_memory_info(self):
        """Update memory usage information."""
        if self.df is None:
            self.memory_info.object = "### Memory Usage\nNo data loaded"
            return
        
        try:
            # Estimate memory usage
            estimated_mb = self.df.estimated_size() / (1024 * 1024)
            
            info = f"""
### Memory Usage
- **Estimated DataFrame Size**: {estimated_mb:.1f} MB
- **Rows in Memory**: {self.df.height:,}
- **Columns in Memory**: {self.df.width}
"""
            
            self.memory_info.object = info
            
        except Exception as e:
            logger.error(f"Error updating memory info: {e}")
            self.memory_info.object = f"### Memory Usage\nError: {str(e)}"
    
    def update_data_preview(self):
        """Update the data preview display."""
        if self.df is None:
            self.data_preview.object = "### Data Preview\nNo data to display"
            return
        
        try:
            # Show first 10 rows
            preview_df = self.df.head(10)
            preview_html = preview_df.to_html()
            
            self.data_preview.object = f"""
### Data Preview
Showing first 10 rows of {self.df.height:,} total rows

{preview_html}
"""
            
        except Exception as e:
            logger.error(f"Error updating data preview: {e}")
            self.data_preview.object = f"### Data Preview\nError: {str(e)}"
    
    def update_column_selectors(self):
        """Update the column selector options."""
        if self.df is None:
            self.x_column.options = []
            self.y_column.options = []
            self.filter_column.options = []
            return
        
        try:
            columns = self.df.columns
            self.x_column.options = columns
            self.y_column.options = columns
            self.filter_column.options = columns
            
            # Set default selections
            if columns:
                self.x_column.value = columns[0]
                if len(columns) > 1:
                    self.y_column.value = columns[1]
                    
        except Exception as e:
            logger.error(f"Error updating column selectors: {e}")
    
    def update_status(self, message: str):
        """Update the status display."""
        self.status_text.object = f"## Status\n{message}"
        logger.info(f"Status: {message}")
    
    def apply_filter(self, event):
        """Apply filter to the data."""
        if self.df is None or not self.filter_column.value or not self.filter_value.value:
            self.update_status("Please select a column and enter a filter value")
            return
        
        try:
            column = self.filter_column.value
            filter_value = self.filter_value.value
            
            # Try to convert filter value to appropriate type
            try:
                # Check if it's numeric
                numeric_value = float(filter_value)
                filtered_df = self.df.filter(pl.col(column) == numeric_value)
            except ValueError:
                # Treat as string
                filtered_df = self.df.filter(pl.col(column) == filter_value)
            
            if filtered_df.height == 0:
                self.update_status(f"No rows match filter: {column} = {filter_value}")
                return
            
            self.df = filtered_df
            self.update_data_preview()
            self.update_file_info()
            self.update_memory_info()
            self.update_status(f"Applied filter: {column} = {filter_value} ({self.df.height:,} rows)")
            self.reset_filter_btn.disabled = False
            
            # Create new plots with filtered data
            self.create_auto_plots()
            
        except Exception as e:
            logger.error(f"Error applying filter: {e}")
            self.update_status(f"Error applying filter: {str(e)}")
    
    def reset_filter(self, event):
        """Reset filter to original data."""
        if self.original_df is None:
            return
        
        try:
            self.df = self.original_df.clone()
            self.update_data_preview()
            self.update_file_info()
            self.update_memory_info()
            self.update_status("Filter reset to original data")
            self.reset_filter_btn.disabled = True
            
            # Create new plots with original data
            self.create_auto_plots()
            
        except Exception as e:
            logger.error(f"Error resetting filter: {e}")
            self.update_status(f"Error resetting filter: {str(e)}")
    
    def create_auto_plots(self):
        """Create automatic plots for the loaded data."""
        if self.df is None:
            return
        
        try:
            # Create subplots for different visualizations
            plots = []
            
            # 1. Numeric columns histogram
            numeric_cols = self.get_numeric_columns()
            if numeric_cols:
                hist_plot = self.create_histogram_plot(numeric_cols[0])
                plots.append(hist_plot)
            
            # 2. Categorical columns value counts
            categorical_cols = self.get_categorical_columns()
            if categorical_cols:
                bar_plot = self.create_bar_plot(categorical_cols[0])
                plots.append(bar_plot)
            
            # 3. Time series if datetime columns exist
            datetime_cols = self.get_datetime_columns()
            if datetime_cols:
                time_plot = self.create_time_series_plot(datetime_cols[0])
                plots.append(time_plot)
            
            # Display plots
            if plots:
                self.plot_area.object = plots[0] if len(plots) == 1 else plots
            else:
                self.plot_area.object = go.Figure().add_annotation(
                    text="No suitable columns for automatic plotting",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
                
        except Exception as e:
            logger.error(f"Error creating auto plots: {e}")
            self.update_status(f"Error creating plots: {str(e)}")
    
    def create_plot(self, event):
        """Create a custom plot based on user selections."""
        if self.df is None or not self.x_column.value:
            return
        
        try:
            plot_type = self.plot_type.value
            x_col = self.x_column.value
            y_col = self.y_column.value
            
            if plot_type == 'histogram':
                fig = self.create_histogram_plot(x_col)
            elif plot_type == 'scatter':
                if not y_col:
                    self.update_status("Y column required for scatter plot")
                    return
                fig = self.create_scatter_plot(x_col, y_col)
            elif plot_type == 'box':
                fig = self.create_box_plot(x_col)
            elif plot_type == 'line':
                if not y_col:
                    self.update_status("Y column required for line plot")
                    return
                fig = self.create_line_plot(x_col, y_col)
            elif plot_type == 'bar':
                if not y_col:
                    self.update_status("Y column required for bar plot")
                    return
                fig = self.create_bar_plot(x_col, y_col)
            elif plot_type == 'violin':
                fig = self.create_violin_plot(x_col)
            elif plot_type == 'heatmap':
                if not y_col:
                    self.update_status("Y column required for heatmap")
                    return
                fig = self.create_heatmap_plot(x_col, y_col)
            else:
                self.update_status("Unknown plot type")
                return
            
            self.plot_area.object = fig
            self.update_status(f"Created {plot_type} plot")
            
        except Exception as e:
            logger.error(f"Error creating plot: {e}")
            self.update_status(f"Error creating plot: {str(e)}")
    
    def get_numeric_columns(self) -> List[str]:
        """Get list of numeric column names."""
        if self.df is None:
            return []
        
        numeric_types = [pl.Int64, pl.Int32, pl.Int16, pl.Int8, 
                        pl.Float64, pl.Float32, pl.UInt64, pl.UInt32, pl.UInt16, pl.UInt8]
        
        return [col for col in self.df.columns 
                if self.df.schema[col] in numeric_types]
    
    def get_categorical_columns(self) -> List[str]:
        """Get list of categorical column names."""
        if self.df is None:
            return []
        
        categorical_types = [pl.Utf8, pl.Categorical]
        
        return [col for col in self.df.columns 
                if self.df.schema[col] in categorical_types]
    
    def get_datetime_columns(self) -> List[str]:
        """Get list of datetime column names."""
        if self.df is None:
            return []
        
        datetime_types = [pl.Datetime, pl.Date, pl.Time]
        
        return [col for col in self.df.columns 
                if self.df.schema[col] in datetime_types]
    
    def create_histogram_plot(self, column: str) -> go.Figure:
        """Create a histogram plot for a numeric column."""
        if self.df is None:
            return go.Figure()
        
        try:
            # Convert to pandas for plotting
            pandas_df = self.df.select(pl.col(column)).to_pandas()
            
            fig = px.histogram(
                pandas_df, 
                x=column,
                title=f"Histogram: {column}",
                nbins=30
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating histogram: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating histogram: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_scatter_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create a scatter plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            pandas_df = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
            
            fig = px.scatter(
                pandas_df,
                x=x_col,
                y=y_col,
                title=f"Scatter Plot: {x_col} vs {y_col}"
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating scatter plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_box_plot(self, column: str) -> go.Figure:
        """Create a box plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            pandas_df = self.df.select(pl.col(column)).to_pandas()
            
            fig = px.box(
                pandas_df,
                y=column,
                title=f"Box Plot: {column}"
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating box plot: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating box plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_line_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create a line plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            pandas_df = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
            
            fig = px.line(
                pandas_df,
                x=x_col,
                y=y_col,
                title=f"Line Plot: {x_col} vs {y_col}"
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating line plot: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating line plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_bar_plot(self, x_col: str, y_col: str = None) -> go.Figure:
        """Create a bar plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            if y_col:
                # Bar plot with two columns
                pandas_df = self.df.select([pl.col(x_col), pl.col(y_col)]).to_pandas()
                fig = px.bar(
                    pandas_df,
                    x=x_col,
                    y=y_col,
                    title=f"Bar Plot: {x_col} vs {y_col}"
                )
            else:
                # Value counts for categorical column
                pandas_df = self.df.select(pl.col(x_col).value_counts()).to_pandas()
                fig = px.bar(
                    pandas_df,
                    x=x_col,
                    y='counts',
                    title=f"Value Counts: {x_col}"
                )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating bar plot: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating bar plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_violin_plot(self, column: str) -> go.Figure:
        """Create a violin plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            pandas_df = self.df.select(pl.col(column)).to_pandas()
            
            fig = px.violin(
                pandas_df,
                y=column,
                title=f"Violin Plot: {column}"
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating violin plot: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating violin plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_heatmap_plot(self, x_col: str, y_col: str) -> go.Figure:
        """Create a heatmap plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            # Create pivot table for heatmap
            pivot_df = self.df.group_by([x_col, y_col]).count().pivot(
                values="count",
                index=x_col,
                columns=y_col
            )
            
            pandas_df = pivot_df.to_pandas()
            
            fig = px.imshow(
                pandas_df,
                title=f"Heatmap: {x_col} vs {y_col}",
                aspect="auto"
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating heatmap: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def create_time_series_plot(self, datetime_col: str) -> go.Figure:
        """Create a time series plot."""
        if self.df is None:
            return go.Figure()
        
        try:
            # Get first numeric column for y-axis
            numeric_cols = self.get_numeric_columns()
            if not numeric_cols:
                return go.Figure()
            
            y_col = numeric_cols[0]
            pandas_df = self.df.select([pl.col(datetime_col), pl.col(y_col)]).to_pandas()
            
            fig = px.line(
                pandas_df,
                x=datetime_col,
                y=y_col,
                title=f"Time Series: {y_col} over {datetime_col}"
            )
            
            fig.update_layout(
                template="plotly_dark",
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating time series plot: {e}")
            return go.Figure().add_annotation(
                text=f"Error creating time series plot: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    def export_data(self, event):
        """Export the current data to CSV."""
        if self.df is None:
            return
        
        try:
            # Create export filename
            base_name = Path(self.file_path).stem if self.file_path else "exported_data"
            export_path = f"{base_name}_export.csv"
            
            # Export to CSV
            self.df.write_csv(export_path)
            
            self.update_status(f"Data exported to {export_path}")
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            self.update_status(f"Error exporting data: {str(e)}")
    
    def serve(self, port: int = 8080):
        """Serve the dashboard application."""
        logger.info(f"Starting Arrow Data Explorer on port {port}")
        
        # Set up the dashboard
        app = self.dashboard
        
        # Serve the application
        app.show(port=port, show=False)
        
        # Start the server
        pn.serve(app, port=port, show=True, title="Arrow Data Explorer")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.cleanup_temp_files()

def main():
    """Main application entry point."""
    print("🌿 Starting Arrow Data Explorer...")
    
    # Create and run the application
    app = ArrowDataExplorer()
    app.serve()

if __name__ == "__main__":
    main() 