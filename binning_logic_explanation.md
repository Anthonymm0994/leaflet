# Binning Logic Explanation

This document explains how the binning logic works in the data visualization system, which is crucial for creating histograms and other frequency-based visualizations from large datasets.

## Overview

Binning is the process of grouping continuous data points into discrete intervals (bins) to create frequency distributions. This is essential for:
- Creating histograms
- Reducing data complexity for visualization
- Enabling interactive filtering and selection
- Performance optimization for large datasets

## Core Binning Functions

### 1. Regular Binning (`binData`)

The `binData` function handles standard numerical data binning:

```javascript
function binData(arr, min, max, numBins) {
    const bins = new Array(numBins).fill(null).map(() => []);
    const binSize = (max - min) / numBins;
    
    for (let i = 0; i < arr.length; i++) {
        const bin = Math.min(numBins - 1, Math.floor((arr[i] - min) / binSize));
        if (bin >= 0 && bin < numBins) bins[bin].push(i);
    }
    
    return { bins, binSize, min, max };
}
```

#### How it works:

1. **Initialize bins**: Create an array of `numBins` empty arrays
2. **Calculate bin size**: `(max - min) / numBins`
3. **Assign data points**: For each value, calculate which bin it belongs to
4. **Store indices**: Store the data point index in the appropriate bin

#### Example:

```javascript
// Sample data: [1.2, 3.7, 2.1, 4.8, 1.9]
// Range: min=1, max=5, numBins=4
// Bin size: (5-1)/4 = 1

// Bins created:
// Bin 0: [0, 4]  (values 1.2, 1.9)
// Bin 1: [2]     (value 2.1)  
// Bin 2: [1]     (value 3.7)
// Bin 3: [3]     (value 4.8)
```

### 2. Angle Binning (`binAngleData`)

The `binAngleData` function handles circular data (angles 0-360°):

```javascript
function binAngleData() {
    const numBins = 120;
    const bins = new Array(numBins).fill(null).map(() => []);
    const binSize = 360 / numBins;  // 3° per bin
    
    for (let i = 0; i < data.angle.length; i++) {
        const bin = Math.floor(data.angle[i] / binSize) % numBins;
        bins[bin].push(i);
    }
    
    // Calculate max count for this dataset
    let maxCount = 0;
    for (let i = 0; i < bins.length; i++) {
        maxCount = Math.max(maxCount, bins[i].length);
    }
    
    return { bins, binSize, numBins, maxCount };
}
```

#### Key differences from regular binning:

1. **Fixed range**: Always 0-360°
2. **Modulo operation**: `% numBins` ensures circular wrapping
3. **No clamping**: Values outside range wrap around naturally
4. **Predefined bins**: 120 bins = 3° per bin

#### Example:

```javascript
// Sample angles: [45°, 180°, 359°, 1°, 270°]
// 120 bins, 3° per bin

// Bins created:
// Bin 15: [0]   (45° / 3° = 15)
// Bin 60: [1]   (180° / 3° = 60)
// Bin 119: [2]  (359° / 3° = 119.67 → 119)
// Bin 0: [3]    (1° / 3° = 0.33 → 0)
// Bin 90: [4]   (270° / 3° = 90)
```

## Binning Process Flow

### 1. Data Preparation
```javascript
// Raw data arrays
data.width = [1.2, 3.7, 2.1, 4.8, 1.9, ...];
data.height = [10.5, 15.2, 12.8, 18.1, 11.3, ...];
data.angle = [45, 180, 359, 1, 270, ...];
```

### 2. Binning Execution
```javascript
// For each data field
binCache.width = binData(data.width, minWidth, maxWidth, 50);
binCache.height = binData(data.height, minHeight, maxHeight, 50);
binCache.angle = binAngleData(); // Special handling
```

### 3. Result Structure
```javascript
// Each bin contains array of data indices
{
    bins: [[0, 4], [2], [1], [3]], // Indices of data points
    binSize: 1.0,                   // Width of each bin
    min: 1,                         // Minimum value
    max: 5                          // Maximum value
}
```

## Edge Cases and Handling

### 1. Boundary Values
```javascript
// Regular binning: Clamps to prevent out-of-bounds
const bin = Math.min(numBins - 1, Math.floor((arr[i] - min) / binSize));

// Angle binning: Natural wrapping
const bin = Math.floor(data.angle[i] / binSize) % numBins;
```

### 2. Empty Bins
```javascript
// Bins with no data points remain empty arrays
bins[5] = []; // No data points in bin 5
```

### 3. Performance Considerations
- **Pre-binning**: Done once during initialization
- **Index storage**: Stores indices, not values (memory efficient)
- **TypedArrays**: Used for large datasets
- **Caching**: Results stored in `binCache` for reuse

## Visualization Integration

### 1. Histogram Rendering
```javascript
// For each bin, draw a bar
for (let i = 0; i < bins.length; i++) {
    const count = bins[i].length;
    const height = (count / maxCount) * chartHeight;
    // Draw bar with calculated height
}
```

### 2. Interactive Filtering
```javascript
// When user selects a range
const selectedBins = bins.slice(startBin, endBin);
const selectedIndices = selectedBins.flat(); // Flatten all indices
// Apply filter to data using selected indices
```

### 3. Tooltip Generation
```javascript
// Calculate bin range for display
const binStart = min + (binIndex * binSize);
const binEnd = binStart + binSize;
const count = bins[binIndex].length;
// Display: "1.0 - 2.0: 1,234 points"
```

## Performance Optimizations

### 1. Memory Efficiency
- Store indices instead of values
- Use `TypedArrays` for large datasets
- Reuse bin structures across renders

### 2. Computational Efficiency
- Pre-calculate bin assignments
- Cache results in `binCache`
- Use integer math for bin calculations

### 3. Rendering Optimization
- Only recalculate when data changes
- Batch rendering operations
- Use efficient Canvas operations

## Common Issues and Solutions

### 1. Edge Bin Clustering
**Problem**: Too many values in first/last bins
**Solution**: Remove clamping, let natural distribution occur

### 2. Uneven Bin Sizes
**Problem**: Bins appear too wide/narrow
**Solution**: Adjust `numBins` parameter for better resolution

### 3. Circular Data Wrapping
**Problem**: Angles don't wrap properly (359° ≠ 1°)
**Solution**: Use modulo operation in angle binning

### 4. Performance with Large Datasets
**Problem**: Binning becomes slow with millions of points
**Solution**: Use sampling, Web Workers, or pre-binning strategies

## Example Usage

```javascript
// Initialize binning for a dataset
const data = generateData(1000000); // 1M points
const binCache = {};

// Bin each field
binCache.width = binData(data.width, 0, 200, 50);
binCache.height = binData(data.height, 0, 100, 50);
binCache.angle = binAngleData();

// Use for visualization
const histogram = new Histogram('canvas', binCache.width);
histogram.draw(); // Renders using binned data
```

This binning system provides the foundation for efficient, interactive data visualization of large datasets while maintaining accuracy and performance. 