# 🌿 Leaflet Arrow Explorer

A professional, fast, and powerful desktop application for exploring and visualizing Apache Arrow data files.

## ✨ Features

- **📊 Professional Dark UI**: Modern, clean interface with dark theme
- **🚀 Fast Arrow Processing**: Native Apache Arrow support for lightning-fast data loading
- **📈 Rich Visualizations**: Interactive charts using Plotly.js (histograms, scatter plots, line charts, bar charts, box plots)
- **📋 Data Exploration**: Schema inspection, data preview, and summary statistics
- **💾 Export Capabilities**: Export data previews to CSV
- **🔄 Real-time Updates**: Refresh data and switch between files seamlessly

## 🛠️ Technology Stack

- **Electron**: Cross-platform desktop application framework
- **TypeScript**: Type-safe development with strict configuration
- **Apache Arrow**: High-performance columnar data format
- **Plotly.js**: Interactive scientific charts and visualizations
- **Modern CSS**: Custom dark theme with CSS variables

## 📁 Project Structure

```
leaflet/
├── src/
│   ├── main/           # Electron main process
│   │   └── main.ts     # Main process logic
│   ├── renderer/       # Electron renderer process
│   │   ├── index.html  # Main HTML interface
│   │   ├── styles.css  # Dark theme styling
│   │   └── renderer.ts # Frontend logic
│   ├── types/          # TypeScript type definitions
│   │   └── index.ts    # Shared types
│   └── utils/          # Utility functions
│       └── arrow.ts    # Arrow data processing
├── data/               # Arrow files directory
├── dist/               # Compiled JavaScript output
├── docs/               # Documentation (preserved)
├── start.bat           # Windows start script
├── build.bat           # Windows build script
├── dev.bat             # Windows development script
└── package.json        # Project configuration
```

## Quick Start

### Windows
```bash
# Start the application
start.bat

# Build executable
build.bat
```

### Manual (Cross-platform)
```bash
# Install dependencies
npm install

# Start in development mode
npm run dev

# Build and start
npm start

# Build executable
npm run dist
```

### Usage
1. Place your `.arrow` files in the `data/` folder
2. Launch the application using the start script
3. Select a file from the sidebar to begin exploring
4. Use the tabs to navigate between Overview, Visualizations, and Data Preview
5. Create custom visualizations by selecting chart types and fields

## 🏗️ Building Executables

### Easy Build (Recommended)

**Windows:**
```bash
# Double-click or run:
build.bat
```

### Manual Build
```bash
# Create distributable packages
npm run dist
```

The executables will be created in the `dist-build/` directory.

## 🔧 Development

### Development Mode
**Windows:**
```bash
dev.bat
```

### Manual Development Commands
```bash
# Build TypeScript to JavaScript
npm run build

# Watch mode for development
npm run watch

# Start with DevTools
npm run dev
```

### Code Quality
- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality and consistency
- **Modular Architecture**: Clean separation of concerns

## 📦 Dependencies

### Core Dependencies
- `apache-arrow`: Arrow data processing
- `arquero`: Data manipulation (available for future use)

### Development Dependencies
- `electron`: Desktop application framework
- `typescript`: Type-safe development
- `electron-builder`: Application packaging

### External Libraries (CDN)
- `plotly.js`: Interactive visualizations
- `chart.js`: Additional charting capabilities

## 🎨 UI/UX Features

- **Dark Theme**: Professional dark mode interface
- **Responsive Design**: Adapts to different window sizes
- **Intuitive Navigation**: Tab-based interface for different views
- **Loading States**: Clear feedback during data operations
- **Error Handling**: User-friendly error messages

## 🔮 Future Enhancements

- **Advanced Filtering**: Conditional data filtering
- **Custom Queries**: SQL-like query interface
- **More Chart Types**: Heatmaps, 3D plots, etc.
- **Data Export**: Full dataset export capabilities
- **Performance Optimization**: Lazy loading for large datasets

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using TypeScript, Electron, and Apache Arrow** 