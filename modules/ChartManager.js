/**
 * ChartManager - Manages chart creation, rendering, and interactions
 */
class ChartManager {
    constructor(dataManager, filterManager) {
        this.dataManager = dataManager;
        this.filterManager = filterManager;
        this.charts = {};
        this.chartConfigs = {};
        this.chartTypes = {
            histogram: HistogramChart,
            time: TimeChart,
            angle: AngleChart,
            categorical: CategoricalChart,
            scatter: ScatterChart
        };
    }

    /**
     * Initialize charts based on configuration
     * @param {Array} chartConfigs - Array of chart configurations
     */
    init(chartConfigs) {
        this.chartConfigs = chartConfigs || [];
        this.createCharts();
        this.setupEventListeners();
    }

    /**
     * Create charts based on configuration
     */
    createCharts() {
        this.chartConfigs.forEach((config, index) => {
            const chartId = `chart${index}`;
            const chartType = config.type || 'histogram';
            const ChartClass = this.chartTypes[chartType];
            
            if (ChartClass) {
                this.charts[chartId] = new ChartClass(
                    chartId,
                    config,
                    this.dataManager,
                    this.filterManager
                );
            }
        });
    }

    /**
     * Setup event listeners for chart updates
     */
    setupEventListeners() {
        window.addEventListener('filtersApplied', () => {
            this.updateAllCharts();
        });
    }

    /**
     * Update all charts
     */
    updateAllCharts() {
        requestAnimationFrame(() => {
            Object.values(this.charts).forEach(chart => {
                if (chart && typeof chart.draw === 'function') {
                    chart.draw();
                }
            });
        });
    }

    /**
     * Get chart by ID
     * @param {string} chartId - Chart identifier
     * @returns {Chart} Chart instance
     */
    getChart(chartId) {
        return this.charts[chartId];
    }

    /**
     * Destroy all charts
     */
    destroy() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
        this.charts = {};
    }

    /**
     * Resize all charts
     */
    resize() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }
}

/**
 * Base Chart class
 */
class Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        this.canvasId = canvasId;
        this.config = config;
        this.dataManager = dataManager;
        this.filterManager = filterManager;
        this.canvas = null;
        this.ctx = null;
        this.isDragging = false;
        this.selection = null;
        
        this.init();
    }

    init() {
        this.createCanvas();
        this.bindEvents();
        this.resize();
    }

    createCanvas() {
        const container = document.getElementById(this.canvasId);
        if (!container) return;

        this.canvas = document.createElement('canvas');
        this.canvas.id = `${this.canvasId}_canvas`;
        container.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d', { alpha: false });
    }

    bindEvents() {
        if (!this.canvas) return;

        this._onResize = this.resize.bind(this);
        this._handleMouseDown = e => this.onMouseDown(e);
        this._handleMouseMove = e => this.onMouseMove(e);
        this._handleMouseUp = e => this.onMouseUp(e);
        this._handleMouseLeave = e => this.onMouseLeave(e);
        this._handleClick = e => this.onClick(e);

        window.addEventListener('resize', this._onResize);
        this.canvas.addEventListener('mousedown', this._handleMouseDown);
        this.canvas.addEventListener('mousemove', this._handleMouseMove);
        this.canvas.addEventListener('mouseup', this._handleMouseUp);
        this.canvas.addEventListener('mouseleave', this._handleMouseLeave);
        this.canvas.addEventListener('click', this._handleClick);
    }

    resize() {
        if (!this.canvas) return;

        const rect = this.canvas.parentElement.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        
        this.canvas.width = (rect.width - 16) * dpr;
        this.canvas.height = (rect.height - 36) * dpr;
        this.canvas.style.width = (rect.width - 16) + 'px';
        this.canvas.style.height = (rect.height - 36) + 'px';
        
        this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        this.width = rect.width - 16;
        this.height = rect.height - 36;
    }

    clear() {
        if (!this.ctx) return;
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.width, this.height);
    }

    getMousePos(e) {
        if (!this.canvas) return { x: 0, y: 0 };
        
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: (e.clientX - rect.left) * (this.width / rect.width),
            y: (e.clientY - rect.top) * (this.height / rect.height)
        };
    }

    // Virtual methods to be overridden
    draw() {}
    onMouseDown(e) {}
    onMouseMove(e) {}
    onMouseUp(e) {}
    onMouseLeave(e) {}
    onClick(e) {}

    destroy() {
        try {
            window.removeEventListener('resize', this._onResize);
            if (this.canvas) {
                this.canvas.removeEventListener('mousedown', this._handleMouseDown);
                this.canvas.removeEventListener('mousemove', this._handleMouseMove);
                this.canvas.removeEventListener('mouseup', this._handleMouseUp);
                this.canvas.removeEventListener('mouseleave', this._handleMouseLeave);
                this.canvas.removeEventListener('click', this._handleClick);
            }
        } catch (_) {}
    }
}

/**
 * Histogram Chart
 */
class HistogramChart extends Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        this.column = config.column;
        this.binData = dataManager.getBinCache(this.column);
        this.margin = { top: 10, right: 10, bottom: 40, left: 50 };
    }

    draw() {
        this.clear();
        if (!this.binData) return;

        const width = this.width - this.margin.left - this.margin.right;
        const height = this.height - this.margin.top - this.margin.bottom;
        const bins = this.binData.bins;
        const barWidth = width / bins.length;

        // Calculate filtered counts
        const filteredCounts = this.calculateFilteredCounts(bins);
        const maxCount = this.binData.maxCount;

        this.ctx.save();
        this.ctx.translate(this.margin.left, this.margin.top);

        // Draw bars
        for (let i = 0; i < bins.length; i++) {
            const x = i * barWidth;
            const h = (bins[i].length / maxCount) * height;
            const fh = (filteredCounts[i] / maxCount) * height;

            // Background
            this.ctx.fillStyle = '#2a2a2a';
            this.ctx.fillRect(x, height - h, barWidth - 1, h);

            // Filtered
            this.ctx.fillStyle = '#4a9eff';
            this.ctx.fillRect(x, height - fh, barWidth - 1, fh);
        }

        this.drawAxes(width, height, maxCount);
        this.ctx.restore();
    }

    calculateFilteredCounts(bins) {
        const filteredIndices = this.dataManager.getFilteredIndices();
        const counts = new Float32Array(bins.length);

        for (let i = 0; i < bins.length; i++) {
            const binIndices = bins[i];
            if (binIndices.length > 1000) {
                // Sample for performance
                let sampled = 0;
                const sampleSize = Math.min(1000, binIndices.length);
                const step = Math.max(1, Math.floor(binIndices.length / sampleSize));
                for (let j = 0; j < binIndices.length && sampled < sampleSize; j += step) {
                    if (filteredIndices[binIndices[j]]) sampled++;
                }
                counts[i] = (sampled / sampleSize) * binIndices.length;
            } else {
                counts[i] = binIndices.filter(idx => filteredIndices[idx]).length;
            }
        }

        return counts;
    }

    drawAxes(width, height, maxCount) {
        // Axes
        this.ctx.strokeStyle = '#444';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(0, height);
        this.ctx.lineTo(width, height);
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(0, height);
        this.ctx.stroke();

        // Grid lines
        this.ctx.strokeStyle = '#2a2a2a';
        this.ctx.lineWidth = 0.5;
        for (let i = 1; i < 5; i++) {
            const y = height * i / 5;
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(width, y);
            this.ctx.stroke();
        }

        // Labels
        this.ctx.fillStyle = '#888';
        this.ctx.font = '10px -apple-system, sans-serif';
        this.ctx.textAlign = 'center';

        const bins = this.binData.bins;
        const step = Math.max(1, Math.floor(bins.length / 10));
        for (let i = 0; i < bins.length; i += step) {
            const x = i * (width / bins.length);
            const value = this.binData.min + i * this.binData.binSize;
            this.ctx.fillText(this.formatValue(value), x, height + 15);
        }

        // Y-axis labels
        this.ctx.textAlign = 'right';
        for (let i = 0; i <= 5; i++) {
            const y = height - (height * i / 5);
            const value = maxCount * i / 5;
            this.ctx.fillText(this.formatCount(value), -5, y + 4);
        }
    }

    formatValue(value) {
        if (this.dataManager.getColumnType(this.column) === 'time') {
            const h = Math.floor(value / 3600);
            const m = Math.floor((value % 3600) / 60);
            return `${h}:${m.toString().padStart(2, '0')}`;
        }
        return value.toFixed(2);
    }

    formatCount(value) {
        if (value >= 1000000) return `${(value/1000000).toFixed(1)}M`;
        if (value >= 1000) return `${(value/1000).toFixed(0)}k`;
        return value.toFixed(0);
    }

    onMouseDown(e) {
        const pos = this.getMousePos(e);
        if (!this.isInChartArea(pos)) return;

        const x = pos.x - this.margin.left;
        const width = this.width - this.margin.left - this.margin.right;
        const bin = Math.floor(x / (width / this.binData.bins.length));

        if (bin >= 0 && bin < this.binData.bins.length) {
            this.isDragging = true;
            this.dragStart = bin;
        }
    }

    onMouseMove(e) {
        const pos = this.getMousePos(e);
        const x = pos.x - this.margin.left;
        const width = this.width - this.margin.left - this.margin.right;

        if (this.isDragging && x >= 0 && x <= width) {
            const bin = Math.floor(x / (width / this.binData.bins.length));
            if (bin >= 0 && bin < this.binData.bins.length) {
                this.selection = [Math.min(this.dragStart, bin), Math.max(this.dragStart, bin)];
                this.draw();
            }
        }
    }

    onMouseUp() {
        if (this.isDragging && this.selection) {
            const filter = [
                this.binData.min + this.selection[0] * this.binData.binSize,
                this.binData.min + (this.selection[1] + 1) * this.binData.binSize
            ];
            this.filterManager.setFilter(this.column, filter);
            this.filterManager.applyFilters();
        }
        this.isDragging = false;
    }

    isInChartArea(pos) {
        return pos.x >= this.margin.left && 
               pos.x <= this.width - this.margin.right &&
               pos.y >= this.margin.top && 
               pos.y <= this.height - this.margin.bottom;
    }
}

/**
 * Categorical Chart
 */
class CategoricalChart extends Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        this.column = config.column;
        this.binData = dataManager.getBinCache(this.column);
        this.margin = { top: 20, right: 10, bottom: 40, left: 60 };
        this.selectedCategories = new Set();
    }

    draw() {
        this.clear();
        if (!this.binData || !this.binData.isCategorical) return;

        const width = this.width - this.margin.left - this.margin.right;
        const height = this.height - this.margin.top - this.margin.bottom;
        const categories = this.binData.categories;
        const bins = this.binData.bins;

        const totalBarWidth = width * 0.8;
        const totalGapWidth = width * 0.2;
        const barWidth = totalBarWidth / categories.length;
        const gapWidth = totalGapWidth / (categories.length + 1);

        this.ctx.save();
        this.ctx.translate(this.margin.left, this.margin.top);

        // Calculate filtered counts
        const filteredCounts = this.calculateFilteredCounts(bins);
        const maxCount = Math.max(...filteredCounts);

        // Draw bars
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#48dbfb'];
        
        categories.forEach((cat, i) => {
            const x = gapWidth + i * (barWidth + gapWidth);
            const h = (bins[i].length / maxCount) * height;
            const fh = (filteredCounts[i] / maxCount) * height;

            // Background bar
            this.ctx.fillStyle = '#2a2a2a';
            this.ctx.fillRect(x, height - h, barWidth, h);

            // Check if selected
            const isSelected = this.selectedCategories.size === 0 || 
                             this.selectedCategories.has(i);

            // Filtered portion
            this.ctx.fillStyle = isSelected ? colors[i % colors.length] : '#444';
            this.ctx.fillRect(x, height - fh, barWidth, fh);

            // Selection outline
            if (this.selectedCategories.has(i) && this.selectedCategories.size > 0) {
                this.ctx.strokeStyle = '#feca57';
                this.ctx.lineWidth = 2;
                this.ctx.strokeRect(x - 1, height - h - 1, barWidth + 2, h + 2);
            }

            // Value label
            this.ctx.fillStyle = '#ccc';
            this.ctx.font = '11px -apple-system, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(this.formatCount(filteredCounts[i]), x + barWidth / 2, height - fh - 5);

            // Category label
            this.ctx.fillStyle = '#888';
            this.ctx.font = '12px -apple-system, sans-serif';
            this.ctx.fillText(cat, x + barWidth / 2, height + 20);
        });

        this.drawAxes(width, height, maxCount);
        this.ctx.restore();
    }

    calculateFilteredCounts(bins) {
        const filteredIndices = this.dataManager.getFilteredIndices();
        const counts = new Array(bins.length).fill(0);

        for (let i = 0; i < bins.length; i++) {
            counts[i] = bins[i].filter(idx => filteredIndices[idx]).length;
        }

        return counts;
    }

    drawAxes(width, height, maxCount) {
        // Axes
        this.ctx.strokeStyle = '#444';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(0, height);
        this.ctx.lineTo(width, height);
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(0, height);
        this.ctx.stroke();

        // Y-axis labels
        this.ctx.fillStyle = '#888';
        this.ctx.font = '10px -apple-system, sans-serif';
        this.ctx.textAlign = 'right';
        for (let i = 0; i <= 5; i++) {
            const y = height - (height * i / 5);
            const value = maxCount * i / 5;
            this.ctx.fillText(this.formatCount(value), -5, y + 4);
        }
    }

    formatCount(value) {
        if (value >= 1000000) return `${(value/1000000).toFixed(1)}M`;
        if (value >= 1000) return `${(value/1000).toFixed(0)}k`;
        return value.toFixed(0);
    }

    onClick(e) {
        const pos = this.getMousePos(e);
        if (!this.isInChartArea(pos)) return;

        const x = pos.x - this.margin.left;
        const width = this.width - this.margin.left - this.margin.right;
        const categories = this.binData.categories;
        const totalBarWidth = width * 0.8;
        const totalGapWidth = width * 0.2;
        const barWidth = totalBarWidth / categories.length;
        const gapWidth = totalGapWidth / (categories.length + 1);

        // Check which bar was clicked
        let clickedBar = -1;
        for (let i = 0; i < categories.length; i++) {
            const barX = gapWidth + i * (barWidth + gapWidth);
            if (x >= barX && x <= barX + barWidth) {
                clickedBar = i;
                break;
            }
        }

        if (clickedBar >= 0) {
            if (this.selectedCategories.has(clickedBar)) {
                this.selectedCategories.delete(clickedBar);
            } else {
                this.selectedCategories.add(clickedBar);
            }

            // Update filters
            if (this.selectedCategories.size > 0 && this.selectedCategories.size < categories.length) {
                const selectedCats = Array.from(this.selectedCategories).map(i => categories[i]);
                this.filterManager.setFilter(this.column, this.filterManager.createCategoricalFilter(selectedCats));
            } else {
                this.filterManager.setFilter(this.column, null);
            }
            
            this.filterManager.applyFilters();
        }
    }

    isInChartArea(pos) {
        return pos.x >= this.margin.left && 
               pos.x <= this.width - this.margin.right &&
               pos.y >= this.margin.top && 
               pos.y <= this.height - this.margin.bottom;
    }
}

// Additional chart types can be added here
class TimeChart extends HistogramChart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
    }

    formatValue(value) {
        const h = Math.floor(value / 3600);
        const m = Math.floor((value % 3600) / 60);
        return `${h}:${m.toString().padStart(2, '0')}`;
    }
}

class AngleChart extends Chart {
    // Implementation for angle charts (radial)
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        // Add angle-specific implementation
    }
}

class ScatterChart extends Chart {
    // Implementation for scatter plots
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        // Add scatter plot implementation
    }
}

// Export for use in other modules
window.ChartManager = ChartManager;
