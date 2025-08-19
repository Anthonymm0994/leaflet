# V6 Extended - Quick Usage Guide

## 🚀 Super Simple Data Loading

### Option 1: Use Your CSV Directly
```bash
python embed_data.py your_data.csv --output my_explorer.html --title "My Data"
```

### Option 2: Test with Sample Data
```bash
python embed_data.py sample_data.csv --output sample_explorer.html
```

## 📋 CSV Format Required

Your CSV needs these **exact column names**:

```csv
width,height,angle,strength,timeSeconds,category_4,score,department,status
45.2,4.8,120.5,78.3,28800,0,85.2,0,1
52.1,6.2,45.0,65.7,43200,1,92.1,1,1
38.9,3.5,270.8,89.1,57600,2,78.5,2,0
```

### Column Specifications:
- **width**: Any numerical value → Histogram
- **height**: Any numerical value → Histogram  
- **angle**: 0-360 degrees → Radial chart
- **strength**: Any numerical value → Histogram
- **timeSeconds**: 0-86400 (seconds in day, 43200=noon) → Histogram
- **category_4**: Integer 0-3 (maps to A,B,C,D) → Bar chart (4 categories)
- **score**: Any numerical value → Histogram
- **department**: Integer 0-7 (maps to dept names) → Bar chart (8 categories)  
- **status**: Integer 0-1 (0=inactive, 1=active) → Bar chart (2 categories)

## 🎯 Department Mapping (0-7):
0. Engineering
1. Sales  
2. Marketing
3. HR
4. Finance
5. Operations
6. Legal
7. Support

## 🎯 Status Mapping (0-1):
0. Inactive
1. Active

## 🎮 Chart Layout:
```
┌─────────────┬─────────────┬─────────────┐
│ WIDTH       │ STRENGTH    │ ANGLE       │
│ (histogram) │ (histogram) │ (radial)    │
├─────────────┼─────────────┼─────────────┤
│ HEIGHT      │ TIMESECONDS │ CATEGORY_4  │
│ (histogram) │ (histogram) │ (4 bars)    │
├─────────────┼─────────────┼─────────────┤
│ SCORE       │ DEPARTMENT  │ STATUS      │
│ (histogram) │ (8 bars)    │ (2 bars)    │
└─────────────┴─────────────┴─────────────┘
```

## ⚡ Performance Notes:
- Works best with 1K-100K rows
- All charts connected (filter one, all update)
- Bar charts: single selection only (click to select, click again to deselect)
- Export filtered data as CSV anytime

## 🔧 If Your Data is Different:
1. Rename your CSV columns to match the required names
2. Or modify the `embed_data.py` script to map your column names
3. Make sure categorical data uses integers (0,1,2,3... not strings)

## ✅ Quick Test:
```bash
# Test with included sample
python embed_data.py sample_data.csv
open my_data_explorer.html
```
