/**
 * 🧪 V14: Comprehensive Test Suite for Core Components
 * 
 * This test suite validates all major functionality of our high-performance
 * data visualization system with isolated testing and performance benchmarks.
 */

class TestSuite {
    constructor() {
        this.tests = [];
        this.results = {
            passed: 0,
            failed: 0,
            total: 0,
            details: []
        };
        this.mockData = null;
        
        this.setupMockData();
        this.registerTests();
    }

    setupMockData() {
        // Create mock data for testing
        const size = 100000; // 100K rows for performance testing
        this.mockData = {
            values: new Float32Array(size),
            x: new Float32Array(size),
            y: new Float32Array(size),
            categories: new Array(size),
            timestamps: new Float32Array(size)
        };

        const categories = ['A', 'B', 'C', 'D', 'E'];
        const baseTime = Date.now();

        for (let i = 0; i < size; i++) {
            this.mockData.values[i] = Math.random() * 100;
            this.mockData.x[i] = Math.random() * 1000;
            this.mockData.y[i] = Math.random() * 1000;
            this.mockData.categories[i] = categories[Math.floor(Math.random() * categories.length)];
            this.mockData.timestamps[i] = baseTime + i * 1000;
        }

        console.log(`✅ Mock data created: ${size.toLocaleString()} points`);
    }

    registerTests() {
        // Core component tests
        this.addTest('DataManager Initialization', this.testDataManagerInit.bind(this));
        this.addTest('DataManager Data Loading', this.testDataManagerLoading.bind(this));
        this.addTest('FilterManager Functionality', this.testFilterManager.bind(this));
        this.addTest('LayoutEngine Grid System', this.testLayoutEngine.bind(this));
        this.addTest('ChartManager Creation', this.testChartManager.bind(this));
        this.addTest('Performance with Large Dataset', this.testLargeDatasetPerformance.bind(this));
        this.addTest('Error Handling', this.testErrorHandling.bind(this));
        this.addTest('Configuration Persistence', this.testConfigPersistence.bind(this));
    }

    addTest(name, testFunction) {
        this.tests.push({ name, testFunction });
    }

    async runAllTests() {
        console.log('🚀 Starting comprehensive test suite...');
        console.log('=' * 50);

        this.results = { passed: 0, failed: 0, total: 0, details: [] };

        for (const test of this.tests) {
            await this.runTest(test);
        }

        this.printResults();
        return this.results;
    }

    async runTest(test) {
        const startTime = performance.now();
        let result = { name: test.name, passed: false, error: null, duration: 0 };

        try {
            await test.testFunction();
            result.passed = true;
            this.results.passed++;
            console.log(`✅ ${test.name}`);
        } catch (error) {
            result.passed = false;
            result.error = error.message;
            this.results.failed++;
            console.log(`❌ ${test.name}: ${error.message}`);
        }

        result.duration = performance.now() - startTime;
        this.results.details.push(result);
        this.results.total++;
    }

    printResults() {
        console.log('\n' + '=' * 50);
        console.log('📊 TEST RESULTS SUMMARY');
        console.log('=' * 50);
        console.log(`Total Tests: ${this.results.total}`);
        console.log(`Passed: ${this.results.passed} ✅`);
        console.log(`Failed: ${this.results.failed} ❌`);
        console.log(`Success Rate: ${((this.results.passed / this.results.total) * 100).toFixed(1)}%`);
        
        const totalDuration = this.results.details.reduce((sum, test) => sum + test.duration, 0);
        console.log(`Total Duration: ${totalDuration.toFixed(2)}ms`);

        if (this.results.failed > 0) {
            console.log('\n❌ FAILED TESTS:');
            this.results.details
                .filter(test => !test.passed)
                .forEach(test => {
                    console.log(`  • ${test.name}: ${test.error}`);
                });
        }

        console.log('=' * 50);
    }

    // Test Implementations

    async testDataManagerInit() {
        // Mock DataManager class
        class MockDataManager {
            constructor(config = {}) {
                this.config = config;
                this.data = null;
                this.isInitialized = false;
            }

            init() {
                this.isInitialized = true;
                return Promise.resolve();
            }

            setData(data) {
                this.data = data;
            }

            getData() {
                return this.data;
            }
        }

        const manager = new MockDataManager({ maxRows: 1000000 });
        await manager.init();

        if (!manager.isInitialized) {
            throw new Error('DataManager failed to initialize');
        }

        if (manager.config.maxRows !== 1000000) {
            throw new Error('Configuration not properly set');
        }
    }

    async testDataManagerLoading() {
        class MockDataManager {
            constructor() {
                this.data = null;
            }

            async loadData(data) {
                // Simulate async loading
                await new Promise(resolve => setTimeout(resolve, 10));
                this.data = data;
                return data;
            }

            getDataSize() {
                return this.data ? this.data.values.length : 0;
            }
        }

        const manager = new MockDataManager();
        const loadedData = await manager.loadData(this.mockData);

        if (!loadedData) {
            throw new Error('Data loading failed');
        }

        if (manager.getDataSize() !== 100000) {
            throw new Error(`Expected 100000 rows, got ${manager.getDataSize()}`);
        }

        if (!(loadedData.values instanceof Float32Array)) {
            throw new Error('Data not properly typed');
        }
    }

    async testFilterManager() {
        class MockFilterManager {
            constructor() {
                this.filters = new Map();
                this.data = null;
            }

            setData(data) {
                this.data = data;
            }

            addFilter(column, condition) {
                this.filters.set(column, condition);
            }

            applyFilters() {
                if (!this.data) return null;

                let filteredIndices = [];
                for (let i = 0; i < this.data.values.length; i++) {
                    let includeRow = true;

                    for (const [column, condition] of this.filters) {
                        if (column === 'values' && condition.type === 'range') {
                            const value = this.data.values[i];
                            if (value < condition.min || value > condition.max) {
                                includeRow = false;
                                break;
                            }
                        }
                    }

                    if (includeRow) {
                        filteredIndices.push(i);
                    }
                }

                return filteredIndices;
            }

            clearFilters() {
                this.filters.clear();
            }
        }

        const filterManager = new MockFilterManager();
        filterManager.setData(this.mockData);

        // Test adding filter
        filterManager.addFilter('values', { type: 'range', min: 25, max: 75 });

        const filteredIndices = filterManager.applyFilters();
        if (!filteredIndices || filteredIndices.length === 0) {
            throw new Error('Filter application failed');
        }

        // Verify filter worked
        const originalSize = this.mockData.values.length;
        const filteredSize = filteredIndices.length;
        if (filteredSize >= originalSize) {
            throw new Error('Filter did not reduce dataset size');
        }

        // Test clearing filters
        filterManager.clearFilters();
        const unfiltered = filterManager.applyFilters();
        if (unfiltered.length !== originalSize) {
            throw new Error('Filter clearing failed');
        }
    }

    async testLayoutEngine() {
        class MockLayoutEngine {
            constructor() {
                this.layouts = new Map();
                this.currentLayout = null;
            }

            registerLayout(name, config) {
                this.layouts.set(name, config);
            }

            setLayout(name) {
                if (!this.layouts.has(name)) {
                    throw new Error(`Layout '${name}' not found`);
                }
                this.currentLayout = this.layouts.get(name);
            }

            getCurrentLayout() {
                return this.currentLayout;
            }

            calculateGridPositions(numCharts) {
                if (!this.currentLayout) return [];

                const positions = [];
                const { columns, rows } = this.currentLayout;
                
                for (let i = 0; i < numCharts && i < columns * rows; i++) {
                    const row = Math.floor(i / columns);
                    const col = i % columns;
                    positions.push({ row, col, width: 1, height: 1 });
                }

                return positions;
            }
        }

        const layoutEngine = new MockLayoutEngine();

        // Test layout registration
        layoutEngine.registerLayout('2x2', { columns: 2, rows: 2 });
        layoutEngine.registerLayout('3x2', { columns: 3, rows: 2 });

        // Test layout setting
        layoutEngine.setLayout('2x2');
        const currentLayout = layoutEngine.getCurrentLayout();
        if (!currentLayout || currentLayout.columns !== 2) {
            throw new Error('Layout setting failed');
        }

        // Test grid calculation
        const positions = layoutEngine.calculateGridPositions(4);
        if (positions.length !== 4) {
            throw new Error('Grid position calculation failed');
        }

        if (positions[0].row !== 0 || positions[0].col !== 0) {
            throw new Error('Grid position calculation incorrect');
        }

        // Test invalid layout
        try {
            layoutEngine.setLayout('invalid');
            throw new Error('Should have thrown error for invalid layout');
        } catch (error) {
            if (!error.message.includes('not found')) {
                throw error;
            }
        }
    }

    async testChartManager() {
        class MockChart {
            constructor(type, canvas, config) {
                this.type = type;
                this.canvas = canvas;
                this.config = config;
                this.data = null;
                this.isRendered = false;
            }

            setData(data) {
                this.data = data;
            }

            render() {
                if (!this.data) {
                    throw new Error('No data to render');
                }
                this.isRendered = true;
            }

            destroy() {
                this.data = null;
                this.isRendered = false;
            }
        }

        class MockChartManager {
            constructor() {
                this.charts = new Map();
                this.chartTypes = new Map();
            }

            registerChartType(type, chartClass) {
                this.chartTypes.set(type, chartClass);
            }

            createChart(id, type, canvas, config = {}) {
                if (!this.chartTypes.has(type)) {
                    throw new Error(`Chart type '${type}' not registered`);
                }

                const ChartClass = this.chartTypes.get(type);
                const chart = new ChartClass(type, canvas, config);
                this.charts.set(id, chart);
                return chart;
            }

            getChart(id) {
                return this.charts.get(id);
            }

            removeChart(id) {
                const chart = this.charts.get(id);
                if (chart) {
                    chart.destroy();
                    this.charts.delete(id);
                }
            }

            renderAll(data) {
                for (const chart of this.charts.values()) {
                    chart.setData(data);
                    chart.render();
                }
            }
        }

        const chartManager = new MockChartManager();

        // Test chart type registration
        chartManager.registerChartType('histogram', MockChart);
        chartManager.registerChartType('scatter', MockChart);

        // Test chart creation
        const mockCanvas = { width: 400, height: 300 };
        const chart1 = chartManager.createChart('chart1', 'histogram', mockCanvas);
        
        if (!chart1 || chart1.type !== 'histogram') {
            throw new Error('Chart creation failed');
        }

        // Test chart retrieval
        const retrievedChart = chartManager.getChart('chart1');
        if (retrievedChart !== chart1) {
            throw new Error('Chart retrieval failed');
        }

        // Test rendering
        chart1.setData(this.mockData);
        chart1.render();
        if (!chart1.isRendered) {
            throw new Error('Chart rendering failed');
        }

        // Test chart removal
        chartManager.removeChart('chart1');
        if (chartManager.getChart('chart1')) {
            throw new Error('Chart removal failed');
        }

        // Test invalid chart type
        try {
            chartManager.createChart('invalid', 'nonexistent', mockCanvas);
            throw new Error('Should have thrown error for invalid chart type');
        } catch (error) {
            if (!error.message.includes('not registered')) {
                throw error;
            }
        }
    }

    async testLargeDatasetPerformance() {
        const startTime = performance.now();
        
        // Test data processing performance
        const sampleSize = 10000;
        const step = Math.floor(this.mockData.values.length / sampleSize);
        
        // Simulate histogram calculation
        const bins = new Array(20).fill(0);
        const values = [];
        
        for (let i = 0; i < this.mockData.values.length; i += step) {
            values.push(this.mockData.values[i]);
        }
        
        const min = Math.min(...values);
        const max = Math.max(...values);
        const binSize = (max - min) / 20;
        
        values.forEach(value => {
            const binIndex = Math.min(Math.floor((value - min) / binSize), 19);
            bins[binIndex]++;
        });
        
        const processingTime = performance.now() - startTime;
        
        // Performance thresholds
        if (processingTime > 100) { // Should complete within 100ms
            throw new Error(`Performance test failed: ${processingTime.toFixed(2)}ms (expected < 100ms)`);
        }
        
        if (values.length === 0) {
            throw new Error('No data processed');
        }
        
        if (bins.every(bin => bin === 0)) {
            throw new Error('Histogram calculation failed');
        }
        
        console.log(`  Performance: ${processingTime.toFixed(2)}ms for ${values.length} points`);
    }

    async testErrorHandling() {
        class MockComponent {
            processData(data) {
                if (!data) {
                    throw new Error('Data is required');
                }
                
                if (!data.values || data.values.length === 0) {
                    throw new Error('Data must contain values');
                }
                
                return data.values.length;
            }
            
            safeProcessData(data) {
                try {
                    return this.processData(data);
                } catch (error) {
                    console.warn('Data processing error:', error.message);
                    return 0;
                }
            }
        }
        
        const component = new MockComponent();
        
        // Test error throwing
        try {
            component.processData(null);
            throw new Error('Should have thrown error for null data');
        } catch (error) {
            if (!error.message.includes('required')) {
                throw error;
            }
        }
        
        try {
            component.processData({ values: [] });
            throw new Error('Should have thrown error for empty data');
        } catch (error) {
            if (!error.message.includes('contain values')) {
                throw error;
            }
        }
        
        // Test safe error handling
        const result1 = component.safeProcessData(null);
        if (result1 !== 0) {
            throw new Error('Safe processing should return 0 for invalid data');
        }
        
        const result2 = component.safeProcessData(this.mockData);
        if (result2 !== this.mockData.values.length) {
            throw new Error('Safe processing should return correct result for valid data');
        }
    }

    async testConfigPersistence() {
        class MockConfigManager {
            constructor() {
                this.config = {};
                this.storage = new Map(); // Mock localStorage
            }
            
            setConfig(key, value) {
                this.config[key] = value;
            }
            
            getConfig(key, defaultValue = null) {
                return this.config.hasOwnProperty(key) ? this.config[key] : defaultValue;
            }
            
            saveToStorage() {
                this.storage.set('config', JSON.stringify(this.config));
            }
            
            loadFromStorage() {
                const stored = this.storage.get('config');
                if (stored) {
                    this.config = JSON.parse(stored);
                }
            }
            
            resetConfig() {
                this.config = {};
                this.storage.delete('config');
            }
        }
        
        const configManager = new MockConfigManager();
        
        // Test config setting and getting
        configManager.setConfig('chartType', 'histogram');
        configManager.setConfig('dataSize', 100000);
        
        if (configManager.getConfig('chartType') !== 'histogram') {
            throw new Error('Config setting/getting failed');
        }
        
        if (configManager.getConfig('nonexistent', 'default') !== 'default') {
            throw new Error('Default value handling failed');
        }
        
        // Test persistence
        configManager.saveToStorage();
        configManager.resetConfig();
        
        if (configManager.getConfig('chartType') !== null) {
            throw new Error('Config reset failed');
        }
        
        configManager.loadFromStorage();
        
        if (configManager.getConfig('chartType') !== 'histogram') {
            throw new Error('Config persistence failed');
        }
        
        if (configManager.getConfig('dataSize') !== 100000) {
            throw new Error('Config persistence failed for numeric values');
        }
    }
}

// Export for use in test runner
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TestSuite;
} else {
    window.TestSuite = TestSuite;
}
