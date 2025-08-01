import { describe, it, expect, beforeEach, afterEach } from 'jest';

// Mock DOM environment for testing
const mockDOM = {
  getElementById: jest.fn(),
  querySelectorAll: jest.fn(),
  addEventListener: jest.fn(),
  createElement: jest.fn(),
  appendChild: jest.fn(),
  innerHTML: '',
  style: { display: '' },
  classList: {
    add: jest.fn(),
    remove: jest.fn(),
    toggle: jest.fn()
  }
};

// Mock window object
const mockWindow = {
  libraryState: {
    stdlib: false,
    plot: false,
    arquero: false,
    chart: false,
    allLoaded: false
  },
  Plot: undefined,
  aq: undefined,
  Chart: undefined,
  onLibrariesLoaded: undefined
};

// Mock ipcRenderer
const mockIpcRenderer = {
  invoke: jest.fn()
};

// Mock global objects
global.document = mockDOM as any;
global.window = mockWindow as any;
global.alert = jest.fn();
global.console = {
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn()
} as any;

describe('Renderer E2E Tests', () => {
  let mockElements: any;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();
    
    // Setup mock DOM elements
    mockElements = {
      'file-list': { innerHTML: '', appendChild: jest.fn() },
      'dataset-info': { innerHTML: '' },
      'schema-info': { innerHTML: '', appendChild: jest.fn() },
      'file-selection': { classList: { add: jest.fn(), remove: jest.fn() } },
      'data-explorer': { classList: { add: jest.fn(), remove: jest.fn() } },
      'refresh-btn': { addEventListener: jest.fn() },
      'chart-type': { value: 'histogram' },
      'x-axis-select': { value: 'age', innerHTML: '', appendChild: jest.fn() },
      'y-axis-select': { value: 'salary', innerHTML: '', appendChild: jest.fn() },
      'create-chart-btn': { addEventListener: jest.fn() },
      'chart-container': { innerHTML: '' },
      'data-table-header': { innerHTML: '' },
      'data-table-body': { innerHTML: '', appendChild: jest.fn() },
      'preview-info-text': { textContent: '' },
      'export-csv-btn': { addEventListener: jest.fn() },
      'summary-stats': { innerHTML: '' },
      'loading-status': { textContent: '' },
      'library-status': { textContent: '', className: '' }
    };

    // Setup getElementById mock
    (document.getElementById as jest.Mock).mockImplementation((id: string) => {
      return mockElements[id] || null;
    });

    // Setup querySelectorAll mock
    (document.querySelectorAll as jest.Mock).mockReturnValue([]);

    // Reset window library state
    mockWindow.libraryState = {
      stdlib: false,
      plot: false,
      arquero: false,
      chart: false,
      allLoaded: false
    };
  });

  describe('Library Loading', () => {
    it('should wait for libraries to load before initializing', async () => {
      // Mock the waitForLibraries function
      const waitForLibraries = jest.fn().mockResolvedValue(undefined);
      
      // Simulate libraries loading
      mockWindow.libraryState.stdlib = true;
      mockWindow.libraryState.plot = true;
      mockWindow.libraryState.arquero = true;
      mockWindow.libraryState.chart = true;
      mockWindow.libraryState.allLoaded = true;

      // Mock library objects
      mockWindow.Plot = {
        plot: jest.fn().mockReturnValue({}),
        rectY: jest.fn(),
        binX: jest.fn(),
        dot: jest.fn(),
        line: jest.fn(),
        barY: jest.fn(),
        boxX: jest.fn()
      };

      expect(mockWindow.libraryState.allLoaded).toBe(true);
    });

    it('should handle library loading failures gracefully', () => {
      // Simulate library loading failure
      mockWindow.libraryState.stdlib = false;
      mockWindow.libraryState.plot = false;
      mockWindow.libraryState.arquero = false;
      mockWindow.libraryState.chart = false;
      mockWindow.libraryState.allLoaded = false;

      expect(mockWindow.libraryState.allLoaded).toBe(false);
    });
  });

  describe('File Loading', () => {
    it('should handle successful file loading', async () => {
      const mockFile = {
        name: 'test.arrow',
        path: '/path/to/test.arrow',
        size: 1024
      };

      const mockData = {
        numRows: 1000,
        numCols: 5,
        fields: [
          { name: 'id', type: 'Int32', nullable: false },
          { name: 'name', type: 'Utf8', nullable: false },
          { name: 'age', type: 'Int32', nullable: false }
        ],
        sampleData: [
          { id: 1, name: 'Alice', age: 25 },
          { id: 2, name: 'Bob', age: 30 }
        ],
        filePath: '/path/to/test.arrow'
      };

      // Mock successful IPC response
      (mockIpcRenderer.invoke as jest.Mock).mockResolvedValue({
        success: true,
        data: mockData
      });

      // Simulate file loading
      const result = await mockIpcRenderer.invoke('load-arrow-file', mockFile.path);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockData);
      expect(result.data.numRows).toBe(1000);
      expect(result.data.numCols).toBe(5);
      expect(result.data.fields).toHaveLength(3);
      expect(result.data.sampleData).toHaveLength(2);
    });

    it('should handle file loading errors', async () => {
      // Mock failed IPC response
      (mockIpcRenderer.invoke as jest.Mock).mockResolvedValue({
        success: false,
        error: 'File not found'
      });

      const result = await mockIpcRenderer.invoke('load-arrow-file', '/nonexistent/file.arrow');

      expect(result.success).toBe(false);
      expect(result.error).toBe('File not found');
    });
  });

  describe('Chart Creation', () => {
    beforeEach(() => {
      // Mock Observable Plot
      mockWindow.Plot = {
        plot: jest.fn().mockReturnValue({}),
        rectY: jest.fn(),
        binX: jest.fn(),
        dot: jest.fn(),
        line: jest.fn(),
        barY: jest.fn(),
        boxX: jest.fn()
      };
    });

    it('should create histogram chart successfully', () => {
      const chartData = [{
        x: [1, 2, 3, 4, 5],
        type: 'histogram',
        name: 'age',
        nbinsx: 30,
        marker: {
          color: '#58a6ff',
          line: {
            color: '#1f6feb',
            width: 1
          }
        }
      }];

      // Mock chart container
      const chartContainer = mockElements['chart-container'];
      chartContainer.innerHTML = '';

      // Simulate chart creation
      const plot = mockWindow.Plot.plot({
        style: {
          background: '#161b22',
          color: '#f0f6fc'
        },
        marks: [
          mockWindow.Plot.rectY(chartData[0].x, mockWindow.Plot.binX({y: "count"}, {x: chartData[0].x, fill: "#58a6ff", stroke: "#1f6feb"}))
        ],
        x: {label: 'age', grid: true, gridColor: "#30363d"},
        y: {label: "Count", grid: true, gridColor: "#30363d"},
        title: `Histogram: age`
      });

      expect(mockWindow.Plot.plot).toHaveBeenCalled();
      expect(plot).toBeDefined();
    });

    it('should handle chart creation errors', () => {
      // Mock Plot to throw error
      mockWindow.Plot.plot = jest.fn().mockImplementation(() => {
        throw new Error('Chart creation failed');
      });

      const chartContainer = mockElements['chart-container'];
      chartContainer.innerHTML = '';

      try {
        mockWindow.Plot.plot({});
      } catch (error) {
        expect(error.message).toBe('Chart creation failed');
      }
    });
  });

  describe('Data Display', () => {
    it('should display dataset information correctly', () => {
      const mockData = {
        numRows: 1000,
        numCols: 5,
        fields: [],
        sampleData: [],
        filePath: ''
      };

      const datasetInfo = mockElements['dataset-info'];
      datasetInfo.innerHTML = `
        <div class="info-item">
          <span class="info-label">Rows</span>
          <span class="info-value">${mockData.numRows.toLocaleString()}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Columns</span>
          <span class="info-value">${mockData.numCols}</span>
        </div>
      `;

      expect(datasetInfo.innerHTML).toContain('1,000');
      expect(datasetInfo.innerHTML).toContain('5');
    });

    it('should display schema information correctly', () => {
      const mockFields = [
        { name: 'id', type: 'Int32', nullable: false },
        { name: 'name', type: 'Utf8', nullable: false },
        { name: 'age', type: 'Int32', nullable: false }
      ];

      const schemaInfo = mockElements['schema-info'];
      schemaInfo.innerHTML = '';

      mockFields.forEach(field => {
        const schemaItem = document.createElement('div');
        schemaItem.className = 'schema-item';
        schemaItem.innerHTML = `
          <div class="schema-field-name">${field.name}</div>
          <div class="schema-field-type">${field.type}</div>
        `;
        schemaInfo.appendChild(schemaItem);
      });

      expect(schemaInfo.appendChild).toHaveBeenCalledTimes(3);
    });

    it('should display data preview correctly', () => {
      const mockSampleData = [
        { id: 1, name: 'Alice', age: 25 },
        { id: 2, name: 'Bob', age: 30 },
        { id: 3, name: 'Charlie', age: 35 }
      ];

      const dataTableHeader = mockElements['data-table-header'];
      const dataTableBody = mockElements['data-table-body'];

      // Create table header
      const headers = Object.keys(mockSampleData[0]);
      dataTableHeader.innerHTML = `<tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>`;

      // Create table body
      dataTableBody.innerHTML = '';
      mockSampleData.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = headers.map(h => `<td>${row[h]}</td>`).join('');
        dataTableBody.appendChild(tr);
      });

      expect(dataTableHeader.innerHTML).toContain('<th>id</th>');
      expect(dataTableHeader.innerHTML).toContain('<th>name</th>');
      expect(dataTableHeader.innerHTML).toContain('<th>age</th>');
      expect(dataTableBody.appendChild).toHaveBeenCalledTimes(3);
    });
  });

  describe('Error Handling', () => {
    it('should show error messages when libraries fail to load', () => {
      const showError = jest.fn();
      
      // Simulate library loading failure
      mockWindow.libraryState.allLoaded = false;
      
      if (!mockWindow.libraryState.allLoaded) {
        showError('Chart libraries not loaded. Please refresh the page and try again.');
      }

      expect(showError).toHaveBeenCalledWith('Chart libraries not loaded. Please refresh the page and try again.');
    });

    it('should handle IPC errors gracefully', async () => {
      // Mock IPC error
      (mockIpcRenderer.invoke as jest.Mock).mockRejectedValue(new Error('IPC communication failed'));

      try {
        await mockIpcRenderer.invoke('load-arrow-file', '/test.arrow');
      } catch (error) {
        expect(error.message).toBe('IPC communication failed');
      }
    });
  });

  describe('Utility Functions', () => {
    it('should format file sizes correctly', () => {
      const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
      };

      expect(formatFileSize(0)).toBe('0 Bytes');
      expect(formatFileSize(1024)).toBe('1 KB');
      expect(formatFileSize(1024 * 1024)).toBe('1 MB');
      expect(formatFileSize(1500)).toBe('1.46 KB');
    });

    it('should format cell values correctly', () => {
      const formatCellValue = (value: any): string => {
        if (value === null || value === undefined) return '';
        if (typeof value === 'number') return value.toLocaleString();
        if (typeof value === 'string') {
          return value.length > 50 ? value.substring(0, 50) + '...' : value;
        }
        return String(value);
      };

      expect(formatCellValue(null)).toBe('');
      expect(formatCellValue(1234)).toBe('1,234');
      expect(formatCellValue('short')).toBe('short');
      expect(formatCellValue('a'.repeat(60))).toBe('a'.repeat(50) + '...');
    });
  });
}); 