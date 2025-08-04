# Project Structure

## Current Repository Layout

```
leaflet/
├── README.md                      # Project overview
├── leaflet_PROJECT_SUMMARY.md     # Comprehensive learnings & analysis
├── OFFLINE_HTML_SUMMARY.md        # Technical implementation details
├── PROJECT_STRUCTURE.md           # This file
├── next_iteration_idea.md         # Original coordinator pattern spec
│
├── data/                          # Source data files
│   ├── test_large_complex.arrow   # Main test dataset (28MB)
│   └── test_large_complex.parquet # Parquet version (6.4MB)
│
├── builds/                        # All HTML build iterations
│   ├── FILE_ORGANIZATION.md       # Build iteration guide
│   ├── TEST_REPORT.md            # Testing results
│   ├── DISCOVERY_LOG.md         # Technical discoveries
│   ├── validation_report.json    # Automated validation results
│   │
│   ├── Iter 0 - original/        # Initial attempts
│   ├── Iter 1 - embedded/        # Base64 embedding
│   ├── Iter 2 - offline/         # Offline bundling attempts
│   ├── Iter 3 - experiments/     # Various experiments
│   ├── Iter 4 - clean attempt/   # Plotly version
│   ├── Iter 5 - observable arquero/  # ✅ WORKING - General explorer
│   ├── Iter 6 - parquet full data/  # Parquet experiment
│   ├── Iter 7 - coordinator pattern/ # Mosaic-inspired
│   ├── Iter 7 - coordinator pattern fixed/
│   ├── Iter 8 - final validated/
│   ├── Iter 9 - duckdb fixed/
│   ├── Iter 10 - es modules/
│   └── Iter 11 - linked plots/   # ✅ BEST - Focused on 5 columns
│
├── scripts/                      # Build and utility scripts
│   └── archive/                  # Old/deprecated scripts
│       └── build_embedded_html.py
│
├── docs/                         # Documentation (gitignored)
│
└── .dependency_cache/            # Cached JS libraries
    ├── arrow-14.min.js
    ├── arquero-5.min.js
    ├── d3-7.min.js
    ├── observable-plot-0.6.min.js
    └── pako-2.min.js
```

## Key Files

### Working HTML Files
- `builds/Iter 11 - linked plots/data-explorer.html` - Best focused report version
- `builds/Iter 5 - observable arquero/data-explorer.html` - Best general explorer

### Documentation
- `leaflet_PROJECT_SUMMARY.md` - Comprehensive project analysis
- `OFFLINE_HTML_SUMMARY.md` - Technical implementation guide
- `builds/FILE_ORGANIZATION.md` - Guide to all iterations

### Data
- `data/test_large_complex.arrow` - Main dataset (100k+ records)

## Notes
- All Python build scripts have been archived
- Failed iterations kept for reference
- Dependency cache prevents re-downloading
- Documentation in /docs is gitignored