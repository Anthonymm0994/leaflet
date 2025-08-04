# Smart Sampling Data Renderer

This iteration implements intelligent sampling strategies for the scatter plot while keeping full data fidelity in histograms.

## Key Features

### 1. **Full Data in Histograms**
- All 100k points are used for histogram calculations
- Accurate distribution representation
- No loss of statistical information

### 2. **Smart Sampling for Scatter Plot**
- **Uniform Random**: Simple random sampling
- **Stratified by Category**: Ensures all categories are represented proportionally
- **Density-preserving**: Maintains visual density patterns
- **No Sampling**: Option to show all points

### 3. **Adjustable Sample Size**
- Default: 5,000 points (smooth performance)
- Range: 100 to 100,000 points
- Real-time updates

### 4. **Fixed Arrow Data Access**
- Properly handles Arrow RecordBatch structure
- Converts Proxy objects to plain JavaScript objects
- No more schema access errors

## How It Works

1. **Histograms**: Always show the complete dataset
   - Background bars: Total data
   - Foreground bars: Filtered data
   - Brushing works on full data

2. **Scatter Plot**: Uses sampled data
   - Sampling happens after filtering
   - Different strategies preserve different aspects
   - Updates automatically with filter changes

## Sampling Strategies Explained

### Uniform Random
- Fastest method
- May miss rare patterns
- Good for general overview

### Stratified by Category
- Ensures each category is represented
- Maintains category proportions
- Best for category-colored plots

### Density-preserving
- Creates 2D bins and samples from each
- Maintains visual density patterns
- Good for finding clusters

## Performance

- 5,000 points: Very smooth interaction
- 10,000 points: Still responsive
- 50,000 points: Some lag but usable
- 100,000 points: Noticeable lag (use "No Sampling" option)

## Technical Notes

- No WebGL/GPU acceleration needed
- Pure SVG rendering via Observable Plot
- Canvas2D was considered but SVG is sufficient with sampling
- Efficient data structures minimize memory usage
