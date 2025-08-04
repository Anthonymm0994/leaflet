# Tool Assessment for Offline Linked Brushing Visualizations

## Goal
Create an offline HTML report with:
- 4 vertical histograms with brushing
- Linked scatter plot
- Layered histogram effect (selected data overlaid on total)
- 100k+ data points
- Single file, no external dependencies

## 🏆 Best Stack: Vega-Lite API

**Why it's the best:**
- Native brushing and linking support
- Declarative specification makes complex interactions simple
- The Observable example you showed uses this exact approach
- Excellent performance with large datasets
- Can be fully embedded offline

**Implementation approach:**
```javascript
import * as vl from 'https://cdn.jsdelivr.net/npm/vega-lite-api@5/+esm';

const brush = vl.selectInterval().encodings('x').resolve('intersect');

const baseHist = vl.markBar()
  .encode(
    vl.x().fieldQ(vl.repeat('row')).bin({maxbins: 30}),
    vl.y().count()
  );

const histograms = vl.layer(
  baseHist.select(brush).encode(vl.color().value('lightgrey')),
  baseHist.transform(vl.filter(brush))
).repeat({row: ['age', 'income', 'rating', 'session_duration']});
```

**Pros:**
- Exact pattern from your reference
- Minimal code for complex interactions
- Built-in optimization for large datasets
- Perfect layering support

**Cons:**
- Requires bundling vega, vega-lite, and vega-embed
- Large file size (~2MB of libraries)

## 🥈 Second Best: Mosaic + Observable Plot

**Why it's good:**
- Mosaic is specifically designed for coordinated views
- Uses DuckDB-WASM for data processing
- Observable Plot for rendering
- Excellent brushing/linking primitives

**Implementation approach:**
```javascript
import * as mosaic from '@uwdata/mosaic';

const coordinator = new mosaic.Coordinator();
const selection = coordinator.selection();

// Histograms with brushing
const histograms = fields.map(field => 
  Plot.rectY(data, Plot.binX({y: "count"}, {
    x: field,
    fill: selection.has(d) ? "steelblue" : "lightgrey"
  }))
);
```

**Pros:**
- Purpose-built for this use case
- Excellent performance via DuckDB
- Clean API for coordinated views

**Cons:**
- DuckDB-WASM offline embedding is problematic
- Newer library, less documentation
- Complex module dependencies

## 🥉 Third Option: D3.js + Crossfilter

**Why it's viable:**
- Complete control over interactions
- Crossfilter optimized for filtering large datasets
- Proven approach for dashboards

**Implementation approach:**
```javascript
const cf = crossfilter(data);
const ageDim = cf.dimension(d => d.age);
const ageGroup = ageDim.group();

// D3 brush
const brush = d3.brushX()
  .on("brush end", function(event) {
    if (event.selection) {
      const [x0, x1] = event.selection;
      ageDim.filterRange([x.invert(x0), x.invert(x1)]);
      updateAllCharts();
    }
  });
```

**Pros:**
- Maximum flexibility
- Crossfilter handles 100k+ records easily
- No external dependencies beyond D3

**Cons:**
- Much more code required
- Manual coordination of views
- No automatic layering

## 📊 Other Options Considered

### 4. Observable Plot + Custom Coordinator
- Use Plot for rendering
- Build custom brush coordination
- Similar to what we attempted but needs more work

### 5. Plotly.js
- Has brushing support but not as elegant
- Large library size
- Less suitable for linked histograms

### 6. Apache ECharts
- Good performance
- Brushing support exists
- But linking multiple charts is manual

## 🎯 Recommendation

**For your use case, I strongly recommend Vega-Lite API** because:

1. **It matches your reference exactly** - The Observable example uses this pattern
2. **Layered histograms are trivial** - Just use `vl.layer()` with filtered data
3. **Brushing just works** - One line: `vl.selectInterval()`
4. **Offline embedding is proven** - Just include the UMD builds
5. **Performance is excellent** - Handles 100k points well

## 📝 Next Steps

1. Create a proper Vega-Lite implementation with:
   - Vega-Lite API for cleaner code
   - Proper layering for the histogram effect
   - Embedded UMD builds for offline use
   - Your exact 4-histogram layout

2. If Vega-Lite file size is a concern, try Mosaic with:
   - Arquero instead of DuckDB for offline compatibility
   - Observable Plot for rendering
   - Custom coordinator for brushing

Would you like me to implement a proper Vega-Lite version that matches your Observable example exactly?