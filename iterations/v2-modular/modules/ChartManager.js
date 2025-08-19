// ChartManager.js - Chart rendering and interaction management
class ChartManager {
    constructor(dataManager, filterManager) {
        this.dataManager = dataManager;
        this.filterManager = filterManager;
        this.charts = {};
        
        // Listen for filter changes
        this.filterManager.addEventListener('filtersApplied', () => {
            this.updateAllCharts();
        });
    }

    createChart(canvasId, type, config) {
        let chart;
        switch (type) {
            case 'histogram':
                chart = new HistogramChart(canvasId, config, this.dataManager, this.filterManager);
                break;
            case 'time':
                chart = new TimeChart(canvasId, config, this.dataManager, this.filterManager);
                break;
            case 'angle':
                chart = new AngleChart(canvasId, config, this.dataManager, this.filterManager);
                break;
            case 'category':
                chart = new CategoryChart(canvasId, config, this.dataManager, this.filterManager);
                break;
            default:
                console.warn(`Unknown chart type: ${type}`);
                return null;
        }
        
        this.charts[canvasId] = chart;
        return chart;
    }

    updateAllCharts() {
        Object.values(this.charts).forEach(chart => chart.draw());
    }

    destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }

    destroyAllCharts() {
        Object.keys(this.charts).forEach(canvasId => this.destroyChart(canvasId));
    }
}

// Base Chart class
class Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.config = config;
        this.dataManager = dataManager;
        this.filterManager = filterManager;
        this.width = 0;
        this.height = 0;
        
        this.resize();
        this.setupEventListeners();
        window.addEventListener('resize', this.resize.bind(this));
    }

    resize() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = (rect.width - 16) * dpr;
        this.canvas.height = (rect.height - 36) * dpr;
        this.canvas.style.width = (rect.width - 16) + 'px';
        this.canvas.style.height = (rect.height - 36) + 'px';
        this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        this.width = rect.width - 16;
        this.height = rect.height - 36;
        this.draw();
    }

    clear() {
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.width, this.height);
    }

    getMousePos(e) {
        const r = this.canvas.getBoundingClientRect();
        return {
            x: (e.clientX - r.left) * (this.width / r.width),
            y: (e.clientY - r.top) * (this.height / r.height)
        };
    }

    setupEventListeners() {
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.canvas.addEventListener('click', this.onClick.bind(this));
    }

    onMouseDown(e) {}
    onMouseMove(e) {}
    onMouseUp(e) {}
    onClick(e) {}
    draw() {}

    destroy() {
        window.removeEventListener('resize', this.resize);
        this.canvas.replaceWith(this.canvas.cloneNode(true));
    }
}

// Histogram Chart for numerical data
class HistogramChart extends Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        this.margin = { top: 10, right: 10, bottom: 40, left: 50 };
        this.isInteracting = false;
        this.isDragging = false;
        this.dragStart = 0;
        this.selection = null;
        this._raf = false;
    }

    draw() {
        this.clear();
        const binData = this.dataManager.binCache[this.config.field];
        if (!binData) return;

        const width = this.width - this.margin.left - this.margin.right;
        const height = this.height - this.margin.top - this.margin.bottom;
        const barWidth = width / binData.bins.length;

        // Calculate counts
        const counts = new Float32Array(binData.bins.length);
        const filteredCounts = new Float32Array(binData.bins.length);

        for (let i = 0; i < binData.bins.length; i++) {
            const bin = binData.bins[i];
            counts[i] = bin.length;
            
            if (bin.length > 1000) {
                let sampled = 0;
                const step = Math.max(1, Math.floor(bin.length / 1000));
                for (let j = 0; j < bin.length && sampled < 1000; j += step) {
                    if (this.dataManager.filteredIndices[bin[j]]) sampled++;
                }
                filteredCounts[i] = (sampled / Math.min(1000, bin.length)) * bin.length;
            } else {
                filteredCounts[i] = bin.filter(idx => this.dataManager.filteredIndices[idx]).length;
            }
        }

        const maxCount = binData.maxCount || Math.max(...counts);

        this.ctx.save();
        this.ctx.translate(this.margin.left, this.margin.top);

        // Draw bars
        for (let i = 0; i < binData.bins.length; i++) {
            const x = i * barWidth;
            const h = (counts[i] / maxCount) * height;
            const fh = (filteredCounts[i] / maxCount) * height;

            this.ctx.fillStyle = '#2a2a2a';
            this.ctx.fillRect(x, height - h, barWidth - 1, h);
            this.ctx.fillStyle = '#4a9eff';
            this.ctx.fillRect(x, height - fh, barWidth - 1, fh);
        }

        // Selection overlay
        if (this.selection) {
            this.ctx.fillStyle = 'rgba(255,255,255,0.1)';
            this.ctx.strokeStyle = '#feca57';
            this.ctx.lineWidth = 2;
            const x1 = this.selection[0] * barWidth;
            const x2 = (this.selection[1] + 1) * barWidth;
            this.ctx.fillRect(x1, 0, x2 - x1, height);
            this.ctx.strokeRect(x1, 0, x2 - x1, height);
        }

        // Axes
        this.ctx.strokeStyle = '#444';
        this.ctx.beginPath();
        this.ctx.moveTo(0, height);
        this.ctx.lineTo(width, height);
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(0, height);
        this.ctx.stroke();

        this.ctx.restore();
    }

    isInChartArea(p) {
        return p.x >= this.margin.left && p.x <= this.width - this.margin.right &&
               p.y >= this.margin.top && p.y <= this.height - this.margin.bottom;
    }

    onMouseDown(e) {
        const p = this.getMousePos(e);
        if (!this.isInChartArea(p)) return;

        const x = p.x - this.margin.left;
        const width = this.width - this.margin.left - this.margin.right;
        const binData = this.dataManager.binCache[this.config.field];
        const bin = Math.floor(x / (width / binData.bins.length));

        if (bin >= 0 && bin < binData.bins.length) {
            this.isDragging = true;
            this.isInteracting = true;
            this.dragStart = bin;
        }
    }

    onMouseMove(e) {
        if (!this.isDragging) return;

        const p = this.getMousePos(e);
        const x = p.x - this.margin.left;
        const width = this.width - this.margin.left - this.margin.right;

        if (x >= 0 && x <= width) {
            const binData = this.dataManager.binCache[this.config.field];
            const bin = Math.floor(x / (width / binData.bins.length));
            if (bin >= 0 && bin < binData.bins.length) {
                this.selection = [Math.min(this.dragStart, bin), Math.max(this.dragStart, bin)];
                if (!this._raf) {
                    this._raf = true;
                    requestAnimationFrame(() => {
                        this._raf = false;
                        this.draw();
                    });
                }
            }
        }
    }

    onMouseUp() {
        if (this.isDragging && this.selection) {
            const binData = this.dataManager.binCache[this.config.field];
            const min = binData.min + this.selection[0] * binData.binSize;
            const max = binData.min + (this.selection[1] + 1) * binData.binSize;
            
            this.filterManager.setFilter(this.config.field, [min, max]);
        }
        
        this.isDragging = false;
        setTimeout(() => { this.isInteracting = false; }, 100);
    }

    onClick(e) {
        if (!this.isInteracting) {
            const p = this.getMousePos(e);
            if (this.isInChartArea(p)) {
                this.selection = null;
                this.filterManager.clearFilter(this.config.field);
                this.draw();
            }
        }
    }
}

// Time Chart (extends Histogram)
class TimeChart extends HistogramChart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
    }
}

// Angle Chart (radial)
class AngleChart extends Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        this.isInteracting = false;
        this.isDragging = false;
        this.selection = null;
    }

    draw() {
        this.clear();
        const binData = this.dataManager.binCache.angle;
        if (!binData) return;

        const cx = this.width / 2;
        const cy = this.height / 2;
        const radius = Math.min(cx, cy) - 20;
        const inner = radius * 0.3;

        this.ctx.save();

        // Grid lines
        this.ctx.strokeStyle = '#2a2a2a';
        this.ctx.lineWidth = 0.5;
        for (let r = inner; r <= radius; r += (radius - inner) / 4) {
            this.ctx.beginPath();
            this.ctx.arc(cx, cy, r, 0, Math.PI * 2);
            this.ctx.stroke();
        }

        for (let a = 0; a < 360; a += 30) {
            const rad = (a - 90) * Math.PI / 180;
            this.ctx.beginPath();
            this.ctx.moveTo(cx + Math.cos(rad) * inner, cy + Math.sin(rad) * inner);
            this.ctx.lineTo(cx + Math.cos(rad) * radius, cy + Math.sin(rad) * radius);
            this.ctx.stroke();
        }

        // Data
        for (let i = 0; i < binData.bins.length; i++) {
            const bin = binData.bins[i];
            const count = bin.filter(idx => this.dataManager.filteredIndices[idx]).length;
            if (count < 1) continue;

            const start = (i * binData.binSize - 90) * Math.PI / 180;
            const end = ((i + 1) * binData.binSize - 90) * Math.PI / 180;
            const scale = (count / binData.maxCount) * (radius - inner);

            this.ctx.fillStyle = '#4a9eff';
            this.ctx.beginPath();
            this.ctx.arc(cx, cy, inner, start, end);
            this.ctx.arc(cx, cy, inner + scale, end, start, true);
            this.ctx.closePath();
            this.ctx.fill();
        }

        this.ctx.restore();
    }
}

// Category Chart
class CategoryChart extends Chart {
    constructor(canvasId, config, dataManager, filterManager) {
        super(canvasId, config, dataManager, filterManager);
        this.margin = { top: 20, right: 10, bottom: 40, left: 60 };
        this.selected = new Set();
    }

    draw() {
        this.clear();
        const width = this.width - this.margin.left - this.margin.right;
        const height = this.height - this.margin.top - this.margin.bottom;

        const counts = [0, 0, 0, 0];
        const totals = [0, 0, 0, 0];
        const step = Math.max(1, Math.floor(this.dataManager.currentRows / 1000000));

        for (let i = 0; i < this.dataManager.currentRows; i += step) {
            totals[this.dataManager.data.category_4[i]]++;
            if (this.dataManager.filteredIndices[i]) {
                counts[this.dataManager.data.category_4[i]]++;
            }
        }

        for (let i = 0; i < 4; i++) {
            counts[i] *= step;
            totals[i] *= step;
        }

        const maxCount = Math.max(...totals);
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'];

        this.ctx.save();
        this.ctx.translate(this.margin.left, this.margin.top);

        const totalBar = width * 0.8;
        const gapW = width * 0.2;
        const barW = totalBar / 4;
        const gap = gapW / 5;

        for (let i = 0; i < 4; i++) {
            const x = gap + i * (barW + gap);
            const h = (totals[i] / maxCount) * height;
            const fh = (counts[i] / maxCount) * height;

            this.ctx.fillStyle = '#2a2a2a';
            this.ctx.fillRect(x, height - h, barW, h);
            
            const isSelected = this.selected.size === 0 || this.selected.has(i);
            this.ctx.fillStyle = isSelected ? colors[i] : '#444';
            this.ctx.fillRect(x, height - fh, barW, fh);

            if (this.selected.has(i)) {
                this.ctx.strokeStyle = '#feca57';
                this.ctx.lineWidth = 2;
                this.ctx.strokeRect(x - 1, height - h - 1, barW + 2, h + 2);
            }

            this.ctx.fillStyle = '#888';
            this.ctx.font = '12px -apple-system, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(['A', 'B', 'C', 'D'][i], x + barW / 2, height + 20);
        }

        this.ctx.restore();
    }

    onMouseDown(e) {
        const p = this.getMousePos(e);
        const width = this.width - this.margin.left - this.margin.right;
        const height = this.height - this.margin.top - this.margin.bottom;
        const x = p.x - this.margin.left;
        const y = p.y - this.margin.top;

        if (x >= 0 && x <= width && y >= 0 && y <= height) {
            const totalBar = width * 0.8;
            const gapW = width * 0.2;
            const barW = totalBar / 4;
            const gap = gapW / 5;

            for (let i = 0; i < 4; i++) {
                const bx = gap + i * (barW + gap);
                if (x >= bx && x <= bx + barW) {
                    if (this.selected.has(i)) {
                        this.selected.delete(i);
                    } else {
                        this.selected.add(i);
                    }

                    this.filterManager.filters.category.clear();
                    if (this.selected.size > 0 && this.selected.size < 4) {
                        this.selected.forEach(c => this.filterManager.filters.category.add(c));
                        this.filterManager.filters.categoryType = 'cat4';
                    }
                    
                    this.filterManager.applyFilters();
                    return;
                }
            }
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChartManager, Chart, HistogramChart, TimeChart, AngleChart, CategoryChart };
}
// Make available globally
window.ChartManager = ChartManager;
window.Chart = Chart;
window.HistogramChart = HistogramChart;
window.TimeChart = TimeChart;
window.AngleChart = AngleChart;
window.CategoryChart = CategoryChart;
