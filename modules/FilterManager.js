/**
 * FilterManager - Handles data filtering and selection
 */
class FilterManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.filters = {};
        this.activeFilters = new Set();
    }

    /**
     * Initialize filters for all columns
     */
    init() {
        this.filters = {};
        this.activeFilters.clear();
        
        this.dataManager.columns.forEach(column => {
            this.filters[column] = null;
        });
    }

    /**
     * Apply a filter to a specific column
     * @param {string} column - Column name
     * @param {*} filterValue - Filter value (range, set, or null)
     */
    setFilter(column, filterValue) {
        this.filters[column] = filterValue;
        
        if (filterValue !== null) {
            this.activeFilters.add(column);
        } else {
            this.activeFilters.delete(column);
        }
    }

    /**
     * Get current filter for a column
     * @param {string} column - Column name
     * @returns {*} Current filter value
     */
    getFilter(column) {
        return this.filters[column];
    }

    /**
     * Check if a row passes all active filters
     * @param {number} rowIndex - Row index to check
     * @returns {boolean} True if row passes all filters
     */
    checkRow(rowIndex) {
        for (const column of this.activeFilters) {
            const filter = this.filters[column];
            if (!filter) continue;
            
            const value = this.dataManager.getColumn(column)[rowIndex];
            if (!this.passesFilter(value, filter, column)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Check if a value passes a specific filter
     * @param {*} value - Value to check
     * @param {*} filter - Filter to apply
     * @param {string} column - Column name for context
     * @returns {boolean} True if value passes filter
     */
    passesFilter(value, filter, column) {
        const columnType = this.dataManager.getColumnType(column);
        
        if (Array.isArray(filter)) {
            // Range filter [min, max)
            if (filter.length === 2) {
                return value >= filter[0] && value < filter[1];
            }
        } else if (filter instanceof Set) {
            // Categorical filter
            return filter.has(value);
        } else if (typeof filter === 'function') {
            // Custom filter function
            return filter(value);
        }
        
        return true;
    }

    /**
     * Apply all filters and update filtered indices
     */
    applyFilters() {
        const startTime = performance.now();
        const currentRows = this.dataManager.getRowCount();
        const newFilteredIndices = new Uint8Array(currentRows);
        
        // Process in batches for performance
        const BATCH_SIZE = 100000;
        let processed = 0;
        
        const processBatch = () => {
            const batchEnd = Math.min(processed + BATCH_SIZE, currentRows);
            
            for (let i = processed; i < batchEnd; i++) {
                newFilteredIndices[i] = this.checkRow(i) ? 1 : 0;
            }
            
            processed = batchEnd;
            
            if (processed < currentRows) {
                // Use requestIdleCallback for better performance
                if (window.requestIdleCallback) {
                    requestIdleCallback(processBatch, { timeout: 16 });
                } else {
                    setTimeout(processBatch, 0);
                }
            } else {
                // All batches processed
                this.dataManager.updateFilteredIndices(newFilteredIndices);
                
                // Trigger update event
                const event = new CustomEvent('filtersApplied', {
                    detail: { 
                        filteredCount: this.dataManager.getFilteredCount(),
                        totalCount: currentRows
                    }
                });
                window.dispatchEvent(event);
            }
        };
        
        processBatch();
    }

    /**
     * Clear all filters
     */
    clearAllFilters() {
        this.filters = {};
        this.activeFilters.clear();
        
        this.dataManager.columns.forEach(column => {
            this.filters[column] = null;
        });
        
        this.dataManager.resetFilters();
        
        // Trigger update event
        const event = new CustomEvent('filtersApplied', {
            detail: { 
                filteredCount: this.dataManager.getFilteredCount(),
                totalCount: this.dataManager.getRowCount()
            }
        });
        window.dispatchEvent(event);
    }

    /**
     * Get active filter count
     * @returns {number} Number of active filters
     */
    getActiveFilterCount() {
        return this.activeFilters.size;
    }

    /**
     * Get filter summary
     * @returns {Object} Summary of current filters
     */
    getFilterSummary() {
        const summary = {};
        
        this.dataManager.columns.forEach(column => {
            const filter = this.filters[column];
            if (filter) {
                summary[column] = {
                    type: this.getFilterType(filter),
                    value: filter,
                    active: true
                };
            } else {
                summary[column] = {
                    type: 'none',
                    value: null,
                    active: false
                };
            }
        });
        
        return summary;
    }

    /**
     * Get filter type
     * @param {*} filter - Filter value
     * @returns {string} Filter type
     */
    getFilterType(filter) {
        if (Array.isArray(filter)) {
            return 'range';
        } else if (filter instanceof Set) {
            return 'categorical';
        } else if (typeof filter === 'function') {
            return 'custom';
        }
        return 'unknown';
    }

    /**
     * Create a range filter
     * @param {number} min - Minimum value (inclusive)
     * @param {number} max - Maximum value (exclusive)
     * @returns {Array} Range filter
     */
    createRangeFilter(min, max) {
        return [min, max];
    }

    /**
     * Create a categorical filter
     * @param {Array} categories - Array of allowed categories
     * @returns {Set} Categorical filter
     */
    createCategoricalFilter(categories) {
        return new Set(categories);
    }

    /**
     * Create a custom filter function
     * @param {Function} filterFn - Filter function
     * @returns {Function} Custom filter
     */
    createCustomFilter(filterFn) {
        return filterFn;
    }

    /**
     * Export filter configuration
     * @returns {Object} Filter configuration
     */
    exportFilters() {
        const exportData = {};
        
        this.dataManager.columns.forEach(column => {
            const filter = this.filters[column];
            if (filter) {
                if (filter instanceof Set) {
                    exportData[column] = Array.from(filter);
                } else if (Array.isArray(filter)) {
                    exportData[column] = [...filter];
                } else {
                    exportData[column] = filter;
                }
            }
        });
        
        return exportData;
    }

    /**
     * Import filter configuration
     * @param {Object} filterConfig - Filter configuration to import
     */
    importFilters(filterConfig) {
        Object.keys(filterConfig).forEach(column => {
            const filterValue = filterConfig[column];
            
            if (Array.isArray(filterValue)) {
                if (filterValue.length === 2 && typeof filterValue[0] === 'number') {
                    // Range filter
                    this.setFilter(column, this.createRangeFilter(filterValue[0], filterValue[1]));
                } else {
                    // Categorical filter
                    this.setFilter(column, this.createCategoricalFilter(filterValue));
                }
            } else {
                this.setFilter(column, filterValue);
            }
        });
        
        this.applyFilters();
    }
}

// Export for use in other modules
window.FilterManager = FilterManager;
