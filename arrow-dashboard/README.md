# 🚀 Arrow Data Explorer - Professional Edition

A **standalone desktop dashboard application** for exploring Apache Arrow files with advanced analytics, professional UI, and robust data handling capabilities.

## ✨ Key Features

### 🎨 **Professional UI**
- **Modern Design**: Gradient headers, card-based layout, and professional styling
- **Tabbed Interface**: Organized into Dashboard, Controls, and Analysis tabs
- **Real-time Metrics**: Live performance tracking and memory analysis
- **Responsive Layout**: Adapts to different screen sizes and resolutions

### 📊 **Advanced Analytics**
- **Multiple Plot Types**: Histogram, scatter, box, line, bar, violin, heatmap, 3D scatter, surface plots
- **Auto Plot Generation**: Automatic data exploration with intelligent plot selection
- **Interactive Visualizations**: Zoom, pan, hover, and export capabilities
- **Statistical Analysis**: Comprehensive data quality and statistical reports

### 🔍 **Data Exploration**
- **Advanced Filtering**: Multiple operators (==, !=, >, <, >=, <=, contains, starts_with)
- **Pagination**: Navigate through large datasets efficiently
- **Column Categorization**: Automatic detection of numeric, categorical, and datetime columns
- **Data Preview**: Real-time table view with formatting

### 💾 **Export & Reporting**
- **CSV Export**: Export filtered data with timestamped filenames
- **JSON Reports**: Comprehensive data analysis reports
- **Memory Analysis**: Detailed performance metrics and memory usage
- **Data Quality Metrics**: Null percentage, completeness analysis

### ⚡ **Performance & Robustness**
- **Memory Management**: Explicit garbage collection and memory monitoring
- **Performance Tracking**: Load times, plot times, and operation metrics
- **Error Handling**: Graceful error recovery with user-friendly messages
- **Temporary File Cleanup**: Automatic cleanup of temporary files

## 🛠️ Technical Stack

- **Data Format**: Apache Arrow IPC files (`.arrow`)
- **Data Processing**: Polars (high-performance DataFrame library)
- **File Loading**: PyArrow for Arrow file reading
- **UI Framework**: Panel (interactive web applications)
- **Visualization**: Plotly (interactive plotting)
- **Packaging**: PyInstaller (standalone executable)
- **Performance**: psutil, numpy for system monitoring

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/Anthonymm0994/leaflet.git
cd leaflet/arrow-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python main.py
```

### Alternative: Automated Setup
```bash
# Run the automated setup script
python setup.py
```

## 🚀 Usage

### Starting the Dashboard
```bash
python main.py
```

The dashboard will open in your default browser at `http://localhost:8080`

### Basic Workflow
1. **Upload File**: Drag and drop or select an Arrow file
2. **Explore Data**: View file information, data preview, and statistics
3. **Create Visualizations**: Use the Controls tab to create custom plots
4. **Filter Data**: Apply advanced filters to focus on specific data
5. **Export Results**: Save filtered data or generate reports

### Advanced Features

#### 📊 Plot Types
- **Histogram**: Distribution analysis for numeric columns
- **Scatter**: Correlation analysis between two variables
- **Box Plot**: Statistical distribution and outliers
- **Line Plot**: Time series and trend analysis
- **Bar Plot**: Categorical data visualization
- **Violin Plot**: Density distribution analysis
- **Heatmap**: Correlation matrix and frequency analysis
- **3D Scatter**: Three-dimensional data exploration
- **Surface Plot**: Two-dimensional function visualization

#### 🔍 Filtering Options
- **Equality**: `==`, `!=` for exact matches
- **Comparison**: `>`, `<`, `>=`, `<=` for numeric ranges
- **Text Search**: `contains`, `starts_with` for string matching
- **Reset**: Restore original data at any time

#### 📈 Performance Metrics
- **Memory Usage**: Real-time RSS and VMS memory tracking
- **Load Times**: Average file loading performance
- **Plot Times**: Visualization generation metrics
- **CPU Usage**: System resource monitoring

## 📁 File Structure

```
arrow-dashboard/
├── main.py                 # Main dashboard application
├── requirements.txt        # Python dependencies
├── setup.py               # Automated setup script
├── run.bat               # Windows launcher
├── build_exe.py          # Executable builder
├── test_app.py           # Basic functionality tests
├── validate_dashboard.py  # Comprehensive validation
├── test_arrow_files.py   # Arrow file testing
└── README.md             # This file
```

## 🧪 Testing

### Basic Functionality Test
```bash
python test_app.py
```

### Comprehensive Validation
```bash
python validate_dashboard.py
```

### Arrow File Testing
```bash
python test_arrow_files.py
```

## 📦 Building Executable

### Automated Build
```bash
python build_exe.py
```

### Manual Build
```bash
pyinstaller --onefile --windowed --name=ArrowDataExplorer main.py
```

## 🔧 Configuration

### Environment Variables
- `PORT`: Dashboard port (default: 8080)
- `DEBUG`: Enable debug mode (default: False)

### Customization
- **CSS Styling**: Modify `CUSTOM_CSS` in `main.py`
- **Plot Themes**: Change `template="plotly_white"` to other themes
- **Color Schemes**: Update gradient colors in CSS classes

## 📊 Performance Considerations

### Memory Management
- **Large Files**: The dashboard handles files up to several GB
- **Garbage Collection**: Automatic cleanup after operations
- **Temporary Files**: Automatic cleanup of uploaded files

### Optimization Tips
- **Filter Early**: Apply filters before creating complex visualizations
- **Use Pagination**: Navigate large datasets efficiently
- **Monitor Memory**: Use the Analysis tab to track performance

## 🐛 Troubleshooting

### Common Issues

#### File Loading Errors
```bash
# Check file format
file your_file.arrow

# Verify Arrow file integrity
python -c "import pyarrow as pa; print(pa.ipc.open_file('your_file.arrow').schema)"
```

#### Memory Issues
- Close other applications to free memory
- Use filters to reduce dataset size
- Monitor memory usage in the Analysis tab

#### Plot Rendering Issues
- Check browser console for JavaScript errors
- Ensure Plotly is properly installed
- Try different plot types for problematic data

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
python main.py
```

## 📈 Advanced Usage

### Custom Plot Creation
```python
# Example: Create custom visualization
def create_custom_plot(self, data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['x'], y=data['y']))
    return fig
```

### Data Export Formats
- **CSV**: Standard comma-separated values
- **JSON**: Structured data with metadata
- **Reports**: Comprehensive analysis reports

### Integration with Other Tools
- **Jupyter**: Use as a backend for Jupyter notebooks
- **Streamlit**: Alternative UI framework integration
- **Dash**: Plotly-based dashboard integration

## 🤝 Contributing

### Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest test_app.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters
- Add docstrings for all functions
- Include error handling for robustness

## 📄 License

This project is part of the Leaflet Arrow Explorer suite. See the main repository for license information.

## 🙏 Acknowledgments

- **Polars**: High-performance DataFrame library
- **Panel**: Interactive web application framework
- **Plotly**: Interactive visualization library
- **PyArrow**: Apache Arrow Python bindings

## 📞 Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review existing issues in the repository
3. Create a new issue with detailed information
4. Include system information and error logs

---

**🚀 Ready to explore your Arrow data with professional-grade tools!** 