# Iteration 26 Summary: Clean Linked Brushing

## Current Status

We've created several versions attempting to implement linked brushing:

1. **Basic Dashboard** (`dashboard-uncompressed.html`, `dashboard-compressed.html`)
   - Clean UI with histograms and scatter plot
   - No brushing functionality
   - Works perfectly

2. **With Individual Brushing** (`dashboard-with-brushing-*.html`)
   - Each histogram has its own brush
   - Brushing updates the scatter plot
   - No cross-histogram filtering

3. **Fully Linked Attempt** (`dashboard-fully-linked-final.html`)
   - Attempted to use filterPredicate parameter
   - **Failed**: "Unrecognized signal name: filterPredicate"
   - The approach of using dynamic filter predicates doesn't work in Vega-Lite

4. **Working Simplified** (`dashboard-working-offline.html`)
   - Each histogram has independent selection
   - Updates count display
   - No cross-filtering yet
   - Works without errors

## Key Learnings

### What Doesn't Work:
- Sharing brush parameters across views → duplicate signal errors
- Using dynamic filterPredicate parameters → not recognized by Vega
- Complex signal coordination → too fragile

### What Does Work:
- Independent views with manual coordination
- Simple selections on individual charts
- Updating data sources directly

## The Challenge

The core challenge is that Vega-Lite compiles to Vega, and during this compilation:
1. Signal names can conflict when using similar patterns
2. Dynamic parameters aren't always supported
3. Cross-view filtering requires careful coordination

## Recommended Approach

For true linked brushing like the Observable example, we need to:

1. **Use separate Vega-Lite views** (not layers or repeats)
2. **Manually coordinate via JavaScript**
3. **Update data directly** rather than using filter transforms
4. **Or use a different approach** like D3.js for more control

## Next Steps

1. **Option A**: Continue with Vega-Lite but use data updates
   - When brush changes, filter the data
   - Update all views with filtered data
   - Simpler but requires re-rendering

2. **Option B**: Switch to D3.js
   - Full control over brushing
   - More complex but guaranteed to work
   - Can implement exact Observable behavior

3. **Option C**: Use Mosaic/Arquero
   - Designed for this use case
   - May have better offline support
   - Worth investigating

The current working version provides a foundation, but achieving true linked brushing with Vega-Lite in an offline context is proving challenging due to the library's compilation model.