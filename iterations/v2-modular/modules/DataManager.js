// DataManager.js - Handles data generation, storage, and operations
class DataManager {
    constructor() {
        this.ROWS = 10000000;
        this.BATCH_SIZE = 100000;
        this.data = {
            width: null,
            height: null,
            angle: null,
            strength: null,
            timeSeconds: null,
            category_4: null,
            category_2: null
        };
        this.filteredIndices = new Uint8Array(this.ROWS);
        this.currentRows = this.ROWS;
        this.binCache = {};
    }

    normalRandom(mean, stddev) {
        const u1 = Math.random();
        const u2 = Math.random();
        const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        return mean + z0 * stddev;
    }

    async generateData(progressCallback) {
        this.data.width = new Float32Array(this.ROWS);
        this.data.height = new Float32Array(this.ROWS);
        this.data.angle = new Float32Array(this.ROWS);
        this.data.strength = new Float32Array(this.ROWS);
        this.data.timeSeconds = new Float32Array(this.ROWS);
        this.data.category_4 = new Uint8Array(this.ROWS);
        this.data.category_2 = new Uint8Array(this.ROWS);

        let i = 0;
        const batchGenerate = () => {
            const end = Math.min(i + this.BATCH_SIZE, this.ROWS);
            for (; i < end; i++) {
                this.data.width[i] = Math.max(0.1, this.normalRandom(50, 15));
                this.data.height[i] = Math.max(0.1, this.normalRandom(30, 10));
                this.data.angle[i] = Math.random() * 360;
                this.data.strength[i] = Math.max(0, Math.min(100, this.normalRandom(50, 20)));
                this.data.timeSeconds[i] = Math.random() * 86400;
                this.data.category_4[i] = Math.floor(Math.random() * 4);
                this.data.category_2[i] = Math.random() < 0.5 ? 0 : 1;
            }
            
            const progress = (i / this.ROWS) * 100;
            progressCallback(progress, `Generated ${i.toLocaleString()} rows...`);
            
            if (i < this.ROWS) {
                setTimeout(batchGenerate, 1);
            } else {
                this.filteredIndices.fill(1);
                this.prebinData();
                progressCallback(100, 'Complete!');
            }
        };
        
        batchGenerate();
    }

    prebinData() {
        // Pre-bin numerical data for histograms
        const fields = ['width', 'height', 'strength'];
        
        for (const field of fields) {
            const values = this.data[field];
            const min = Math.min(...values);
            const max = Math.max(...values);
            const numBins = 100;
            const binSize = (max - min) / numBins;
            
            const bins = Array(numBins).fill().map(() => []);
            for (let i = 0; i < values.length; i++) {
                const binIndex = Math.min(Math.floor((values[i] - min) / binSize), numBins - 1);
                bins[binIndex].push(i);
            }
            
            this.binCache[field] = {
                bins,
                min,
                max,
                binSize,
                numBins,
                maxCount: Math.max(...bins.map(bin => bin.length))
            };
        }

        // Pre-bin time data (24 hour bins)
        const timeValues = this.data.timeSeconds;
        const timeBins = Array(24).fill().map(() => []);
        for (let i = 0; i < timeValues.length; i++) {
            const hour = Math.floor(timeValues[i] / 3600);
            timeBins[hour].push(i);
        }
        
        this.binCache.time = {
            bins: timeBins,
            min: 0,
            max: 86400,
            binSize: 3600,
            numBins: 24,
            maxCount: Math.max(...timeBins.map(bin => bin.length))
        };

        // Pre-bin angle data (36 bins = 10 degrees each)
        const angleValues = this.data.angle;
        const angleBins = Array(36).fill().map(() => []);
        for (let i = 0; i < angleValues.length; i++) {
            const binIndex = Math.floor(angleValues[i] / 10);
            angleBins[binIndex].push(i);
        }
        
        this.binCache.angle = {
            bins: angleBins,
            min: 0,
            max: 360,
            binSize: 10,
            numBins: 36,
            maxCount: Math.max(...angleBins.map(bin => bin.length))
        };
    }

    getColumn(column) {
        return this.data[column];
    }

    getFilteredData(column) {
        return this.data[column].filter((_, i) => this.filteredIndices[i]);
    }

    getRowCount() {
        return this.currentRows;
    }

    getFilteredCount() {
        return this.filteredIndices.reduce((sum, val) => sum + val, 0);
    }

    updateFilteredIndices(newIndices) {
        this.filteredIndices = newIndices;
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataManager;
}
// Make available globally
window.DataManager = DataManager;
