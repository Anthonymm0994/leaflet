# Iteration 13: Mosaic-Inspired Linked Histograms

## Goal
Recreate the coordinated filtering and layout patterns from Mosaic examples:
- [Mosaic Gaia Example](https://idl.uw.edu/mosaic/examples/gaia.html)
- [Mosaic Flights 10M](https://observablehq.com/@uwdata/mosaic-cross-filter-flights-10m)

## Implementation
A fully offline, single-file HTML report with linked histograms and scatter plots using:
- **Base64-encoded Arrow data**
- **D3.js for brushing interactions**
- **Observable Plot for visualizations**
- **Central coordinator pattern** for filter management

## Features

### ✅ Implemented
1. **Linked Histograms**
   - Width distribution with brushing
   - Height distribution with brushing
   - Angle distribution with brushing
   - All histograms update when any filter changes

2. **Scatter Plot**
   - Width vs Height with angle coloring
   - Sampled to 5000 points for performance
   - Updates with all filter changes

3. **Category Bar Chart**
   - Click to filter by category
   - Shows distribution across category_5

4. **Coordinator Pattern**
   - Central filter state management
   - Builds SQL-ready WHERE clauses
   - Updates all views on filter change

5. **Interactive Features**
   - Brush selection on histograms
   - Click selection on categories
   - Reset button to clear all filters
   - Visual feedback for active filters

6. **Responsive Design**
   - Mosaic-style grid layout
   - Adapts to different screen sizes
   - Dark theme optimized for data

## Technical Details

### Architecture
```javascript
class Coordinator {
    filters = {}  // Central filter state
    
    setFilter(field, range) {
        // Update filter and notify all views
    }
    
    buildWhereClause() {
        // Convert filters to SQL WHERE clause
    }
    
    updateAll() {
        // Refresh all visualizations
    }
}
```

### Filter Types
- **Numerical**: `[min, max]` ranges for width, height, angle
- **Categorical**: Single value for category_5

### Performance Optimizations
- Scatter plot samples to 5000 points
- Efficient D3 brushing
- Minimal DOM updates

## Status
- ✅ **Core functionality complete**
- ✅ **All interactions working**
- ⏳ **DuckDB-JS integration pending** (using JS filtering for now)
- ⏳ **Radial angle plot pending**

## Next Steps
1. Integrate actual DuckDB-JS for SQL queries
2. Add radial visualization for angle
3. Implement time-based filtering (good_time)
4. Add density contours to scatter plot
5. Performance optimization for larger datasets

## Files
- `linked-histograms.html` - Main implementation (38.4 MB with embedded data)
- `README.md` - This documentation

## Usage
Simply open `linked-histograms.html` in a browser. No server required!

### Interactions
- **Brush** on any histogram to filter by range
- **Click** on category bars to filter
- **Reset** button appears when filters are active
- All views update automatically with coordinated filtering