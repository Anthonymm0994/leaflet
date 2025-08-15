/**
 * DataExplorer - Main orchestrator for the data exploration system
 */
class DataExplorer {
    constructor() {
        this.dataManager = null;
        this.filterManager = null;
        this.chartManager = null;
        this.config = null;
        this.statsVisible = false;
        this.miniMode = false;
        this.originalData = null;
    }

    /**
     * Initialize the data explorer
     * @param {Object} config - Configuration object
     */
    init(config = null) {
        // Use provided config or fall back to global config
        this.config = config || window.DataExplorerConfig || this.getDefaultConfig();
        
        // Initialize managers
        this.dataManager = new DataManager();
        this.filterManager = new FilterManager(this.dataManager);
        this.chartManager = new ChartManager(this.dataManager, this.filterManager);
        
        // Initialize data
        const rowCount = this.dataManager.init(this.config);
        
        // Initialize filters
        this.filterManager.init();
        
        // Initialize charts
        this.chartManager.init(this.config.chartTypes || []);
        
        // Setup UI
        this.setupUI();
        this.updateStats();
        this.updateRanges();
        
        // Hide loading, show main
        document.getElementById('loading').style.display = 'none';
        document.getElementById('main').style.display = 'block';
        
        // Setup event listeners
        this.setupEventListeners();
        
        console.log(`DataExplorer initialized with ${rowCount} rows`);
    }

    /**
     * Get default configuration
     * @returns {Object} Default configuration
     */
    getDefaultConfig() {
        return {
            title: "Generic Data Explorer",
            columns: [],
            data: [],
            chartTypes: [],
            miniMetrics: []
        };
    }

    /**
     * Setup the user interface
     */
    setupUI() {
        // Set title
        document.getElementById('title').textContent = this.config.title || 'Data Explorer';
        
        // Update total count
        document.getElementById('totalCount').textContent = this.formatCount(this.dataManager.getRowCount());
        
        // Create chart grid
        this.createChartGrid();
        
        // Create range display
        this.createRangeDisplay();
        
        // Create mini mode grid
        this.createMiniGrid();
    }

    /**
     * Create the chart grid
     */
    createChartGrid() {
        const grid = document.getElementById('chartGrid');
        grid.innerHTML = '';
        
        const chartConfigs = this.config.chartTypes || [];
        const numCharts = chartConfigs.length;
        
        if (numCharts === 0) {
            grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #888;">No charts configured</div>';
            return;
        }
        
        // Calculate grid layout
        const cols = Math.min(3, numCharts);
        const rows = Math.ceil(numCharts / cols);
        
        grid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        grid.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
        
        chartConfigs.forEach((config, index) => {
            const panel = document.createElement('div');
            panel.className = 'panel';
            panel.id = `chart${index}`;
            
            const title = document.createElement('div');
            title.className = 'panel-title';
            title.textContent = config.title || `Chart ${index + 1}`;
            
            panel.appendChild(title);
            grid.appendChild(panel);
        });
    }

    /**
     * Create the range display
     */
    createRangeDisplay() {
        const rangeDisplay = document.getElementById('rangeDisplay');
        rangeDisplay.innerHTML = '';
        
        this.dataManager.columns.forEach(column => {
            const rangeItem = document.createElement('div');
            rangeItem.className = 'range-item';
            rangeItem.id = `range_${column}`;
            
            const label = document.createElement('span');
            label.className = 'range-label';
            label.textContent = column;
            
            const value = document.createElement('span');
            value.className = 'range-value';
            value.id = `range_value_${column}`;
            value.textContent = '0';
            
            rangeItem.appendChild(label);
            rangeItem.appendChild(value);
            rangeDisplay.appendChild(rangeItem);
        });
    }

    /**
     * Create the mini mode grid
     */
    createMiniGrid() {
        const miniGrid = document.getElementById('miniGrid');
        miniGrid.innerHTML = '';
        
        const metrics = this.config.miniMetrics || [];
        
        if (metrics.length === 0) {
            // Create default metrics
            const defaultMetrics = [
                { id: 'filtered', label: 'Filtered Rows' },
                { id: 'percent', label: 'of Total' },
                { id: 'avg', label: 'Avg Value' }
            ];
            
            defaultMetrics.forEach(metric => {
                this.createMiniPanel(miniGrid, metric.id, metric.label);
            });
        } else {
            metrics.forEach(metric => {
                this.createMiniPanel(miniGrid, metric.id, metric.label);
            });
        }
    }

    /**
     * Create a mini panel
     * @param {HTMLElement} container - Container element
     * @param {string} id - Panel ID
     * @param {string} label - Panel label
     */
    createMiniPanel(container, id, label) {
        const panel = document.createElement('div');
        panel.className = 'mini-panel';
        
        const value = document.createElement('div');
        value.className = 'mini-value';
        value.id = `mini_${id}`;
        value.textContent = '0';
        
        const labelEl = document.createElement('div');
        labelEl.className = 'mini-label';
        labelEl.textContent = label;
        
        panel.appendChild(value);
        panel.appendChild(labelEl);
        container.appendChild(panel);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Listen for filter updates
        window.addEventListener('filtersApplied', (e) => {
            this.updateStats();
            this.updateRanges();
        });
        
        // Optimize resize handling
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.chartManager.resize();
                this.chartManager.updateAllCharts();
            }, 250);
        });
    }

    /**
     * Update statistics display
     */
    updateStats() {
        const totalCount = this.dataManager.getRowCount();
        const filteredCount = this.dataManager.getFilteredCount();
        const percent = totalCount > 0 ? (filteredCount / totalCount * 100).toFixed(1) : 0;
        
        // Update main display
        document.getElementById('filteredCount').textContent = this.formatCount(filteredCount);
        document.getElementById('percentFiltered').textContent = percent + '%';
        
        // Update mini mode
        const miniFiltered = document.getElementById('mini_filtered');
        const miniPercent = document.getElementById('mini_percent');
        
        if (miniFiltered) {
            miniFiltered.textContent = this.formatCount(filteredCount);
        }
        if (miniPercent) {
            miniPercent.textContent = percent + '%';
        }
        
        // Update stats panel if visible
        if (this.statsVisible) {
            this.updateStatsPanel();
        }
    }

    /**
     * Update ranges display
     */
    updateRanges() {
        this.dataManager.columns.forEach(column => {
            const rangeElement = document.getElementById(`range_value_${column}`);
            if (!rangeElement) return;
            
            const columnType = this.dataManager.getColumnType(column);
            const data = this.dataManager.getColumn(column);
            
            if (columnType === 'time') {
                const min = Math.min(...data);
                const max = Math.max(...data);
                const formatTime = (seconds) => {
                    const h = Math.floor(seconds / 3600);
                    const m = Math.floor((seconds % 3600) / 60);
                    return `${h}:${m.toString().padStart(2, '0')}`;
                };
                rangeElement.textContent = `${formatTime(min)} - ${formatTime(max)}`;
            } else if (columnType === 'number' || columnType === 'integer') {
                const min = Math.min(...data);
                const max = Math.max(...data);
                rangeElement.textContent = `${min.toFixed(2)} - ${max.toFixed(2)}`;
            } else {
                // Categorical - show unique values count
                const uniqueValues = new Set(data).size;
                rangeElement.textContent = `${uniqueValues} unique values`;
            }
        });
    }

    /**
     * Update stats panel
     */
    updateStatsPanel() {
        const statsPanel = document.getElementById('statsPanel');
        if (!statsPanel) return;
        
        const totalCount = this.dataManager.getRowCount();
        const filteredCount = this.dataManager.getFilteredCount();
        const percent = totalCount > 0 ? (filteredCount / totalCount * 100).toFixed(1) : 0;
        
        statsPanel.innerHTML = `
            <div>Filtered Count: <strong>${this.formatCount(filteredCount)}</strong></div>
            <div>Percentage: <strong>${percent}%</strong></div>
            <div>─────────────────</div>
        `;
        
        // Add column-specific stats
        this.dataManager.columns.forEach(column => {
            const columnType = this.dataManager.getColumnType(column);
            const data = this.dataManager.getColumn(column);
            
            if (columnType === 'number' || columnType === 'integer') {
                const filteredData = this.dataManager.getFilteredData(column);
                if (filteredData.length > 0) {
                    const sum = filteredData.reduce((a, b) => a + b, 0);
                    const avg = sum / filteredData.length;
                    statsPanel.innerHTML += `<div>Avg ${column}: <strong>${avg.toFixed(2)}</strong></div>`;
                }
            }
        });
    }

    /**
     * Format count for display
     * @param {number} count - Count to format
     * @returns {string} Formatted count
     */
    formatCount(count) {
        if (count >= 1000000) return `${(count/1000000).toFixed(1)}M`;
        if (count >= 1000) return `${(count/1000).toFixed(0)}k`;
        return count.toLocaleString();
    }

    /**
     * Toggle stats panel
     */
    toggleStats() {
        this.statsVisible = !this.statsVisible;
        const statsPanel = document.getElementById('statsPanel');
        statsPanel.style.display = this.statsVisible ? 'block' : 'none';
        
        if (this.statsVisible) {
            this.updateStatsPanel();
        }
    }

    /**
     * Toggle mini mode
     */
    toggleMiniMode() {
        this.miniMode = !this.miniMode;
        const btn = document.getElementById('miniModeBtn');
        
        if (this.miniMode) {
            document.getElementById('normalMode').style.display = 'none';
            document.getElementById('miniMode').style.display = 'block';
            btn.innerHTML = '🔍 Normal';
        } else {
            document.getElementById('miniMode').style.display = 'none';
            document.getElementById('normalMode').style.display = 'grid';
            btn.innerHTML = '📱 Mini';
        }
    }

    /**
     * Reset all filters
     */
    resetAll() {
        this.filterManager.clearAllFilters();
        this.chartManager.updateAllCharts();
    }

    /**
     * Export data as CSV
     */
    exportCSV() {
        const csv = this.dataManager.exportCSV();
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `filtered_data_${this.dataManager.getFilteredCount()}_rows.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Save snapshot
     */
    saveSnapshot() {
        // Implementation for saving dashboard snapshot
        console.log('Snapshot functionality not implemented yet');
    }

    /**
     * Update configuration
     * @param {Object} newConfig - New configuration
     */
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        
        // Reinitialize if data changed
        if (newConfig.data || newConfig.columns) {
            this.init(this.config);
        }
        
        // Update charts if chart types changed
        if (newConfig.chartTypes) {
            this.chartManager.destroy();
            this.createChartGrid();
            this.chartManager.init(newConfig.chartTypes);
        }
    }

    /**
     * Get current configuration
     * @returns {Object} Current configuration
     */
    getConfig() {
        return { ...this.config };
    }

    /**
     * Get data summary
     * @returns {Object} Data summary
     */
    getDataSummary() {
        return {
            totalRows: this.dataManager.getRowCount(),
            filteredRows: this.dataManager.getFilteredCount(),
            columns: this.dataManager.columns,
            activeFilters: this.filterManager.getActiveFilterCount(),
            filterSummary: this.filterManager.getFilterSummary()
        };
    }

    /**
     * Destroy the data explorer
     */
    destroy() {
        if (this.chartManager) {
            this.chartManager.destroy();
        }
        
        // Remove event listeners
        window.removeEventListener('filtersApplied', this.updateStats);
        window.removeEventListener('resize', this.resizeHandler);
        
        this.dataManager = null;
        this.filterManager = null;
        this.chartManager = null;
    }
}

// Create global instance
window.DataExplorer = new DataExplorer();

// Export for use in other modules
window.DataExplorerClass = DataExplorer;
