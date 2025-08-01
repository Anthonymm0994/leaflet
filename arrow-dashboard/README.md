# 🌿 Arrow Data Explorer Dashboard

A **robust, production-ready** standalone desktop application for exploring Apache Arrow files using **polars** and **panel**. Built with Python and packaged as a standalone executable.

## 🚀 Enhanced Features

- **🔒 Robust File Loading**: Comprehensive error handling and memory management
- **📊 Advanced Visualizations**: Histograms, scatter plots, box plots, line charts, bar charts, violin plots, heatmaps
- **🔍 Data Filtering**: Interactive filtering with reset functionality
- **📈 Memory Monitoring**: Real-time memory usage tracking
- **💾 File Information**: Detailed file size, row/column counts, null values, data types
- **📋 Data Preview**: Formatted table display with sample data
- **📤 Export Functionality**: CSV export with smart naming
- **🎨 Responsive UI**: Clean, modern interface with sidebar controls
- **⚡ Performance Optimized**: Efficient data processing with polars

## 📋 Requirements

### Development Environment
- Python 3.8+
- pip (Python package manager)

### Runtime Dependencies
- **pyarrow** >= 14.0.0 (Apache Arrow file reading)
- **polars** >= 0.20.0 (High-performance DataFrame operations)
- **panel** >= 1.4.0 (Web dashboard framework)
- **plotly** >= 5.17.0 (Interactive plotting)
- **numpy** >= 1.24.0 (Numerical computing)
- **psutil** >= 5.9.0 (System monitoring)
- **pyinstaller** >= 6.0.0 (Executable packaging)

## 🛠️ Installation & Setup

### 1. Quick Start
```bash
# Navigate to the arrow-dashboard directory
cd arrow-dashboard

# Run automated setup
python setup.py

# Start the application
python main.py
```

### 2. Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_app.py

# Start application
python main.py
```

The dashboard will open in your default web browser at `http://localhost:8080`

## 📦 Building Standalone Executable

### Automated Build
```bash
python build_exe.py
```

### Manual Build
```bash
pyinstaller --onefile --windowed --name=ArrowDataExplorer main.py
```

### Build Output
- **Executable**: `dist/ArrowDataExplorer.exe`
- **Size**: ~50-100MB (includes all dependencies)
- **Distribution**: Single file, no Python installation required

## 🎯 Usage Guide

### 1. Loading Data
1. Click "Upload Arrow File" in the sidebar
2. Select your `.arrow` file
3. The dashboard automatically loads and displays comprehensive file information

### 2. Exploring Data
- **File Info**: View row/column counts, data types, null values, file size
- **Memory Usage**: Monitor real-time memory consumption
- **Data Preview**: See first 10 rows in a formatted table
- **Auto Plots**: Automatic visualizations based on data types

### 3. Filtering Data
1. Select a column from "Filter Column" dropdown
2. Enter a filter value in "Filter Value" text box
3. Click "Apply Filter" to filter the data
4. Use "Reset Filter" to return to original data

### 4. Creating Custom Visualizations
1. Select X-axis column from dropdown
2. Select Y-axis column (if needed)
3. Choose plot type (histogram, scatter, box, line, bar, violin, heatmap)
4. Click "Create Plot"

### 5. Exporting Data
- Click "Export to CSV" to save the current dataset
- File will be saved as `{filename}_export.csv`

## 🏗️ Enhanced Architecture

### Core Components
- **`main.py`**: Enhanced main application with robust error handling
- **`ArrowDataExplorer`**: Main application class with memory management
- **Panel UI**: Web-based dashboard interface with responsive design
- **Polars DataFrame**: High-performance data processing engine
- **Plotly**: Interactive visualization library with multiple chart types

### Data Flow
1. **File Upload** → Temporary file storage with cleanup
2. **pyarrow** → Read Arrow IPC file with error handling
3. **polars** → Convert to DataFrame with memory optimization
4. **Panel** → Display in web interface with real-time updates
5. **Plotly** → Create interactive charts with error recovery
6. **Export** → CSV file output with smart naming

### Key Design Decisions
- **polars over pandas**: Better performance for large datasets
- **panel over dash**: Simpler setup, better integration
- **pyarrow IPC**: Native Arrow file format support
- **plotly**: Rich interactive visualizations
- **Memory Management**: Automatic cleanup and garbage collection
- **Error Handling**: Comprehensive exception management

## 🔧 Technical Details

### File Format Support
- **Primary**: Apache Arrow IPC files (`.arrow`)
- **Export**: CSV format
- **Future**: Parquet, Feather, JSON

### Data Type Detection
- **Numeric**: Int64, Int32, Int16, Int8, Float64, Float32, UInt64, UInt32, UInt16, UInt8
- **Categorical**: Utf8, Categorical
- **Temporal**: Datetime, Date, Time
- **Boolean**: Boolean

### Plot Types
- **Histogram**: Distribution of numeric values
- **Scatter**: Correlation between two numeric columns
- **Box Plot**: Statistical distribution with outliers
- **Line Chart**: Time series or sequential data
- **Bar Chart**: Categorical data or value counts
- **Violin Plot**: Distribution shape and density
- **Heatmap**: Correlation matrix or pivot table visualization

### Memory Management
- **Automatic Cleanup**: Temporary files are automatically removed
- **Garbage Collection**: Forced GC after large operations
- **Memory Monitoring**: Real-time memory usage tracking
- **Optimized Loading**: Efficient data loading with polars

## 🧪 Testing & Validation

### Test Suites
- **`test_app.py`**: Basic functionality and dependency testing
- **`test_arrow_files.py`**: Comprehensive Arrow file testing
- **`validate_dashboard.py`**: Dashboard validation with real datasets

### Test Coverage
- **Import Testing**: All dependency verification
- **File Loading**: Arrow file creation and loading
- **Application Initialization**: Core component validation
- **Data Processing**: DataFrame operations testing
- **Memory Management**: Memory efficiency testing
- **Error Handling**: Edge cases and error conditions
- **Performance**: Load time and memory usage benchmarks

### Running Tests
```bash
# Basic tests
python test_app.py

# Arrow file tests
python test_arrow_files.py

# Dashboard validation
python validate_dashboard.py

# Stress testing (optional)
STRESS_TEST=true python test_arrow_files.py
```

## 📈 Performance Characteristics

### Memory Usage
- **Base Application**: ~50MB RAM
- **Data Loading**: 2x file size recommended
- **Large Files**: Optimal for < 500MB datasets
- **Memory Monitoring**: Real-time tracking with cleanup

### Processing Speed
- **File Loading**: Near-instant for typical files
- **Visualization**: Real-time plot generation
- **Export**: Fast CSV generation
- **Filtering**: Immediate response with polars

### Scalability
- **Small Files**: < 1MB - Instant loading
- **Medium Files**: 1-100MB - Fast loading with memory monitoring
- **Large Files**: 100MB-500MB - Optimized loading with cleanup
- **Very Large Files**: > 500MB - Consider data sampling

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 2. Port already in use
```bash
# Change port in main.py
app.serve(port=8081)  # Use different port
```

#### 3. Large file loading issues
- The application loads entire files into memory
- For very large files (>1GB), consider data sampling
- Monitor system memory usage with the memory display

#### 4. Memory issues
- Check the memory usage display in the sidebar
- Use the reset filter button to free memory
- Restart the application if memory usage is high

#### 5. PyInstaller build failures
```bash
# Clean and rebuild
rm -rf build dist __pycache__
python build_exe.py
```

### Performance Tips
- **File Size**: Optimal for files < 500MB
- **Memory**: Ensure 2x file size available RAM
- **CPU**: Multi-core processing for large datasets
- **Network**: Local file access recommended
- **Filtering**: Use filters to reduce memory usage

## 🔮 Future Enhancements

### Planned Features
- [ ] Data filtering and subsetting (✅ Implemented)
- [ ] Advanced statistical analysis
- [ ] Multiple file comparison
- [ ] Custom plot configurations
- [ ] Data transformation tools
- [ ] Export to multiple formats
- [ ] Lazy loading for large files
- [ ] Caching for better performance

### Technical Improvements
- [ ] Plugin system for custom visualizations
- [ ] Dark/light theme toggle
- [ ] Responsive mobile interface
- [ ] Advanced memory optimization
- [ ] Parallel processing for large datasets

## 📄 License

This project is open source. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with the validation scripts
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages in the console
3. Run the validation scripts to identify issues
4. Create an issue with detailed information

---

**🌿 Arrow Data Explorer - A robust, production-ready data exploration dashboard for Apache Arrow files**

### 🏆 Key Achievements

- **✅ Complete Arrow File Support**: Native Apache Arrow IPC format handling
- **✅ High Performance**: Optimized with polars for large datasets
- **✅ Robust Error Handling**: Comprehensive exception management
- **✅ Memory Management**: Automatic cleanup and monitoring
- **✅ Interactive Visualizations**: Multiple chart types with real-time updates
- **✅ Data Filtering**: Interactive filtering with reset functionality
- **✅ Export Capabilities**: CSV export with smart naming
- **✅ Standalone Executable**: Single file distribution
- **✅ Comprehensive Testing**: Multiple test suites for validation
- **✅ Production Ready**: Professional-grade application with documentation 