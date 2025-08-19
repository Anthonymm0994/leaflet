# Data Explorer System

A high-performance, self-contained data exploration tool that can handle millions of rows while maintaining interactive performance. The system is designed to be generic and easily configurable for different datasets.

> **📁 See [ITERATIONS.md](ITERATIONS.md) for the complete evolution of this system through different versions.**

## Current Version: V3 - Embedded Working

This README describes the current working version (V3). For other iterations, see the `iterations/` folder.

## Features

- **High Performance**: Handles millions of rows with efficient data structures and batching
- **Self-Contained**: All JavaScript code is embedded in a single HTML file
- **Generic Design**: Works with any dataset structure
- **Interactive Charts**: Drag-to-filter histograms, categorical charts, and more
- **Real-time Filtering**: Apply multiple filters with instant visual feedback
- **Export Capabilities**: Export filtered data as CSV
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

The system is built as a single, self-contained HTML file with embedded JavaScript:

- **DataManager**: Efficient data storage using TypedArrays, automatic type inference, and pre-binning for performance
- **FilterManager**: Batch processing of filters with event-driven updates
- **ChartManager**: Extensible chart system with base Chart class and specialized implementations
- **DataExplorer**: High-level API for configuration and control

## Quick Start

### 1. Basic Usage

Simply open `data_explorer.html` in a web browser. The system will automatically initialize with sample data for testing.

### 2. Using Python to Load Data

The easiest way to use the explorer is with the Python data loader:

```bash
# Generate an HTML file from CSV data
python data_loader.py your_data.csv --title "Your Dataset" --output explorer.html

# Generate from JSON data
python data_loader.py your_data.json --title "Your Dataset" --output explorer.html

# Generate from Excel data
python data_loader.py your_data.xlsx --title "Your Dataset" --output explorer.html
```

### 3. Custom Configuration

You can also create custom configurations programmatically:

```python
from data_loader import DataExplorerConfig

config = DataExplorerConfig()
config.load_csv('your_data.csv')
config.set_title('Custom Title')
config.add_chart({
    'type': 'histogram',
    'column': 'age',
    'title': 'Age Distribution'
})
config.generate_html('custom_explorer.html')
```

## Chart Types

The system supports multiple chart types:

- **HistogramChart**: For numerical data with drag-to-filter functionality
- **CategoricalChart**: For string/categorical data with click-to-select
- **TimeChart**: Specialized histogram for time data
- **AngleChart**: Radial chart for angular data (framework ready)
- **ScatterChart**: Placeholder for scatter plots (framework ready)

## Performance Features

- **TypedArrays**: Uses `Float32Array` and `Int32Array` for efficient memory usage
- **Pre-binning**: Pre-calculates data bins for instant chart rendering
- **Batch Processing**: Applies filters in batches to maintain UI responsiveness
- **Sampling**: Uses data sampling for performance in large datasets
- **Canvas Rendering**: High-performance 2D graphics with HTML Canvas

## Data Types

The system automatically infers column types:

- **number**: Floating-point numerical data
- **integer**: Whole number data
- **time**: Time-based data (seconds, minutes, hours)
- **string**: Text data (automatically categorized if ≤20 unique values)

## Examples

### Basic Numerical Data
```bash
python data_loader.py test_data/test_data_numerical.csv --title "Employee Data"
```

### Time Series Data
```bash
python data_loader.py test_data/test_data_time.csv --title "Time Series Analysis"
```

### Categorical Data
```bash
python data_loader.py test_data/test_data_categorical.csv --title "Category Breakdown"
```

### Mixed Data Types
```bash
python data_loader.py test_data/test_data_mixed.csv --title "Mixed Dataset"
```

## Customization

### Chart Configuration
```python
chart_config = {
    'type': 'histogram',  # or 'categorical', 'time'
    'column': 'column_name',
    'title': 'Chart Title'
}
```

### Mini Metrics
```python
metrics = [
    {'id': 'filtered', 'label': 'Filtered Rows'},
    {'id': 'percent', 'label': 'of Total'},
    {'id': 'avg_column', 'label': 'Average Value'}
]
```

## File Structure

```
leaflet/
├── data_explorer.html          # Main explorer file (self-contained)
├── data_loader.py              # Python script for data loading
├── generate_test_data.py       # Generate test datasets
├── demo_explorer.py            # Generate demo explorers
├── test_explorer.py            # Automated testing
├── requirements.txt             # Python dependencies
├── test_data/                  # Test datasets and generated explorers
└── README.md                   # This file
```

## Requirements

- **Python**: 3.7+ with pandas, numpy
- **Browser**: Modern browser with ES6+ support
- **Data**: CSV, JSON, or Excel files

## Installation

```bash
pip install -r requirements.txt
```

## Testing

Run the automated tests to verify functionality:

```bash
python test_explorer.py
```

Generate test datasets:

```bash
python generate_test_data.py
```

## Performance Benchmarks

The system has been tested with:
- **50K rows**: Instant loading and filtering
- **500K rows**: Smooth interaction with <100ms filter response
- **1M+ rows**: Maintains responsiveness with sampling

## Contributing

The system is designed to be easily extensible:
- Add new chart types by extending the `Chart` base class
- Implement new data types in the `DataManager.inferType()` method
- Add new filter types in the `FilterManager` class

## License

This project is open source and available under the MIT License.
