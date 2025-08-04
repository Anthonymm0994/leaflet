# Implementation Plan - Offline Interactive Dashboard

## 🎯 Overview

Based on the aggregated expert feedback, we have a clear path forward. The recommendations validate our Vega-Lite + Arquero approach while suggesting powerful optimizations using TypedArrays, bitmasks, and pre-computed indices.

## ✅ What We'll Keep

1. **Vega-Lite** for visualizations (native brushing via signals)
2. **Apache Arrow JS** for data loading
3. **Base64 + gzip** compression (pako for decompression)
4. **Single HTML file** approach

## 🔄 What We'll Change

1. **Replace object arrays with TypedArrays** for massive memory savings
2. **Implement bitmask-based filtering** for O(1) performance
3. **Pre-compute bin indices** with flat arrays and offsets
4. **Add progressive enhancement** for scatter plots
5. **Implement UX features** (undo/redo, localStorage, URL state)

## 📋 Implementation Phases

### Phase 1: Data Structure Optimization (Priority: HIGH)

Create a Python preprocessor that generates optimized data structures:

```python
def preprocess_arrow_data(arrow_file):
    # Output structure:
    {
        "data": {
            "age": Float32Array,        # Columnar storage
            "income": Float32Array,
            "rating": Float32Array,
            "session_duration": Float32Array,
            "premium_tier": Uint8Array   # Categorical as codes
        },
        "bins": {
            "age": {
                "edges": [18, 20, 22, ...],  # Bin boundaries
                "counts": Uint16Array,        # Pre-computed counts
                "indices": Uint32Array,       # Flat array of row indices
                "offsets": Uint32Array        # Where each bin starts in indices
            }
        },
        "metadata": {
            "total_rows": 100030,
            "categories": {"premium_tier": ["basic", "standard", "premium"]}
        }
    }
```

**Benefits:**
- 2-4x memory reduction
- Direct array access (no object property lookups)
- Cache-friendly memory layout

### Phase 2: Bitmask Filtering System (Priority: HIGH)

Implement ultra-fast filtering using bit operations:

```javascript
class BitmaskFilter {
    constructor(totalRows) {
        // 1 bit per row, packed into Uint8Array
        this.mask = new Uint8Array(Math.ceil(totalRows / 8));
        this.totalRows = totalRows;
    }
    
    setFromBinSelection(binIndices, indicesArray, offsetsArray) {
        // Clear mask
        this.mask.fill(0);
        
        // Set bits for selected bins
        for (const binId of binIndices) {
            const start = offsetsArray[binId];
            const end = offsetsArray[binId + 1];
            
            for (let i = start; i < end; i++) {
                const rowIdx = indicesArray[i];
                const byteIdx = Math.floor(rowIdx / 8);
                const bitIdx = rowIdx % 8;
                this.mask[byteIdx] |= (1 << bitIdx);
            }
        }
    }
    
    // Combine multiple filters with AND
    static intersect(masks) {
        const result = new Uint8Array(masks[0].length);
        for (let i = 0; i < result.length; i++) {
            result[i] = masks.reduce((acc, mask) => acc & mask[i], 0xFF);
        }
        return result;
    }
}
```

**Benefits:**
- O(1) filtering operations
- Minimal memory overhead (1 bit per row)
- Fast bitwise operations

### Phase 3: Vega-Lite Integration (Priority: HIGH)

Update Vega-Lite specs to work with pre-computed bins:

```javascript
const histogramSpec = {
    data: { 
        values: bins.age.map((count, i) => ({
            bin_id: i,
            count: count,
            x0: edges[i],
            x1: edges[i + 1]
        }))
    },
    layer: [
        // Background bars (total counts)
        {
            mark: { type: 'bar', color: '#30363d' },
            encoding: {
                x: { field: 'x0', type: 'quantitative' },
                x2: { field: 'x1' },
                y: { field: 'count', type: 'quantitative' }
            }
        },
        // Foreground bars (filtered counts)
        {
            params: [{
                name: 'brush',
                select: { type: 'interval', encodings: ['x'] }
            }],
            mark: { type: 'bar', color: '#58a6ff' },
            encoding: {
                x: { field: 'x0', type: 'quantitative' },
                x2: { field: 'x1' },
                y: { field: 'filtered_count', type: 'quantitative' }
            }
        }
    ]
};
```

### Phase 4: Progressive Scatter Plot (Priority: MEDIUM)

Implement LOD (Level of Detail) for the scatter plot:

```javascript
class ProgressiveScatterPlot {
    constructor(data, canvas) {
        this.fullData = data;
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Pre-compute samples
        this.samples = {
            low: this.stratifiedSample(1000),
            medium: this.stratifiedSample(5000),
            high: this.stratifiedSample(10000)
        };
    }
    
    render(selectionMask, quality = 'auto') {
        const selectedCount = this.countSelected(selectionMask);
        
        // Auto-select quality based on selection size
        if (quality === 'auto') {
            if (selectedCount < 5000) quality = 'full';
            else if (selectedCount < 20000) quality = 'high';
            else if (selectedCount < 50000) quality = 'medium';
            else quality = 'low';
        }
        
        // Use Canvas API for fast rendering
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        const data = quality === 'full' ? this.fullData : this.samples[quality];
        // ... render points based on selectionMask
    }
}
```

### Phase 5: UX Enhancements (Priority: MEDIUM)

Add user-friendly features:

```javascript
// 1. Undo/Redo
class FilterHistory {
    constructor() {
        this.history = [];
        this.currentIndex = -1;
    }
    
    push(filterState) {
        this.history = this.history.slice(0, this.currentIndex + 1);
        this.history.push(filterState);
        this.currentIndex++;
    }
    
    undo() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            return this.history[this.currentIndex];
        }
    }
}

// 2. URL State
function saveToURL(filters) {
    const params = new URLSearchParams();
    for (const [field, range] of Object.entries(filters)) {
        params.set(field, `${range[0]}-${range[1]}`);
    }
    window.location.hash = params.toString();
}

// 3. LocalStorage
function saveToLocalStorage(filters) {
    localStorage.setItem('dashboard-filters', JSON.stringify(filters));
}
```

### Phase 6: Build Pipeline (Priority: LOW)

Create an automated build process:

```bash
#!/bin/bash
# build.sh

# 1. Preprocess data
python preprocess_data.py data/test_large_complex.arrow

# 2. Bundle JavaScript
esbuild src/dashboard.js --bundle --minify --format=iife > dist/bundle.js

# 3. Compress data
gzip -c preprocessed_data.json | base64 > dist/data.b64

# 4. Inline everything
python inline_html.py template.html dist/dashboard.html

# 5. Optional: Brotli compression
brotli dist/dashboard.html -o dist/dashboard.html.br
```

## 📊 Expected Performance Metrics

| Metric | Current | Target | Method |
|--------|---------|---------|---------|
| File Size | 38MB | <30MB | Better compression + TypedArrays |
| Load Time | 5-8s | <3s | Optimized parsing |
| Brush Response | 200-300ms | <50ms | Bitmask filtering |
| Memory Usage | 400-500MB | <200MB | TypedArrays |
| Scatter Render | 500ms | <100ms | Progressive LOD |

## 🚫 What We Won't Do

1. **WebGL** - Not supported on file:// in many browsers
2. **Web Workers** - Can't load from file://
3. **WASM** - Too complex for offline embedding
4. **External dependencies** - Everything must be inlined

## 📅 Timeline

1. **Week 1**: Implement TypedArray data structures and bitmask filtering
2. **Week 2**: Integrate with Vega-Lite and test performance
3. **Week 3**: Add progressive rendering and UX features
4. **Week 4**: Optimize build pipeline and final testing

## 🎯 Next Immediate Steps

1. Create `preprocess_data.py` to generate TypedArray-based structure
2. Build a minimal proof-of-concept with bitmask filtering
3. Test Vega-Lite integration with pre-computed bins
4. Benchmark performance with 100k records

This plan incorporates all the expert feedback while staying true to our offline constraints. The key insight is using TypedArrays and bitmasks for massive performance gains without adding complexity.