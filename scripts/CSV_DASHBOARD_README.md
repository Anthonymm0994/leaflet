# CSV to Interactive Dashboard Generator

This tool converts any CSV file into an interactive, self-contained HTML dashboard with multiple linked visualizations, identical to the real_next_best_yet.html dashboard.

## Features

- **Fully Offline**: All data is embedded directly in the HTML file - no external dependencies
- **Interactive Visualizations**: 
  - 4 linked histograms (customizable data columns)
  - 1 radial/angle chart (0-360 degrees)
  - 1-2 category bar charts
  - Real-time statistics panel
- **Cross-filtering**: Click and drag on any chart to filter all others
- **Multi-selection**: Click category bars to select/deselect
- **Mini/Mega Mode**: Zoom into filtered data subsets
- **CSV Export**: Export all selected data (no limits)
- **Performance**: Handles millions of rows efficiently using typed arrays

## Installation

```bash
pip install pandas numpy htmlmin
```

## Usage

### Basic Usage

```bash
python csv_to_dashboard.py input.csv output.html \
    --time time_column \
    --width width_column \
    --height height_column \
    --angle angle_column \
    --strength strength_column \
    --category category_column
```

### Full Example

```bash
python csv_to_dashboard.py sales_data.csv sales_dashboard.html \
    --time timestamp \
    --width revenue \
    --height quantity \
    --angle day_of_year \
    --strength satisfaction_score \
    --category product_category \
    --category2 is_premium \
    --compress
```

### Parameters

- `input_csv`: Path to your CSV file
- `output_html`: Path for the generated dashboard
- `--time`: Column containing time data (24-hour format, e.g., "14:30:45")
- `--width`: Column for the first histogram (numeric)
- `--height`: Column for the second histogram (numeric)
- `--angle`: Column for angle data (0-360 degrees)
- `--strength`: Column for the fourth histogram (numeric)
- `--category`: Column for categorical data (will show as bar chart)
- `--category2`: (Optional) Secondary category column (binary/boolean)
- `--compress`: (Optional) Generate a minified version
- `--sample-size`: (Optional) Sample N rows for testing

## Data Requirements

### Time Column
- Accepts formats: "HH:MM:SS", "HH:MM", or numeric seconds
- Automatically converts to seconds since midnight
- Example: "14:30:45", "14:30", or 52245

### Numeric Columns (width, height, strength)
- Any numeric data
- Handles NaN values (replaces with column mean)
- Automatically determines min/max ranges

### Angle Column
- Values should be 0-360 degrees
- Values outside range are wrapped (e.g., 370 → 10)

### Category Columns
- Any text or numeric categories
- Automatically maps to indices
- Supports any number of unique values

## Output

The tool generates:
1. `output.html` - Full dashboard with embedded data
2. `output-compressed.html` - Minified version (if --compress used)

## File Sizes

- 10K rows → ~350 KB HTML
- 100K rows → ~2.9 MB HTML  
- 1M rows → ~29 MB HTML
- 3M rows → ~84 MB HTML
- 5M rows → ~140 MB HTML

## Performance Tips

1. **Large Files**: For files over 1M rows, consider sampling:
   ```bash
   python csv_to_dashboard.py large.csv dashboard.html --sample-size 1000000 ...
   ```

2. **Compression**: Use `--compress` to reduce file size slightly

3. **Browser Limits**: Most browsers handle up to 10M rows well

## Examples

### Example 1: Sales Data
```bash
python csv_to_dashboard.py sales_2024.csv sales_dashboard.html \
    --time sale_time \
    --width sale_amount \
    --height items_sold \
    --angle day_of_week \
    --strength customer_rating \
    --category product_type \
    --category2 is_return
```

### Example 2: Sensor Data
```bash
python csv_to_dashboard.py sensor_log.csv sensor_dashboard.html \
    --time timestamp \
    --width temperature \
    --height humidity \
    --angle wind_direction \
    --strength pressure \
    --category sensor_id \
    --compress
```

### Example 3: Test Data Generation
```python
# Generate test CSV
import pandas as pd
import numpy as np

data = {
    'time': [f"{h:02d}:{m:02d}:00" for h, m in zip(
        np.random.randint(0, 24, 10000), 
        np.random.randint(0, 60, 10000))],
    'metric1': np.random.normal(50, 10, 10000),
    'metric2': np.random.exponential(2, 10000),
    'angle': np.random.uniform(0, 360, 10000),
    'metric3': np.random.gamma(2, 2, 10000),
    'category': np.random.choice(['A', 'B', 'C'], 10000)
}

pd.DataFrame(data).to_csv('test_data.csv', index=False)
```

## Dashboard Features

The generated dashboard includes all features from real_next_best_yet.html:

1. **Interactive Filtering**: 
   - Drag to select ranges on histograms
   - Click bars to filter categories
   - Combine multiple filters

2. **Mini Mode**:
   - Click "Mini" to zoom into filtered subset
   - All charts recalculate for the subset
   - Click "Mega" to return to full data

3. **Statistics Panel**:
   - Real-time statistics update as you filter
   - Shows count and percentages
   - Matches hover tooltips

4. **Export Options**:
   - Export all selected data (no row limits)
   - Maintains filter selections
   - CSV format matches input structure

## Troubleshooting

### "File too large" in browser
- Use `--sample-size` to limit rows
- Try a different browser (Chrome handles large files best)

### Missing data columns
- Check column names match exactly (case-sensitive)
- Use quotes if column names have spaces

### Time parsing errors
- Ensure time format is HH:MM:SS or similar
- Check for invalid time values

### Template file not found
- Make sure real_next_best_yet.html exists in builds/test_ag_2/
- The script uses this as the template for generating dashboards