# Data Explorer v16 - Zoom on Cursor

This iteration adds zooming functionality to all plots with the zoom centered on the mouse cursor position.

## New Features

### 🎯 Zoom on Mouse Cursor
- **Mouse Wheel Zoom**: Scroll up/down to zoom in/out on any chart
- **Cursor-Centered**: Zoom is always centered on the mouse cursor position
- **Zoom Range**: Zoom levels from 1x to 10x
- **Visual Feedback**: Zoom level indicator displayed on charts when zoomed in

### 🔍 Zoom Controls
- **Reset Button**: Each chart has a 🔍 button to reset zoom to 1x
- **Global Reset**: The "🔄 Reset" button now resets both filters and zoom levels
- **Zoom Persistence**: Zoom levels are saved in snapshots

### 📊 Enhanced Chart Interaction
- **Smooth Zooming**: Smooth zoom transitions with proper coordinate transformations
- **Maintained Functionality**: All existing features (filtering, selection, etc.) work with zoom
- **Performance Optimized**: Efficient rendering with zoom transformations

## How to Use

### Zooming
1. **Mouse Wheel**: Hover over any chart and scroll up to zoom in, down to zoom out
2. **Cursor Position**: Zoom is centered exactly where your mouse cursor is positioned
3. **Reset Zoom**: Click the 🔍 button on any chart to reset its zoom level
4. **Global Reset**: Use the "🔄 Reset" button to reset all charts and filters

### Chart Types with Zoom
- **Histogram Charts**: Full zoom support with maintained bin visibility
- **Categorical Charts**: Zoom support for bar charts
- **Time Charts**: Inherits histogram zoom functionality

## Technical Implementation

### Zoom System
- **Canvas Transformations**: Uses HTML5 Canvas transform methods for smooth zooming
- **Coordinate Mapping**: Maintains proper mouse coordinate mapping during zoom
- **Performance**: Efficient rendering with minimal overhead

### Event Handling
- **Mouse Wheel**: Prevents default scrolling behavior for precise zoom control
- **Coordinate Calculation**: Accurate mouse position calculation relative to chart area
- **Zoom Limits**: Bounded zoom levels (1x to 10x) for usability

### State Management
- **Zoom State**: Each chart maintains its own zoom level and center point
- **Snapshot Integration**: Zoom levels are included in saved snapshots
- **Reset Functionality**: Comprehensive reset options for all zoom states

## File Structure

```
v16-zoom-on-cursor/
├── data_explorer.html    # Main data explorer with zoom functionality
└── README.md            # This documentation
```

## Usage Examples

### Basic Zooming
1. Open the data explorer
2. Hover over any chart
3. Scroll up with mouse wheel to zoom in
4. Scroll down to zoom out
5. Click 🔍 to reset zoom

### Advanced Usage
1. Zoom into specific areas of interest
2. Use filters while zoomed in for detailed analysis
3. Save snapshots that preserve zoom levels
4. Reset all zoom levels with the global reset button

## Browser Compatibility

- **Modern Browsers**: Full support for mouse wheel events and canvas transformations
- **Touch Devices**: Touch gestures for zooming (pinch-to-zoom) may work depending on browser
- **Performance**: Optimized for smooth zooming on modern hardware

## Future Enhancements

- **Pan Support**: Drag to pan around zoomed charts
- **Zoom History**: Undo/redo zoom operations
- **Zoom Presets**: Predefined zoom levels for common use cases
- **Touch Support**: Enhanced touch gesture support for mobile devices
