# Iteration 15: Vega-Lite Style Brushing & Linking

## Overview
Recreation of the Vega-Lite brushing and linking functionality from [this Observable notebook](https://observablehq.com/@weiglemc/brushing-and-linking-example-with-vega-lite), adapted for offline use with your embedded Arrow dataset.

## Implementation

### Key Features
1. **Scatter Plot**: Width vs Height, colored by angle
2. **Linked Histograms**: Width and Height distributions
3. **Brush Filtering**: Brush on histograms to filter the scatter plot
4. **Category Legend**: Click to filter by category_5 values
5. **Dual Display**: Shows both total data (gray) and filtered data (blue) in histograms
6. **Reset Button**: Clear all filters with one click

### Visual Design
- Clean, professional styling matching Vega-Lite aesthetics
- Light background with white chart containers
- Blue color scheme (#4c78a8) for selections
- Subtle shadows and borders
- Responsive layout

### Interactions
- **Brush on Histograms**: Creates a range filter that updates the scatter plot
- **Click Category Items**: Toggle category filtering
- **All Views Linked**: Changes in one view immediately update all others
- **Visual Feedback**: Active filters shown with badges and highlighting

## Technical Details

### Architecture
```javascript
class BrushLinkController {
    // Central controller manages all filter state
    filters = {
        width: null,      // [min, max] or null
        height: null,     // [min, max] or null
        categories: Set() // Selected categories
    }
    
    applyFilters() {
        // Filters data and updates all views
    }
}
```

### Data Flow
1. User interacts (brush/click)
2. Filter state updates
3. Data is filtered
4. All visualizations redraw
5. Statistics update

### Performance Optimizations
- Scatter plot samples to 3000 points max
- Efficient filtering with single pass
- Minimal DOM manipulation
- Smart brush handling

## Differences from Original

### What's Replicated
- Layout and visual style
- Brushing interaction on histograms
- Linked filtering behavior
- Category selection
- Overall user experience

### What's Different
- Uses Observable Plot instead of Vega-Lite
- Manual brush implementation with D3
- Simplified parameter system
- All offline, no external dependencies

## Usage

Open `brushing-linking.html` in any modern browser. No server required!

1. **Brush** on either histogram to select a range
2. **Click** category items to filter by category
3. **Observe** how all views update together
4. **Reset** to clear all filters

## File
- `brushing-linking.html` - Complete implementation (38.4 MB)