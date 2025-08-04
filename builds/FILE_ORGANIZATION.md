# File Organization Structure

## Directory Layout

```
builds/
├── original/          # Original template files
│   ├── data-explorer.html
│   ├── data-explorer-compressed.html
│   └── data-explorer-optimized.html
│
├── embedded/          # Versions with Arrow data embedded (need CDN)
│   ├── data-explorer-embedded.html
│   └── data-explorer-embedded-compressed.html
│
├── offline/           # Fully offline versions (no CDN needed)
│   ├── data-explorer-offline-optimized.html (86MB) - Has syntax errors
│   ├── data-explorer-offline-optimized-compressed.html (58MB) - Has syntax errors
│   ├── data-explorer-offline-fixed.html (66MB) - Fixed version
│   └── data-explorer-offline-fixed-compressed.html (38MB) - Fixed compressed
│
└── test/              # Test files for debugging
    └── test-basic.html - Simple test for blob URLs and workers
```

## Version History

### Original Templates
- Basic templates that load dependencies from CDN
- Work online only

### Embedded Versions
- Arrow data embedded as base64
- Still require CDN for DuckDB and other libraries
- Work online only

### Offline Versions

#### First Attempt (has errors)
- `data-explorer-offline-optimized.html` - Syntax errors with template literals
- `data-explorer-offline-optimized-compressed.html` - Same syntax errors

#### Fixed Versions (v2)
- `data-explorer-offline-fixed.html` - Properly escaped, should work offline
- `data-explorer-offline-fixed-compressed.html` - Compressed version, much smaller

## File Sizes

| Version | Size | Status |
|---------|------|--------|
| offline-optimized | 86MB | ❌ Has syntax errors |
| offline-optimized-compressed | 58MB | ❌ Has syntax errors |
| offline-fixed | 66MB | ✅ Should work |
| offline-fixed-compressed | 38MB | ✅ Should work |

## Testing Order

1. First test `test/test-basic.html` to verify browser supports blob URLs
2. Then try `offline/data-explorer-offline-fixed-compressed.html` (smaller)
3. If issues, try `offline/data-explorer-offline-fixed.html` (uncompressed)

## Known Issues Fixed

- Octal escape sequences in template literals
- Proper JSON encoding for worker code
- Module imports replaced with global references
- Better error handling and logging