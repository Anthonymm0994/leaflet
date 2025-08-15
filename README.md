# Modular Data Explorer

A high-performance, modular data exploration tool that can handle millions of rows while maintaining interactive performance. The system is designed to be generic and easily configurable for different datasets.

## Features

- **High Performance**: Handles millions of rows with efficient data structures and batching
- **Modular Architecture**: Clean separation of concerns with reusable components
- **Generic Design**: Works with any dataset structure
- **Interactive Charts**: Drag-to-filter histograms, categorical charts, and more
- **Real-time Filtering**: Apply multiple filters with instant visual feedback
- **Export Capabilities**: Export filtered data as CSV
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

The system is built with a modular architecture:

```
modules/
├── DataManager.js      # Handles data loading, storage, and operations
├── FilterManager.js    # Manages filtering logic and operations
├── ChartManager.js     # Creates and manages interactive charts
└── DataExplorer.js     # Main orchestrator and public API
```

### Key Components

- **DataManager**: Efficient data storage using TypedArrays, automatic type inference, and pre-binning for performance
- **FilterManager**: Batch processing of filters with event-driven updates
- **ChartManager**: Extensible chart system with base Chart class and specialized implementations
- **DataExplorer**: High-level API for configuration and control

## Quick Start

### 1. Basic Usage

Simply open `data_explorer.html` in a web browser. The system will automatically initialize with any embedded configuration.

### 2. Using Python to Load Data

The easiest way to use the explorer is with the Python data loader:

```bash
# Install dependencies
pip install -r requirements.txt

# Load CSV data and generate HTML
python data_loader.py your_data.csv --title "My Dataset Explorer"

# Load Excel data
python data_loader.py your_data.xlsx --format excel --title "Excel Data Explorer"

# Save configuration separately
python data_loader.py your_data.csv --config config.json --output explorer.html
```

### 3. Custom Configuration

You can also create custom configurations programmatically:

```python
from data_loader import DataExplorerConfig

# Create configuration
config = DataExplorerConfig()
config.load_csv("data.csv")
config.set_title("Custom Explorer")
config.add_chart({
    "type": "histogram",
    "column": "age",
    "title": "Age Distribution"
})

# Generate HTML
config.generate_html("custom_explorer.html")
```

## Configuration Format

The system uses a JSON configuration object:

```json
{
  "title": "Dataset Explorer",
  "columns": ["id", "name", "age", "category"],
  "data": [...],
  "columnTypes": {
    "id": "integer",
    "age": "number",
    "category": "string"
  },
  "chartTypes": [
    {
      "type": "histogram",
      "column": "age",
      "title": "Age Distribution"
    }
  ],
  "miniMetrics": [
    {"id": "filtered", "label": "Filtered Rows"},
    {"id": "avg_age", "label": "Average Age"}
  ]
}
```

### Column Types

- `"number"`: Floating-point numerical data
- `"integer"`: Integer numerical data
- `"string"`: Categorical or text data
- `"time"`: Time data (automatically detected from HH:MM:SS format)

### Chart Types

- `"histogram"`: For numerical data with range filtering
- `"time"`: For time data with time-based filtering
- `"categorical"`: For categorical data with selection filtering
- `"angle"`: For angular data (radial charts)
- `"scatter"`: For scatter plots (planned)

## Performance Features

### Data Optimization

- **TypedArrays**: Uses Float32Array and Uint8Array for efficient memory usage
- **Pre-binning**: Data is pre-binned for instant chart rendering
- **Sampling**: Large datasets use intelligent sampling for real-time updates
- **Batch Processing**: Filters are applied in batches to maintain responsiveness

### Rendering Optimization

- **Canvas-based**: High-performance 2D canvas rendering
- **RequestAnimationFrame**: Smooth chart updates
- **Event Batching**: Efficient event handling and updates

## Customization

### Adding New Chart Types

Extend the base `Chart` class:

```javascript
class CustomChart extends Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        // Custom initialization
    }
    
    draw() {
        // Custom drawing logic
    }
}

// Register with ChartManager
ChartManager.prototype.chartTypes.custom = CustomChart;
```

### Custom Filters

Create custom filter functions:

```javascript
// Custom filter function
const customFilter = (value) => value > 100;

// Apply to a column
filterManager.setFilter('column_name', filterManager.createCustomFilter(customFilter));
```

## API Reference

### DataExplorer

Main public API for controlling the explorer.

```javascript
// Initialize with configuration
DataExplorer.init(config);

// Update configuration
DataExplorer.updateConfig(newConfig);

// Get current state
const summary = DataExplorer.getDataSummary();

// Export data
DataExplorer.exportCSV();
```

### DataManager

Handles data operations and storage.

```javascript
// Get column data
const data = dataManager.getColumn('column_name');

// Get filtered data
const filtered = dataManager.getFilteredData('column_name');

// Get data statistics
const count = dataManager.getRowCount();
const filteredCount = dataManager.getFilteredCount();
```

### FilterManager

Manages filtering operations.

```javascript
// Apply range filter
filterManager.setFilter('column', [min, max]);

// Apply categorical filter
filterManager.setFilter('column', new Set(['cat1', 'cat2']));

// Apply custom filter
filterManager.setFilter('column', filterManager.createCustomFilter(fn));

// Apply all filters
filterManager.applyFilters();
```

## Browser Support

- **Modern Browsers**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **Features Used**: TypedArrays, Canvas API, ES6+ features
- **Performance**: Optimized for desktop and mobile devices

## Development

### Building

The system is pure JavaScript and HTML - no build step required. Simply:

1. Place all files in a web server directory
2. Ensure the `modules/` folder is accessible
3. Open the HTML file in a browser

### Testing

Test with various dataset sizes:

```python
# Generate test data
import pandas as pd
import numpy as np

# Create large test dataset
n_rows = 1000000
data = {
    'id': range(n_rows),
    'value': np.random.normal(100, 20, n_rows),
    'category': np.random.choice(['A', 'B', 'C'], n_rows),
    'time': [f"{h:02d}:{m:02d}:00" for h, m in zip(np.random.randint(0, 24, n_rows), np.random.randint(0, 60, n_rows))]
}

df = pd.DataFrame(data)
df.to_csv('test_data.csv', index=False)
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Areas for improvement:

- Additional chart types
- More export formats
- Enhanced filtering options
- Performance optimizations
- Mobile-specific features
