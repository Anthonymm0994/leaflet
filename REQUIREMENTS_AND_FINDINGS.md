# Offline Interactive Data Visualization Dashboard - Requirements & Findings

## Executive Summary

We need to build a fully offline, single-file HTML dashboard that can visualize and interactively filter 100,000+ data points using linked brushing across multiple histograms and scatter plots. The solution must work via the `file://` protocol without any external dependencies.

## Hard Requirements

1. **Single HTML File**: Everything must be embedded in one HTML file
2. **Fully Offline**: Must work via `file://` protocol with no network requests
3. **Large Dataset**: Handle 100,000+ records efficiently
4. **Interactive Filtering**: Click-and-drag brushing on histograms to filter all views
5. **Linked Visualizations**: 
   - 4 vertical histograms (age, income, rating, session_duration)
   - 1 scatter plot (age vs income)
   - All charts update when any histogram is brushed
6. **Visual Design**: Dark theme matching GitHub's design system
7. **Performance**: Smooth interactions even with large datasets
8. **Data Format**: Apache Arrow format (currently 28MB base64-encoded)

## Current Technical Constraints

### What Doesn't Work Offline

1. **DuckDB-WASM**: Requires Web Workers, SharedArrayBuffer, and separate files
2. **Module Imports**: ES6 imports fail on `file://` protocol
3. **Web Workers**: Cannot load external scripts from local files
4. **Large WASM Modules**: WebAssembly.instantiateStreaming blocked locally

### What Does Work

1. **Inline Scripts**: All JavaScript embedded as `<script>` tags
2. **Base64 Data**: Binary data encoded as base64 strings
3. **Blob URLs**: Can create workers/modules from inline code
4. **Pure JavaScript**: Libraries without WASM/Worker dependencies

## Proven Solution Stack

Based on extensive testing across 23 iterations:

1. **Data Processing**: Arquero (pure JavaScript, ~200KB)
2. **Visualization**: Vega-Lite (native brushing support, ~2MB with dependencies)
3. **Data Loading**: Apache Arrow JS (handles Arrow format, ~500KB)

## Ideal Solution Proposal

### Pre-computed Optimizations

Since bins can be calculated in advance:

1. **Pre-binned Data Structure**:
   ```javascript
   {
     // Original data for scatter plot and details
     raw_data: [...],
     
     // Pre-computed histogram bins
     histograms: {
       age: {
         bins: [
           { id: 0, min: 18, max: 20, count: 1250, indices: [0, 5, 12, ...] },
           { id: 1, min: 20, max: 22, count: 1340, indices: [1, 3, 7, ...] },
           // ... 30 bins total
         ]
       },
       income: { /* similar structure */ },
       rating: { /* similar structure */ },
       session_duration: { /* similar structure */ }
     },
     
     // Pre-computed statistics
     stats: {
       age: { min: 18, max: 75, mean: 35.2, std: 12.3 },
       income: { min: 10000, max: 200000, mean: 65000, std: 25000 },
       // ...
     }
   }
   ```

2. **Optimization Benefits**:
   - No runtime binning computation
   - Instant histogram rendering
   - Efficient filtering via bin indices
   - Smaller memory footprint

### Proposed Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HTML Container                        │
├─────────────────────────────────────────────────────────┤
│  Embedded Libraries (Base64/Inline):                    │
│  - Vega-Lite (for visualizations)                      │
│  - Arquero (for data filtering)                        │
│  - Arrow.js (for data loading)                         │
├─────────────────────────────────────────────────────────┤
│  Pre-processed Data (Base64):                           │
│  - Original Arrow data                                  │
│  - Pre-computed bins as JSON                           │
│  - Indices for efficient filtering                     │
├─────────────────────────────────────────────────────────┤
│  Visualization Layer:                                   │
│  - 4 Vega-Lite histograms with shared brush           │
│  - 1 Vega-Lite scatter plot                           │
│  - Coordinated through Vega signals                    │
└─────────────────────────────────────────────────────────┘
```

### Performance Optimizations

1. **Lazy Loading**: Load and render visible data first
2. **Virtual Scrolling**: For any data tables
3. **Canvas Rendering**: Use canvas instead of SVG for scatter plot
4. **Debounced Updates**: Throttle brush events
5. **Index-based Filtering**: Use pre-computed indices for fast filtering

## Open Questions for Other Models

1. **Alternative Visualization Libraries**:
   - Are there other libraries with native brushing that work offline?
   - Could we use WebGL-based libraries (e.g., deck.gl) offline?

2. **Data Compression**:
   - Should we use a different compression than gzip for the Arrow data?
   - Would Parquet format offer advantages despite browser limitations?

3. **Filtering Performance**:
   - Is there a more efficient data structure for multi-dimensional filtering?
   - Should we implement a custom bit-mask index for selections?

4. **Memory Management**:
   - How can we best handle 100k+ points without exhausting browser memory?
   - Should we implement data paging or progressive loading?

5. **Browser Compatibility**:
   - What's the minimum browser version we should target?
   - Are there polyfills needed for older browsers?

6. **User Experience**:
   - Should we add query saving/loading capabilities?
   - Would SQL-like filtering be valuable even without DuckDB?

## Specific Technical Challenges

1. **Brushing Coordination**:
   - How to efficiently propagate selections across views?
   - Should we use a central event bus or Vega's signal system?

2. **Large Dataset Rendering**:
   - When to use aggregation vs. sampling for scatter plots?
   - How to maintain responsiveness during brush operations?

3. **File Size**:
   - Current size is ~38MB - is this acceptable?
   - What's the practical limit for inline base64 data?

## Success Metrics

1. **Performance**: <100ms response time for brush interactions
2. **File Size**: Ideally under 50MB total
3. **Browser Support**: Chrome, Firefox, Safari (latest 2 versions)
4. **Load Time**: <5 seconds on modern hardware
5. **Memory Usage**: <500MB RAM for 100k points

## Next Steps

1. Implement pre-binning optimization
2. Test performance with full 100k dataset
3. Explore alternative compression methods
4. Consider progressive enhancement for larger datasets
5. Build production-ready version with all optimizations

## Request for Feedback

We're particularly interested in:

1. **Alternative approaches** we haven't considered
2. **Performance optimization** techniques for large datasets
3. **Compression strategies** for embedded data
4. **Browser-specific workarounds** for offline limitations
5. **User experience improvements** for data exploration

Please provide any insights on making this solution more efficient, maintainable, or user-friendly while maintaining the strict offline requirement.