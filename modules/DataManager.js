/**
 * DataManager - Handles data loading, storage, and basic operations
 */
class DataManager {
    constructor() {
        this.data = {};
        this.originalData = null;
        this.currentRows = 0;
        this.columns = [];
        this.columnTypes = {};
        this.binCache = {};
        this.filteredIndices = null;
    }

    /**
     * Initialize data from configuration
     * @param {Object} config - Configuration object with data and columns
     */
    init(config) {
        this.columns = config.columns || [];
        this.columnTypes = config.columnTypes || {};
        this.data = this.parseData(config.data || []);
        this.currentRows = this.data[this.columns[0]]?.length || 0;
        this.filteredIndices = new Uint8Array(this.currentRows);
        this.filteredIndices.fill(1);
        
        this.prebinData();
        return this.currentRows;
    }

    /**
     * Parse data from various formats into typed arrays
     * @param {Array} rawData - Raw data array
     * @returns {Object} Parsed data object
     */
    parseData(rawData) {
        if (!rawData || rawData.length === 0) return {};
        
        const parsed = {};
        const numRows = rawData.length;
        
        this.columns.forEach(column => {
            const values = rawData.map(row => row[column]);
            const type = this.columnTypes[column] || this.inferType(values);
            
            switch (type) {
                case 'number':
                    parsed[column] = new Float32Array(values);
                    break;
                case 'integer':
                    parsed[column] = new Uint8Array(values);
                    break;
                case 'string':
                    parsed[column] = values;
                    break;
                case 'time':
                    parsed[column] = new Float32Array(values.map(v => this.parseTime(v)));
                    break;
                default:
                    parsed[column] = values;
            }
        });
        
        return parsed;
    }

    /**
     * Infer data type from values
     * @param {Array} values - Array of values
     * @returns {string} Inferred type
     */
    inferType(values) {
        if (values.length === 0) return 'string';
        
        const sample = values.slice(0, Math.min(100, values.length));
        const allNumbers = sample.every(v => !isNaN(v) && v !== null && v !== undefined);
        
        if (allNumbers) {
            const allIntegers = sample.every(v => Number.isInteger(parseFloat(v)));
            return allIntegers ? 'integer' : 'number';
        }
        
        // Check if it's time data
        const timePattern = /^\d{1,2}:\d{2}(:\d{2})?(\.\d+)?$/;
        if (sample.every(v => typeof v === 'string' && timePattern.test(v))) {
            return 'time';
        }
        
        return 'string';
    }

    /**
     * Parse time string to seconds
     * @param {string} timeStr - Time string (HH:MM:SS or HH:MM)
     * @returns {number} Time in seconds
     */
    parseTime(timeStr) {
        if (typeof timeStr !== 'string') return 0;
        
        const parts = timeStr.split(':');
        if (parts.length === 2) {
            return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60;
        } else if (parts.length === 3) {
            return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60 + parseFloat(parts[2]);
        }
        return 0;
    }

    /**
     * Pre-bin data for performance
     */
    prebinData() {
        this.binCache = {};
        
        this.columns.forEach(column => {
            const type = this.columnTypes[column] || this.inferType(this.data[column]);
            
            if (type === 'number' || type === 'integer') {
                this.binCache[column] = this.binData(this.data[column], 50);
            } else if (type === 'time') {
                this.binCache[column] = this.binData(this.data[column], 50);
            } else if (type === 'string') {
                this.binCache[column] = this.binCategoricalData(this.data[column]);
            }
        });
    }

    /**
     * Bin numerical data
     * @param {Float32Array|Uint8Array} arr - Data array
     * @param {number} numBins - Number of bins
     * @returns {Object} Binned data
     */
    binData(arr, numBins) {
        if (!arr || arr.length === 0) return { bins: [], binSize: 1, min: 0, max: 1, maxCount: 0 };
        
        let min = Infinity, max = -Infinity;
        for (let i = 0; i < arr.length; i++) {
            if (arr[i] < min) min = arr[i];
            if (arr[i] > max) max = arr[i];
        }
        
        const range = max - min;
        if (range <= 0) {
            const bins = new Array(numBins).fill(null).map(() => []);
            for (let i = 0; i < arr.length; i++) bins[0].push(i);
            return { bins, binSize: 1, min, max, maxCount: arr.length };
        }
        
        const binSize = range / numBins;
        const bins = new Array(numBins).fill(null).map(() => []);
        
        for (let i = 0; i < arr.length; i++) {
            const value = Math.min(arr[i], max - Number.EPSILON);
            const bin = Math.floor((value - min) / binSize);
            if (bin >= 0 && bin < numBins) bins[bin].push(i);
        }
        
        let maxCount = 0;
        for (let i = 0; i < bins.length; i++) {
            if (bins[i].length > maxCount) maxCount = bins[i].length;
        }
        
        return { bins, binSize, min, max, maxCount };
    }

    /**
     * Bin categorical data
     * @param {Array} arr - Categorical data array
     * @returns {Object} Binned categorical data
     */
    binCategoricalData(arr) {
        const categories = new Map();
        
        for (let i = 0; i < arr.length; i++) {
            const cat = arr[i];
            if (!categories.has(cat)) {
                categories.set(cat, []);
            }
            categories.get(cat).push(i);
        }
        
        const bins = Array.from(categories.values());
        const maxCount = Math.max(...bins.map(bin => bin.length));
        
        return { 
            bins, 
            categories: Array.from(categories.keys()), 
            maxCount,
            isCategorical: true 
        };
    }

    /**
     * Get filtered data for a specific column
     * @param {string} column - Column name
     * @returns {Array} Filtered values
     */
    getFilteredData(column) {
        if (!this.data[column] || !this.filteredIndices) return [];
        
        const result = [];
        for (let i = 0; i < this.currentRows; i++) {
            if (this.filteredIndices[i]) {
                result.push(this.data[column][i]);
            }
        }
        return result;
    }

    /**
     * Get filtered indices
     * @returns {Uint8Array} Filtered indices array
     */
    getFilteredIndices() {
        return this.filteredIndices;
    }

    /**
     * Update filtered indices
     * @param {Uint8Array} newIndices - New filtered indices
     */
    updateFilteredIndices(newIndices) {
        this.filteredIndices = newIndices;
    }

    /**
     * Get column data
     * @param {string} column - Column name
     * @returns {Array|Float32Array|Uint8Array} Column data
     */
    getColumn(column) {
        return this.data[column];
    }

    /**
     * Get column type
     * @param {string} column - Column name
     * @returns {string} Column type
     */
    getColumnType(column) {
        return this.columnTypes[column] || this.inferType(this.data[column]);
    }

    /**
     * Get bin cache for a column
     * @param {string} column - Column name
     * @returns {Object} Bin cache
     */
    getBinCache(column) {
        return this.binCache[column];
    }

    /**
     * Get current row count
     * @returns {number} Current row count
     */
    getRowCount() {
        return this.currentRows;
    }

    /**
     * Get filtered row count
     * @returns {number} Filtered row count
     */
    getFilteredCount() {
        if (!this.filteredIndices) return 0;
        return this.filteredIndices.reduce((sum, val) => sum + val, 0);
    }

    /**
     * Reset filters
     */
    resetFilters() {
        this.filteredIndices = new Uint8Array(this.currentRows);
        this.filteredIndices.fill(1);
    }

    /**
     * Export filtered data as CSV
     * @returns {string} CSV string
     */
    exportCSV() {
        const rows = [this.columns.join(',')];
        const filteredCount = this.getFilteredCount();
        
        for (let i = 0; i < this.currentRows; i++) {
            if (this.filteredIndices[i]) {
                const row = this.columns.map(col => {
                    const value = this.data[col][i];
                    if (typeof value === 'number') {
                        return value.toFixed(6);
                    }
                    return String(value);
                });
                rows.push(row.join(','));
            }
        }
        
        return rows.join('\n');
    }
}

// Export for use in other modules
window.DataManager = DataManager;
