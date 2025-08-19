// DataExplorer.js - Main orchestrator and public API
class DataExplorer {
    constructor() {
        this.dataManager = null;
        this.filterManager = null;
        this.chartManager = null;
        this.isMiniMode = false;
    }

    async init() {
        // Initialize managers
        this.dataManager = new DataManager();
        this.filterManager = new FilterManager(this.dataManager);
        this.chartManager = new ChartManager(this.dataManager, this.filterManager);

        // Set up event listeners
        this.filterManager.addEventListener('filtersApplied', () => {
            this.updateStats();
            this.updateRanges();
        });

        // Generate data
        await this.dataManager.generateData((progress, status) => {
            document.getElementById('progress').style.width = progress + '%';
            document.getElementById('loadingStatus').textContent = status;
            
            if (progress >= 100) {
                setTimeout(() => {
                    this.setupUI();
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('main').style.display = 'block';
                }, 500);
            }
        });
    }

    setupUI() {
        // Create charts
        this.chartManager.createChart('timeCanvas', 'time', { field: 'time' });
        this.chartManager.createChart('strengthCanvas', 'histogram', { field: 'strength' });
        this.chartManager.createChart('widthCanvas', 'histogram', { field: 'width' });
        this.chartManager.createChart('heightCanvas', 'histogram', { field: 'height' });
        this.chartManager.createChart('angleCanvas', 'angle', { field: 'angle' });
        this.chartManager.createChart('categoryCanvas', 'category', { field: 'category_4' });

        // Initial stats update
        this.updateStats();
        this.updateRanges();
        
        // Draw all charts
        this.chartManager.updateAllCharts();
    }

    updateStats() {
        const totalCount = this.dataManager.getRowCount();
        const filteredCount = this.dataManager.getFilteredCount();
        const percent = totalCount > 0 ? ((filteredCount / totalCount) * 100).toFixed(1) : 0;

        document.getElementById('filteredCount').textContent = this.formatCount(filteredCount);
        document.getElementById('percentFiltered').textContent = percent + '%';

        // Update cat2 stats
        let cat2True = 0;
        let cat2Total = 0;
        for (let i = 0; i < this.dataManager.ROWS; i++) {
            if (this.dataManager.filteredIndices[i]) {
                cat2Total++;
                if (this.dataManager.data.category_2[i] === 1) {
                    cat2True++;
                }
            }
        }
        const cat2Percent = cat2Total > 0 ? ((cat2True / cat2Total) * 100).toFixed(1) : 0;
        document.getElementById('cat2True').textContent = cat2Percent + '%';
    }

    updateRanges() {
        const fields = [
            { name: 'time', data: this.dataManager.data.timeSeconds, format: this.formatTime },
            { name: 'strength', data: this.dataManager.data.strength, format: this.formatNumber },
            { name: 'width', data: this.dataManager.data.width, format: this.formatNumber },
            { name: 'height', data: this.dataManager.data.height, format: this.formatNumber },
            { name: 'angle', data: this.dataManager.data.angle, format: this.formatAngle }
        ];

        for (const field of fields) {
            const filteredData = field.data.filter((_, i) => this.dataManager.filteredIndices[i]);
            if (filteredData.length > 0) {
                const min = Math.min(...filteredData);
                const max = Math.max(...filteredData);
                const element = document.getElementById(field.name + 'Range');
                if (element) {
                    element.textContent = `${field.format(min)} - ${field.format(max)}`;
                }
            }
        }
    }

    formatCount(count) {
        if (count >= 1000000) return (count / 1000000).toFixed(1) + 'M';
        if (count >= 1000) return (count / 1000).toFixed(1) + 'K';
        return count.toString();
    }

    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    }

    formatNumber(num) {
        return num.toFixed(2);
    }

    formatAngle(angle) {
        return angle.toFixed(1) + '°';
    }

    toggleStats() {
        const panel = document.getElementById('statsPanel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        
        if (panel.style.display === 'block') {
            this.updateStatsPanel();
        }
    }

    updateStatsPanel() {
        const panel = document.getElementById('statsPanel');
        const totalCount = this.dataManager.getRowCount();
        const filteredCount = this.dataManager.getFilteredCount();
        
        panel.innerHTML = `
            <div>Total Rows:<strong>${this.formatCount(totalCount)}</strong></div>
            <div>Filtered Rows:<strong>${this.formatCount(filteredCount)}</strong></div>
            <div>Filtered Percentage:<strong>${((filteredCount / totalCount) * 100).toFixed(1)}%</strong></div>
        `;
    }

    toggleMiniMode() {
        this.isMiniMode = !this.isMiniMode;
        const mainGrid = document.querySelector('.grid');
        const miniMode = document.querySelector('.mini-mode');
        const rangeDisplay = document.querySelector('.range-display');
        
        if (this.isMiniMode) {
            mainGrid.style.display = 'none';
            miniMode.style.display = 'block';
            rangeDisplay.style.display = 'none';
            document.getElementById('miniModeBtn').textContent = '📊 Full';
        } else {
            mainGrid.style.display = 'grid';
            miniMode.style.display = 'none';
            rangeDisplay.style.display = 'flex';
            document.getElementById('miniModeBtn').textContent = '📱 Mini';
        }
    }

    resetAll() {
        this.filterManager.clearAllFilters();
    }

    exportCSV() {
        const headers = ['width', 'height', 'angle', 'strength', 'timeSeconds', 'category_4', 'category_2'];
        const filteredData = [];
        
        for (let i = 0; i < this.dataManager.ROWS; i++) {
            if (this.dataManager.filteredIndices[i]) {
                const row = headers.map(header => this.dataManager.data[header][i]);
                filteredData.push(row);
            }
        }
        
        const csvContent = [headers.join(','), ...filteredData.map(row => row.join(','))].join('\n');
        this.downloadCSV(csvContent, 'filtered_data.csv');
    }

    downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    saveSnapshot() {
        const snapshot = {
            timestamp: new Date().toISOString(),
            filters: this.filterManager.filters,
            filteredCount: this.dataManager.getFilteredCount(),
            totalCount: this.dataManager.getRowCount()
        };
        
        const dataStr = JSON.stringify(snapshot, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = window.URL.createObjectURL(dataBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'explorer_snapshot.json';
        a.click();
        window.URL.revokeObjectURL(url);
    }

    destroy() {
        if (this.chartManager) {
            this.chartManager.destroyAllCharts();
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataExplorer;
}
// Make available globally
window.DataExplorer = DataExplorer;
