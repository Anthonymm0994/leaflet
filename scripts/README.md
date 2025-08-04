# Scripts

## build_dashboard.py

A reusable script to create fully offline dashboards from Apache Arrow files.

### Usage

```bash
python build_dashboard.py <arrow_file> <column1> <column2> ... [--output <output_file>]
```

### Example

```bash
python build_dashboard.py ../data/mydata.arrow age income score rating --output my_dashboard.html
```

### Features

- Processes Apache Arrow files
- Converts numeric columns to TypedArrays
- Handles categorical data by converting to numeric indices
- Embeds all JavaScript libraries for offline use
- Creates interactive dashboard with:
  - Histogram brushing with AND logic
  - Dynamic scatter plot
  - Summary statistics
  - Export functionality

### Requirements

- Python 3.6+
- pyarrow
- numpy
- requests (for downloading libraries)