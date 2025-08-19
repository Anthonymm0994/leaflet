# V1 - Original Working Version

This is the original, fully functional data explorer as provided by the user.

## Files
- `data_explorer.html` - Complete working explorer (2025 lines)

## Features
- ✅ **10M Row Performance**: Handles 10 million rows efficiently
- ✅ **Interactive Charts**: Drag-to-filter histograms
- ✅ **Multiple Chart Types**: Time, strength, width, height, angle, categories
- ✅ **Real-time Filtering**: Instant visual feedback
- ✅ **Export Functions**: CSV export, snapshots
- ✅ **Mini Mode**: Compact view for dashboards
- ✅ **Statistics Panel**: Detailed stats overlay

## Chart Types
1. **Time Distribution** (24h) - Histogram with time formatting
2. **Strength Distribution** - Numerical histogram
3. **Width Distribution** - Numerical histogram  
4. **Height Distribution** - Numerical histogram
5. **Angle Distribution** - Radial/circular chart
6. **Category Distribution** - Bar chart with selection

## How to Use
```bash
# Simply open the file
open data_explorer.html
```

## Architecture
- **Single File**: Everything embedded in one HTML file
- **TypedArrays**: Float32Array for performance
- **Canvas Rendering**: High-performance 2D graphics
- **Batch Processing**: Efficient filtering of large datasets
- **Pre-binning**: Data pre-processed for instant chart updates

## Performance Features
- Handles 10M+ rows smoothly
- Sub-100ms filter response times
- Efficient memory usage with TypedArrays
- Sampling for real-time calculations
- RequestAnimationFrame for smooth updates

## Interactions
- **Drag to Filter**: Click and drag on histograms to select ranges
- **Click to Select**: Click on categorical charts to select/deselect
- **Reset**: Click charts to clear individual filters
- **Export**: Save filtered data as CSV

## Status
✅ **Reference Implementation** - Fully working, high-performance baseline
