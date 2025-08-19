# V3 - Embedded Modular Version

This version combines the best of both worlds: the self-contained nature of V1 with the clean modular architecture of V2, plus Python integration for data loading.

## Files Structure
```
v3-embedded/
├── data_explorer.html          # Self-contained explorer with embedded modules
├── data_loader.py              # Python script for data loading
├── generate_test_data.py       # Generate test datasets
├── demo_explorer.py            # Generate demo explorers
├── test_explorer.py            # Automated testing
├── requirements.txt            # Python dependencies
├── test_data/                  # Test datasets and generated explorers
└── README.md                   # This file
```

## Features
- ✅ **Self-Contained**: All JavaScript embedded in single HTML file
- ✅ **Modular Architecture**: Clean class structure within the file
- ✅ **Python Integration**: Load data from CSV, JSON, Excel
- ✅ **Configurable**: Generate explorers for any dataset
- ✅ **High Performance**: TypedArrays and efficient algorithms
- ✅ **All Chart Types**: Histogram, categorical, time, angle
- ✅ **Interactive**: Drag-to-filter, click-to-select
- ✅ **Export Functions**: CSV export, snapshots

## Architecture (Embedded)

The single HTML file contains modular JavaScript classes:

### DataManager
- Handles data loading and storage
- Automatic type inference
- Pre-binning for performance
- TypedArray optimization

### FilterManager  
- Manages filter state
- Batch filter application
- Event-driven updates
- Multiple filter types

### Chart Classes
- Base `Chart` class with common functionality
- `HistogramChart` for numerical data
- `CategoricalChart` for string data  
- `TimeChart` for time data
- `AngleChart` for angular data (planned)

### DataExplorer
- Main orchestrator
- UI management
- Stats and range updates
- Public API

## Usage

### Standalone (Sample Data)
```bash
open data_explorer.html
```

### With Your Data
```bash
# CSV data
python data_loader.py your_data.csv --title "Your Dataset" --output explorer.html

# Excel data  
python data_loader.py your_data.xlsx --title "Excel Data" --output explorer.html

# JSON data
python data_loader.py your_data.json --title "JSON Data" --output explorer.html
```

### Generate Test Data
```bash
python generate_test_data.py
```

### Run Tests
```bash
python test_explorer.py
```

### Generate Demos
```bash
python demo_explorer.py
```

## Python Integration

The `data_loader.py` script:
1. Loads data from various formats
2. Automatically infers column types
3. Generates appropriate chart configurations
4. Embeds data and config into HTML template
5. Creates self-contained explorer file

### Example Configuration
```python
from data_loader import DataExplorerConfig

config = DataExplorerConfig()
config.load_csv('data.csv')
config.set_title('My Dataset')
config.add_chart({
    'type': 'histogram',
    'column': 'age', 
    'title': 'Age Distribution'
})
config.generate_html('my_explorer.html')
```

## Data Types Supported
- **number**: Floating-point numerical data → Histogram charts
- **integer**: Whole number data → Histogram charts  
- **time**: Time data (auto-detected) → Time charts
- **string**: Text data → Categorical charts (if ≤20 unique values)

## Performance Features
- **TypedArrays**: `Float32Array`, `Int32Array` for memory efficiency
- **Pre-binning**: Data pre-processed for instant chart updates
- **Sampling**: Large datasets use intelligent sampling
- **Batch Processing**: Filters applied in batches
- **Canvas Rendering**: High-performance 2D graphics

## Benefits
- ✅ **Easy Deployment**: Single HTML file
- ✅ **No Dependencies**: Works in any modern browser
- ✅ **Portable**: Email, share, or host anywhere
- ✅ **Configurable**: Python script for any dataset
- ✅ **Maintainable**: Clean modular code structure
- ✅ **Performant**: Handles millions of rows

## Chart Interactions
- **Histograms**: Drag to select range, click to clear
- **Categories**: Click bars to select/deselect categories
- **Mini Mode**: Toggle compact dashboard view
- **Export**: Save filtered data as CSV
- **Snapshots**: Save current filter state as JSON

## Examples Generated
The system includes several example explorers:
- `demo_basic_numerical.html` - Employee dataset
- `demo_time_series.html` - Time-based data
- `demo_categorical.html` - Category analysis
- `demo_mixed.html` - Mixed data types
- `demo_large_dataset.html` - Performance test with 500K rows

## Status
✅ **Current Recommended Version** - Production ready
