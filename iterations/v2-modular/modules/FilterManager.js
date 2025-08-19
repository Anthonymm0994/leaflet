// FilterManager.js - Handles filtering logic and operations
class FilterManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.filters = {
            width: null,
            height: null,
            strength: null,
            time: null,
            angle: null,
            category: new Set(),
            categoryType: 'cat4'
        };
        this.eventListeners = [];
    }

    addEventListener(event, callback) {
        if (!this.eventListeners[event]) {
            this.eventListeners[event] = [];
        }
        this.eventListeners[event].push(callback);
    }

    dispatchEvent(event, data) {
        if (this.eventListeners[event]) {
            this.eventListeners[event].forEach(callback => callback(data));
        }
    }

    setFilter(column, filterValue) {
        this.filters[column] = filterValue;
        this.applyFilters();
    }

    getFilter(column) {
        return this.filters[column];
    }

    clearFilter(column) {
        this.filters[column] = null;
        if (column === 'category') {
            this.filters.category.clear();
        }
        this.applyFilters();
    }

    clearAllFilters() {
        for (const key of Object.keys(this.filters)) {
            if (key === 'category') {
                this.filters.category.clear();
            } else if (key !== 'categoryType') {
                this.filters[key] = null;
            }
        }
        this.dataManager.filteredIndices.fill(1);
        this.dispatchEvent('filtersApplied');
    }

    applyFilters() {
        const newIndices = new Uint8Array(this.dataManager.ROWS);
        newIndices.fill(1);

        // Apply range filters
        const rangeFilters = ['width', 'height', 'strength', 'time', 'angle'];
        for (const field of rangeFilters) {
            const filter = this.filters[field];
            if (filter && Array.isArray(filter) && filter.length === 2) {
                const [min, max] = filter;
                const data = field === 'time' ? this.dataManager.data.timeSeconds : this.dataManager.data[field];
                
                for (let i = 0; i < this.dataManager.ROWS; i++) {
                    if (newIndices[i] && (data[i] < min || data[i] > max)) {
                        newIndices[i] = 0;
                    }
                }
            }
        }

        // Apply category filter
        if (this.filters.category.size > 0 && this.filters.category.size < 4) {
            const categoryData = this.dataManager.data.category_4;
            for (let i = 0; i < this.dataManager.ROWS; i++) {
                if (newIndices[i] && !this.filters.category.has(categoryData[i])) {
                    newIndices[i] = 0;
                }
            }
        }

        this.dataManager.updateFilteredIndices(newIndices);
        this.dispatchEvent('filtersApplied');
    }

    createRangeFilter(min, max) {
        return [min, max];
    }

    createCategoricalFilter(categories) {
        return new Set(categories);
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FilterManager;
}
// Make available globally
window.FilterManager = FilterManager;
