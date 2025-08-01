import { ArrowFile, ArrowData, ArrowField, ChartType } from '../types';

// Global state
let currentFile: ArrowFile | null = null;
let currentData: ArrowData | null = null;

// DOM elements
const fileList = document.getElementById('file-list') as HTMLDivElement;
const datasetInfo = document.getElementById('dataset-info') as HTMLDivElement;
const schemaInfo = document.getElementById('schema-info') as HTMLDivElement;
const fileSelection = document.getElementById('file-selection') as HTMLDivElement;
const dataExplorer = document.getElementById('data-explorer') as HTMLDivElement;
const refreshBtn = document.getElementById('refresh-btn') as HTMLButtonElement;

// Tab elements
const tabBtns = document.querySelectorAll('.tab-btn') as NodeListOf<HTMLButtonElement>;
const tabContents = document.querySelectorAll('.tab-content') as NodeListOf<HTMLDivElement>;

// Visualization elements
const chartTypeSelect = document.getElementById('chart-type') as HTMLSelectElement;
const xAxisSelect = document.getElementById('x-axis-select') as HTMLSelectElement;
const yAxisSelect = document.getElementById('y-axis-select') as HTMLSelectElement;
const createChartBtn = document.getElementById('create-chart-btn') as HTMLButtonElement;
const chartContainer = document.getElementById('chart-container') as HTMLDivElement;

// Data preview elements
const dataTableHeader = document.getElementById('data-table-header') as HTMLTableSectionElement;
const dataTableBody = document.getElementById('data-table-body') as HTMLTableSectionElement;
const previewInfoText = document.getElementById('preview-info-text') as HTMLSpanElement;
const exportCsvBtn = document.getElementById('export-csv-btn') as HTMLButtonElement;

// Summary stats elements
const summaryStats = document.getElementById('summary-stats') as HTMLDivElement;

// Loading status elements
const loadingStatus = document.getElementById('loading-status') as HTMLDivElement;
const libraryStatus = document.getElementById('library-status') as HTMLDivElement;

// Type declaration for the secure API
declare global {
  interface Window {
    electronAPI: {
      readDataFolder: () => Promise<{ success: boolean; files?: ArrowFile[]; error?: string }>;
      loadArrowFile: (filePath: string) => Promise<{ success: boolean; data?: ArrowData; error?: string }>;
      getColumnData: (filePath: string, columnName: string) => Promise<{ success: boolean; data?: any; error?: string }>;
    };
    libraryState: {
      stdlib: boolean;
      plot: boolean;
      arquero: boolean;
      chart: boolean;
      allLoaded: boolean;
    };
    Plot: any;
  }
}

/**
 * Check if all required libraries are loaded
 */
function checkLibrariesLoaded(): boolean {
  const state = window.libraryState;
  if (!state) {
    console.error('❌ Library state not available');
    return false;
  }
  
  const required = ['stdlib', 'plot', 'arquero', 'chart'];
  const missing = required.filter(lib => !state[lib as keyof typeof state]);
  
  if (missing.length > 0) {
    console.warn('⚠️ Missing libraries:', missing);
    return false;
  }
  
  return true;
}

/**
 * Update library status display
 */
function updateLibraryStatusDisplay(): void {
  const state = window.libraryState;
  if (!state) return;
  
  const loaded = ['stdlib', 'plot', 'arquero', 'chart'].filter(lib => state[lib as keyof typeof state]);
  const total = 4;
  
  if (libraryStatus) {
    libraryStatus.textContent = `Libraries: ${loaded.length}/${total} loaded`;
    libraryStatus.className = `library-status ${loaded.length === total ? 'success' : ''}`;
  }
}

/**
 * Initialize the application
 */
async function init(): Promise<void> {
  console.log('🌿 Leaflet Arrow Explorer starting...');
  
  // Update loading status
  updateLoadingStatus('Checking DOM elements...');
  
  // Debug: Check if DOM elements exist
  console.log('🔍 Checking DOM elements...');
  console.log('fileList:', !!fileList);
  console.log('datasetInfo:', !!datasetInfo);
  console.log('schemaInfo:', !!schemaInfo);
  console.log('fileSelection:', !!fileSelection);
  console.log('dataExplorer:', !!dataExplorer);
  console.log('refreshBtn:', !!refreshBtn);
  
  updateLoadingStatus('Waiting for libraries to load...');
  
  // Wait for libraries to load
  await waitForLibraries();
  
  updateLoadingStatus('Setting up event listeners...');
  
  // Setup event listeners
  setupEventListeners();
  
  // Show initial state
  showInitialState();
  
  // Show the file selection screen immediately
  console.log('📁 Showing file selection screen...');
  
  updateLoadingStatus('Ready!');
  
  // Don't load data files automatically - let user select when ready
  console.log('✅ Application initialized - ready for user interaction');
}

/**
 * Wait for all libraries to load
 */
async function waitForLibraries(): Promise<void> {
  return new Promise((resolve) => {
    const checkLibraries = () => {
      if (checkLibrariesLoaded()) {
        console.log('✅ All libraries loaded successfully');
        resolve();
      } else {
        updateLibraryStatusDisplay();
        setTimeout(checkLibraries, 100);
      }
    };
    
    // Start checking immediately
    checkLibraries();
  });
}

/**
 * Show initial state of the application
 */
function showInitialState(): void {
  if (fileList) {
    fileList.innerHTML = `
      <div class="info-placeholder">
        <div style="text-align: center; padding: 20px;">
          <div style="font-size: 24px; margin-bottom: 10px;">📁</div>
          <div style="font-weight: bold; margin-bottom: 5px;">No files loaded</div>
          <div style="font-size: 12px; color: #8b949e;">Click "Refresh Data" to scan for Arrow files</div>
        </div>
      </div>
    `;
  }
}

/**
 * Update loading status message
 */
function updateLoadingStatus(message: string): void {
  if (loadingStatus) {
    loadingStatus.textContent = message;
  }
  console.log('📊 Loading:', message);
}

/**
 * Load data files from the data folder
 */
async function loadDataFiles(): Promise<void> {
  try {
    // Show loading state
    if (fileList) {
      fileList.innerHTML = `
        <div class="info-placeholder">
          <div style="text-align: center; padding: 20px;">
            <div style="font-size: 24px; margin-bottom: 10px;">⏳</div>
            <div style="font-weight: bold; margin-bottom: 5px;">Loading files...</div>
            <div style="font-size: 12px; color: #8b949e;">Scanning data folder</div>
          </div>
        </div>
      `;
    }
    
    const result = await window.electronAPI.readDataFolder();
    
    if (result.success && result.files) {
      displayFileList(result.files);
    } else {
      showError('Failed to load data files: ' + (result.error || 'Unknown error'));
    }
  } catch (error) {
    showError('Error loading data files: ' + (error instanceof Error ? error.message : 'Unknown error'));
  }
}

/**
 * Display file list in sidebar
 */
function displayFileList(files: ArrowFile[]): void {
  fileList.innerHTML = '';
  
  if (files.length === 0) {
    fileList.innerHTML = '<div class="info-placeholder">No Arrow files found in data folder</div>';
    return;
  }
  
  files.forEach(file => {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.innerHTML = `
      <div class="file-name">${file.name}</div>
      <div class="file-size">${formatFileSize(file.size)}</div>
    `;
    
    fileItem.addEventListener('click', () => loadFile(file));
    fileList.appendChild(fileItem);
  });
}

/**
 * Load a specific Arrow file
 */
async function loadFile(file: ArrowFile): Promise<void> {
  try {
    console.log(`📦 Loading file: ${file.name}`);
    
    // Update UI to show loading state
    updateFileSelection(file);
    
    const result = await window.electronAPI.loadArrowFile(file.path);
    
    if (result.success && result.data) {
      currentFile = file;
      currentData = result.data;
      
      displayDatasetInfo(result.data);
      displaySchemaInfo(result.data.fields);
      displayDataPreview(result.data.sampleData);
      displaySummaryStats(result.data);
      setupVisualizationControls(result.data.fields);
      
      // Show data explorer
      fileSelection.classList.add('hidden');
      dataExplorer.classList.remove('hidden');
      
      console.log(`✅ File loaded: ${result.data.numRows.toLocaleString()} rows, ${result.data.numCols} columns`);
    } else {
      showError('Failed to load file: ' + (result.error || 'Unknown error'));
    }
  } catch (error) {
    showError('Error loading file: ' + (error instanceof Error ? error.message : 'Unknown error'));
  }
}

/**
 * Update file selection UI
 */
function updateFileSelection(file: ArrowFile): void {
  // Remove active class from all file items
  document.querySelectorAll('.file-item').forEach(item => {
    item.classList.remove('active');
  });
  
  // Add active class to selected file
  const fileItems = Array.from(document.querySelectorAll('.file-item'));
  for (const item of fileItems) {
    const nameElement = item.querySelector('.file-name');
    if (nameElement && nameElement.textContent === file.name) {
      item.classList.add('active');
      break;
    }
  }
}

/**
 * Display dataset information
 */
function displayDatasetInfo(data: ArrowData): void {
  if (!currentFile) return;
  
  datasetInfo.innerHTML = `
    <div class="info-item">
      <span class="info-label">Rows</span>
      <span class="info-value">${data.numRows.toLocaleString()}</span>
    </div>
    <div class="info-item">
      <span class="info-label">Columns</span>
      <span class="info-value">${data.numCols}</span>
    </div>
    <div class="info-item">
      <span class="info-label">File Size</span>
      <span class="info-value">${formatFileSize(currentFile.size)}</span>
    </div>
  `;
}

/**
 * Display schema information
 */
function displaySchemaInfo(fields: ArrowField[]): void {
  schemaInfo.innerHTML = '';
  
  fields.forEach(field => {
    const schemaItem = document.createElement('div');
    schemaItem.className = 'schema-item';
    schemaItem.innerHTML = `
      <div class="schema-field-name">${field.name}</div>
      <div class="schema-field-type">${field.type}</div>
    `;
    schemaInfo.appendChild(schemaItem);
  });
}

/**
 * Display summary statistics
 */
function displaySummaryStats(data: ArrowData): void {
  if (!summaryStats) return;
  
  const numericFields = data.fields.filter(field => 
    field.type.includes('Int') || field.type.includes('Float') || field.type.includes('Double')
  );
  
  const stringFields = data.fields.filter(field => 
    field.type.includes('Utf8') || field.type.includes('String')
  );
  
  summaryStats.innerHTML = `
    <div class="stat-item">
      <div class="stat-value">${data.numRows.toLocaleString()}</div>
      <div class="stat-label">Total Rows</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${data.numCols}</div>
      <div class="stat-label">Total Columns</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${numericFields.length}</div>
      <div class="stat-label">Numeric Fields</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">${stringFields.length}</div>
      <div class="stat-label">Text Fields</div>
    </div>
  `;
}

/**
 * Display data preview
 */
function displayDataPreview(sampleData: Record<string, any>[]): void {
  if (!sampleData || sampleData.length === 0) {
    dataTableHeader.innerHTML = '<tr><th>No data available</th></tr>';
    dataTableBody.innerHTML = '';
    return;
  }
  
  // Create table header
  const firstRow = sampleData[0];
  if (!firstRow) {
    dataTableHeader.innerHTML = '<tr><th>No data available</th></tr>';
    dataTableBody.innerHTML = '';
    return;
  }
  
  const headers = Object.keys(firstRow);
  dataTableHeader.innerHTML = `<tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
  
  // Create table body
  dataTableBody.innerHTML = '';
  sampleData.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = headers.map(h => `<td>${formatCellValue(row[h])}</td>`).join('');
    dataTableBody.appendChild(tr);
  });
  
  // Update preview info
  if (currentData) {
    previewInfoText.textContent = `Showing first ${sampleData.length} rows of ${currentData.numRows.toLocaleString()} total rows`;
  }
}

/**
 * Setup visualization controls
 */
function setupVisualizationControls(fields: ArrowField[]): void {
  // Clear existing options
  xAxisSelect.innerHTML = '';
  yAxisSelect.innerHTML = '';
  
  // Add field options
  fields.forEach(field => {
    const option = document.createElement('option');
    option.value = field.name;
    option.textContent = field.name;
    xAxisSelect.appendChild(option.cloneNode(true));
    yAxisSelect.appendChild(option);
  });
}

/**
 * Setup event listeners
 */
function setupEventListeners(): void {
  // Tab switching
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.dataset['tab'];
      if (tabName) {
        switchTab(tabName);
      }
    });
  });
  
  // Refresh button - load files on demand
  refreshBtn.addEventListener('click', async () => {
    console.log('🔄 Loading data files...');
    try {
      await loadDataFiles();
    } catch (error) {
      console.warn('⚠️ Could not load data files:', error);
      if (fileList) {
        fileList.innerHTML = '<div class="info-placeholder">No Arrow files found in data folder</div>';
      }
    }
  });
  
  // Create chart button
  createChartBtn.addEventListener('click', createChart);
  
  // Export CSV button
  exportCsvBtn.addEventListener('click', exportToCsv);
}

/**
 * Switch tabs
 */
function switchTab(tabName: string): void {
  // Update tab buttons
  tabBtns.forEach(btn => {
    btn.classList.toggle('active', btn.dataset['tab'] === tabName);
  });
  
  // Update tab content
  tabContents.forEach(content => {
    content.classList.toggle('active', content.id === `${tabName}-tab`);
  });
}

/**
 * Create chart
 */
async function createChart(): Promise<void> {
  if (!currentData || !currentFile) return;
  
  // Check if libraries are available
  if (!checkLibrariesLoaded()) {
    showError('Chart libraries not loaded. Please refresh the page and try again.');
    return;
  }
  
  const chartType = chartTypeSelect.value as ChartType;
  const xField = xAxisSelect.value;
  const yField = yAxisSelect.value;
  
  if (!xField) {
    showError('Please select an X-axis field');
    return;
  }
  
  try {
    // Get column data
          const xResult = await window.electronAPI.getColumnData(currentFile.path, xField);
    if (!xResult.success || !xResult.data) {
      showError('Failed to load X-axis data: ' + (xResult.error || 'Unknown error'));
      return;
    }
    
    let yData: any[] | null = null;
    if (yField && chartType !== 'histogram') {
              const yResult = await window.electronAPI.getColumnData(currentFile.path, yField);
      if (!yResult.success || !yResult.data) {
        showError('Failed to load Y-axis data: ' + (yResult.error || 'Unknown error'));
        return;
      }
      yData = yResult.data.values;
    }
    
    // Create chart based on type
    const chartData = createChartData(chartType, xResult.data.values, yData, xField, yField);
    displayChart(chartData, chartType, xField, yField);
    
  } catch (error) {
    showError('Error creating chart: ' + (error instanceof Error ? error.message : 'Unknown error'));
  }
}

/**
 * Create chart data
 */
function createChartData(
  chartType: ChartType, 
  xData: any[], 
  yData: any[] | null, 
  xField: string, 
  yField: string
): any[] {
  switch (chartType) {
    case 'histogram':
      return [{
        x: xData,
        type: 'histogram',
        name: xField,
        nbinsx: 30,
        marker: {
          color: '#58a6ff',
          line: {
            color: '#1f6feb',
            width: 1
          }
        }
      }];
      
    case 'scatter':
      return [{
        x: xData,
        y: yData,
        type: 'scatter',
        mode: 'markers',
        name: `${xField} vs ${yField}`,
        marker: {
          color: '#58a6ff',
          size: 6,
          opacity: 0.7
        }
      }];
      
    case 'line':
      return [{
        x: xData,
        y: yData,
        type: 'scatter',
        mode: 'lines+markers',
        name: `${xField} vs ${yField}`,
        line: {
          color: '#58a6ff',
          width: 2
        },
        marker: {
          color: '#58a6ff',
          size: 4
        }
      }];
      
    case 'bar':
      return [{
        x: xData,
        y: yData,
        type: 'bar',
        name: `${xField} vs ${yField}`,
        marker: {
          color: '#58a6ff'
        }
      }];
      
    case 'box':
      return [{
        y: xData,
        type: 'box',
        name: xField,
        marker: {
          color: '#58a6ff'
        }
      }];
      
    default:
      return [];
  }
}

/**
 * Display chart
 */
function displayChart(chartData: any[], chartType: ChartType, xField: string, yField: string): void {
  chartContainer.innerHTML = '';
  
  // Check if Observable Plot is available
  if (!window.Plot) {
    console.error('❌ Observable Plot not loaded');
    chartContainer.innerHTML = `
      <div class="error-message">
        <h3>⚠️ Chart Library Not Loaded</h3>
        <p>Observable Plot failed to load. Please check your internet connection and refresh the page.</p>
        <button onclick="location.reload()" class="btn btn-primary">🔄 Reload Page</button>
      </div>
    `;
    return;
  }
  
  try {
    const Plot = window.Plot;
    
    // Create data for Observable Plot
    const data = chartData[0];
    let plot;
    
    switch (chartType) {
      case 'histogram':
        plot = Plot.plot({
          style: {
            background: '#161b22',
            color: '#f0f6fc'
          },
          marks: [
            Plot.rectY(data.x, Plot.binX({y: "count"}, {x: data.x, fill: "#58a6ff", stroke: "#1f6feb"}))
          ],
          x: {label: xField, grid: true, gridColor: "#30363d"},
          y: {label: "Count", grid: true, gridColor: "#30363d"},
          title: `Histogram: ${xField}`
        });
        break;
        
      case 'scatter':
        plot = Plot.plot({
          style: {
            background: '#161b22',
            color: '#f0f6fc'
          },
          marks: [
            Plot.dot(data.x, data.y, {fill: "#58a6ff", opacity: 0.7, r: 3})
          ],
          x: {label: xField, grid: true, gridColor: "#30363d"},
          y: {label: yField, grid: true, gridColor: "#30363d"},
          title: `Scatter Plot: ${xField} vs ${yField}`
        });
        break;
        
      case 'line':
        plot = Plot.plot({
          style: {
            background: '#161b22',
            color: '#f0f6fc'
          },
          marks: [
            Plot.line(data.x, data.y, {stroke: "#58a6ff", strokeWidth: 2}),
            Plot.dot(data.x, data.y, {fill: "#58a6ff", r: 2})
          ],
          x: {label: xField, grid: true, gridColor: "#30363d"},
          y: {label: yField, grid: true, gridColor: "#30363d"},
          title: `Line Chart: ${xField} vs ${yField}`
        });
        break;
        
      case 'bar':
        plot = Plot.plot({
          style: {
            background: '#161b22',
            color: '#f0f6fc'
          },
          marks: [
            Plot.barY(data.x, data.y, {fill: "#58a6ff"})
          ],
          x: {label: xField, grid: true, gridColor: "#30363d"},
          y: {label: yField, grid: true, gridColor: "#30363d"},
          title: `Bar Chart: ${xField} vs ${yField}`
        });
        break;
        
      case 'box':
        plot = Plot.plot({
          style: {
            background: '#161b22',
            color: '#f0f6fc'
          },
          marks: [
            Plot.boxX(data.y, {fill: "#58a6ff"})
          ],
          x: {label: xField, grid: true, gridColor: "#30363d"},
          y: {label: "Value", grid: true, gridColor: "#30363d"},
          title: `Box Plot: ${xField}`
        });
        break;
        
      default:
        chartContainer.innerHTML = '<div class="error-message">Unsupported chart type</div>';
        return;
    }
    
    chartContainer.appendChild(plot);
    
  } catch (error) {
    console.error('❌ Error creating chart:', error);
    chartContainer.innerHTML = `
      <div class="error-message">
        <h3>⚠️ Chart Creation Error</h3>
        <p>Failed to create chart: ${error instanceof Error ? error.message : 'Unknown error'}</p>
        <button onclick="location.reload()" class="btn btn-primary">🔄 Reload Page</button>
      </div>
    `;
  }
}

/**
 * Export to CSV
 */
function exportToCsv(): void {
  if (!currentData || !currentData.sampleData || !currentFile) {
    showError('No data to export');
    return;
  }
  
  const firstRow = currentData.sampleData[0];
  if (!firstRow) {
    showError('No data to export');
    return;
  }
  
  const headers = Object.keys(firstRow);
  const csvContent = [
    headers.join(','),
    ...currentData.sampleData.map(row => 
      headers.map(header => `"${row[header]}"`).join(',')
    )
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${currentFile.name.replace('.arrow', '')}_preview.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * Format file size in human readable format
 */
function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Format cell value for display
 */
function formatCellValue(value: any): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'number') return value.toLocaleString();
  if (typeof value === 'string') {
    return value.length > 50 ? value.substring(0, 50) + '...' : value;
  }
  return String(value);
}

/**
 * Show error message
 */
function showError(message: string): void {
  console.error('❌ Error:', message);
  alert(message);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('🎯 DOM Content Loaded - Starting initialization...');
  
  // Immediate debugging
  console.log('🔍 Immediate DOM check:');
  console.log('loading-fallback:', !!document.getElementById('loading-fallback'));
  console.log('main-app:', !!document.getElementById('main-app'));
  console.log('file-list:', !!document.getElementById('file-list'));
  
  // Show the main app immediately for testing
  const loadingFallback = document.getElementById('loading-fallback');
  const mainApp = document.getElementById('main-app');
  
  if (loadingFallback) {
    console.log('✅ Found loading fallback, hiding it');
    loadingFallback.style.display = 'none';
  } else {
    console.log('❌ Loading fallback not found');
  }
  
  if (mainApp) {
    console.log('✅ Found main app, showing it');
    mainApp.style.display = 'flex';
  } else {
    console.log('❌ Main app not found');
  }
  
  // Try to initialize with better error handling
  setTimeout(() => {
    init().catch(error => {
      console.error('❌ Failed to initialize application:', error);
      // Show error in the UI
      const body = document.body;
      if (body) {
        body.innerHTML = `
          <div style="padding: 20px; color: white; background: #161b22; min-height: 100vh; font-family: Arial, sans-serif;">
            <h1>🌿 Leaflet Arrow Explorer</h1>
            <h2>❌ Application Error</h2>
            <p><strong>Error:</strong> ${error.message}</p>
            <p><strong>Stack:</strong> ${error.stack}</p>
            <button onclick="location.reload()" style="padding: 10px 20px; background: #58a6ff; color: white; border: none; border-radius: 4px; cursor: pointer;">
              🔄 Reload Application
            </button>
          </div>
        `;
      }
    });
  }, 100); // Small delay to ensure DOM is ready
}); 