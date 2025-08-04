# Offline Data Visualization Dashboard

## Overview

This project evolved through 36 iterations to create a fully offline, self-contained HTML data visualization dashboard that works via the `file://` protocol with no external dependencies. The dashboard visualizes large datasets (100k+ points) using Apache Arrow data format with interactive brushing and linking capabilities.

## Final Solution

The best working solution is in **`builds/Iter 36 - final with stats/`**:
- `dashboard-with-stats.html` - Final dashboard with summary statistics
- `build_dashboard.py` - Reusable script to create dashboards from any Arrow file

### Key Features
- **Fully Offline**: All JavaScript libraries embedded directly in HTML
- **Interactive Brushing**: Select ranges on histograms with AND logic (intersect mode)
- **Linked Visualizations**: Selections update across all charts
- **Summary Statistics**: Real-time stats panel showing min, max, mean, median, std dev
- **Dynamic Axes**: Choose X/Y columns for scatter plot
- **Export Functionality**: Export selected or all data as CSV
- **Performance Optimized**: Handles 100k+ data points efficiently

## What We Learned

### 1. Module Loading Challenges
- **DuckDB-WASM**: Initially attempted but incompatible with `file://` protocol due to Web Worker and WASM loading restrictions
- **Solution**: Switched to simpler libraries that work with direct script tags

### 2. Data Format Evolution
- Started with direct Arrow.js usage (complex module loading issues)
- Moved to preprocessing Arrow data into TypedArrays with base64 encoding
- Final: Embedded preprocessed data for reliable offline usage

### 3. Visualization Libraries Journey
- **Observable Plot**: Good for basic charts but limited brushing capabilities
- **D3.js**: Too low-level for rapid development
- **Vega-Lite**: Winner - native brushing support and declarative syntax

### 4. Brushing Implementation
- Key insight: Brush parameter must be defined inside the first layer of repeat specification
- `resolve: "intersect"` enables AND logic between multiple selections
- Debounced updates possible but not always necessary

### 5. Performance Optimizations
- TypedArrays for efficient memory usage
- Sampling for scatter plots (adjustable 1k-20k points)
- Canvas renderer option for many points
- Pre-computed statistics where possible

## Technical Stack (Final)

- **Data**: Apache Arrow → TypedArrays (Float32Array, Uint32Array)
- **Visualization**: Vega-Lite 5 with Vega-Embed
- **Interactivity**: Native Vega-Lite brushing with intersect mode
- **Styling**: Dark theme with custom CSS
- **Export**: Client-side CSV generation

## Usage

### Using Existing Dashboard
Simply open `builds/Iter 36 - final with stats/dashboard-with-stats.html` in a web browser.

### Creating Custom Dashboard
```bash
cd builds/Iter 36 - final with stats
python build_dashboard.py path/to/data.arrow column1 column2 column3 --output my_dashboard.html
```

## Project Structure

```
leaflet/
├── data/                                 # Data files
│   ├── test_large_complex.arrow         # Original Arrow data
│   └── preprocessed_uncompressed.json   # Preprocessed TypedArray format
├── builds/                              # All iterations
│   ├── Iter 0-35/                      # Previous attempts and experiments
│   └── Iter 36 - final with stats/     # Final working solution
└── rough_idea.md                        # Original project concept
```

## Key Iterations

- **Iter 5**: First working Arquero-based solution
- **Iter 21**: Added interactive features and tooltips
- **Iter 25**: Implemented TypedArray preprocessing
- **Iter 27**: Discovered correct Vega-Lite brush pattern
- **Iter 32**: Validated linked brushing
- **Iter 35**: Multiple working patterns tested
- **Iter 36**: Final version with summary statistics

## Lessons for Future Projects

1. **Start Simple**: Complex module systems (ES modules, CommonJS) don't work well with `file://`
2. **Test Early**: Browser console is your friend for debugging
3. **Use CDNs for Testing**: But always inline for final offline version
4. **Vega-Lite is Powerful**: Handles most interactive visualization needs
5. **Preprocess When Possible**: Reduces runtime computation
6. **TypedArrays are Fast**: Much better than regular JavaScript arrays for large datasets

## Credits

Inspired by:
- [Observable Brushing and Linking Example](https://observablehq.com/@weiglemc/brushing-and-linking-example-with-vega-lite)
- [Mosaic](https://github.com/uwdata/mosaic) for coordinated views patterns
- Apache Arrow for efficient columnar data format