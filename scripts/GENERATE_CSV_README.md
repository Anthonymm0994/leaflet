# Test CSV Generator for Dashboard

This script generates CSV files with various data patterns suitable for testing the interactive dashboard. It can create realistic datasets with different distributions and patterns.

## Installation

No additional dependencies needed beyond what's required for the dashboard converter:
```bash
pip install pandas numpy
```

## Usage

### Basic Usage
```bash
python generate_test_csv.py
```
This creates a 100,000 row CSV file with mixed data patterns.

### Advanced Usage
```bash
python generate_test_csv.py --rows 1000000 --pattern realistic --output sales_data.csv
```

### Parameters

- `--rows`: Number of rows to generate (default: 100,000)
- `--output`: Output filename (default: test_data.csv)
- `--pattern`: Data distribution pattern
  - `normal`: Normal/Gaussian distributions
  - `skewed`: Skewed distributions (lognormal, exponential, gamma)
  - `bimodal`: Multiple peaks in data
  - `realistic`: Business-like patterns with time correlations
  - `timeseries`: Sequential time series with trends
  - `mixed`: Combination of all patterns (default)
- `--categories`: Number of categories to generate (default: 4)
- `--seed`: Random seed for reproducibility (default: 42)

## Data Patterns

### Normal Pattern
- Uniform time distribution
- Normal distributions for all metrics
- Good for testing basic functionality

### Skewed Pattern
- Business hours concentration
- Right-skewed sales data (lognormal)
- Exponential decay patterns
- Realistic for business metrics

### Bimodal Pattern
- Multiple peaks in distributions
- Cardinal direction concentration for angles
- Time peaks at specific hours
- Good for testing filtering on multi-modal data

### Realistic Pattern
- Business hours with lunch dips
- Sales correlated with time of day
- Department-based angle distribution
- Customer satisfaction with rush hour effects
- Most realistic for business dashboards

### Time Series Pattern
- Sequential time data
- Trending patterns with seasonality
- Multiple frequency components
- Good for testing time-based analysis

### Mixed Pattern
- Combines all patterns in one dataset
- Most comprehensive for testing
- Default option

## Generated Columns

The CSV will contain:
- `timestamp`: Time in HH:MM:SS format
- `width_metric`: Primary numeric metric
- `height_metric`: Secondary numeric metric  
- `angle_degrees`: Angle data (0-360)
- `strength_score`: Score metric (0-100)
- `main_category`: Categorical data
- `status`: Binary category (Active/Inactive)
- `width_height_ratio`: Derived ratio metric
- `composite_score`: Weighted combination of metrics

## Examples

### Generate 1M rows of realistic business data
```bash
python generate_test_csv.py --rows 1000000 --pattern realistic --output business_data.csv
```

### Generate 5M rows with 10 categories
```bash
python generate_test_csv.py --rows 5000000 --categories 10 --output large_test.csv
```

### Generate time series data for testing trends
```bash
python generate_test_csv.py --rows 500000 --pattern timeseries --output timeseries.csv
```

### Use with dashboard converter
After generating a CSV:
```bash
python csv_to_dashboard.py business_data.csv dashboard.html \
    --time timestamp \
    --width width_metric \
    --height height_metric \
    --angle angle_degrees \
    --strength strength_score \
    --category main_category \
    --category2 status
```

## Data Characteristics

### Correlations
- Height is partially correlated with width (r ≈ 0.6)
- Strength shows fatigue effect over time
- Category distribution follows power law for many categories

### Realistic Features
- Business hour patterns
- Lunch break dips
- Rush hour effects
- Department-based clustering
- Time-of-day correlations

### Testing Features
- NaN values handled appropriately
- Negative values clipped where needed
- Extreme values for stress testing
- Various distribution shapes

## Performance

Generation speed (approximate):
- 100K rows: ~1 second
- 1M rows: ~5 seconds
- 5M rows: ~25 seconds
- 10M rows: ~50 seconds

File sizes:
- 100K rows: ~10 MB
- 1M rows: ~100 MB
- 5M rows: ~500 MB