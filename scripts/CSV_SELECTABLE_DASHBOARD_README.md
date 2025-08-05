# CSV to Selectable Category Dashboard Converter

This script converts any CSV file into an interactive HTML dashboard with selectable category distributions. Users can switch between viewing 2-category and 4-category distributions in the category chart.

## Features

- **Selectable Category Views**: Toggle between category_2 (binary) and category_4 (up to 4 categories)
- **Auto Column Detection**: Automatically identifies appropriate columns based on data patterns
- **All Dashboard Features**: Cross-filtering, mini/mega mode, CSV export, snapshots
- **Efficient Data Handling**: Uses typed arrays and base64 encoding for millions of rows
- **Self-Contained Output**: Single HTML file works offline with all data embedded

## Installation

```bash
pip install pandas numpy
# Optional for compression
pip install htmlmin
```

## Usage

### Basic Usage
```bash
python csv_to_selectable_dashboard.py input.csv output.html
```

### With Column Mapping
```bash
python csv_to_selectable_dashboard.py sales_data.csv dashboard.html \
    --time timestamp \
    --width revenue \
    --height units_sold \
    --angle region_code \
    --strength satisfaction \
    --category product_type \
    --category2 is_premium
```

### With Compression
```bash
python csv_to_selectable_dashboard.py data.csv dashboard.html --compress
```

### Testing with Sample
```bash
python csv_to_selectable_dashboard.py large_data.csv test.html --sample 10000
```

## Parameters

- `input_csv`: Path to input CSV file
- `output_html`: Path for output HTML dashboard
- `--time`: Column for time data (HH:MM:SS format)
- `--width`: Column for width metric (primary numeric)
- `--height`: Column for height metric (secondary numeric)
- `--angle`: Column for angle data (0-360 degrees)
- `--strength`: Column for strength metric (0-100 range)
- `--category`: Column for main category (up to 4 unique values)
- `--category2`: Column for binary category
- `--compress`: Compress the output HTML
- `--sample N`: Use only first N rows (for testing)

## Column Auto-Detection

If columns are not specified, the script attempts to detect them:

1. **Time**: Looks for HH:MM:SS formatted strings
2. **Angle**: Numeric column with values 0-360
3. **Strength**: Numeric column with values 0-100
4. **Width/Height**: Other positive numeric columns
5. **Category2**: Categorical column with exactly 2 unique values
6. **Category**: Categorical column with 2-4 unique values

## Dashboard Features

### Category Selection
- Dropdown menu above category chart
- Switch between:
  - **category_4**: Shows up to 4 categories (A, B, C, D)
  - **category_2**: Shows binary categories (False, True)
- Filters and stats update based on selected view

### Interactive Features
- **Cross-filtering**: Click and drag on any chart to filter all others
- **Multi-selection**: Click bars in category chart to select/deselect
- **Mini/Mega Mode**: Isolate filtered data for detailed analysis
- **Stats Panel**: View detailed statistics for filtered data
- **CSV Export**: Download filtered data as CSV
- **Snapshot**: Save current view as PNG image

## Examples

### Business Data Dashboard
```bash
# Generate test data
python generate_test_csv.py --rows 1000000 --pattern realistic --output business.csv

# Create dashboard
python csv_to_selectable_dashboard.py business.csv business_dashboard.html \
    --time timestamp \
    --width width_metric \
    --height height_metric \
    --angle angle_degrees \
    --strength strength_score \
    --category main_category \
    --category2 status
```

### Sensor Data Dashboard
```bash
python csv_to_selectable_dashboard.py sensor_data.csv sensor_dashboard.html \
    --time reading_time \
    --width temperature \
    --height humidity \
    --angle wind_direction \
    --strength signal_strength \
    --category sensor_type \
    --category2 is_active
```

### Quick Test
```bash
# Generate small test file
python generate_test_csv.py --rows 100000 --output test.csv

# Create dashboard with auto-detection
python csv_to_selectable_dashboard.py test.csv test_dashboard.html
```

## Performance

- 100K rows: ~3 MB HTML, loads in <1 second
- 1M rows: ~30 MB HTML, loads in 2-3 seconds
- 5M rows: ~150 MB HTML, loads in 5-10 seconds
- 10M rows: ~300 MB HTML, loads in 10-15 seconds

## Tips

1. **Column Selection**: The script works best when you specify columns explicitly
2. **Data Quality**: Clean data (no missing values) produces better visualizations
3. **Categories**: Limit main category to 4 unique values for best display
4. **Compression**: Use `--compress` for files over 1M rows to reduce size
5. **Testing**: Use `--sample` to test with subset before processing full dataset

## Troubleshooting

### "Template not found" Error
Make sure `selectable_category_dashboard.html` exists in the `builds/` directory.

### Large File Issues
- Use compression: `--compress`
- Sample data first: `--sample 100000`
- Check available memory for very large datasets

### Category Display Issues
- Ensure category column has ≤4 unique values
- Binary category should have exactly 2 unique values
- Non-string categories are converted to strings