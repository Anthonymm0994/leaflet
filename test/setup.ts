// Test setup file for Jest

// Mock Electron
jest.mock('electron', () => ({
  app: {
    whenReady: jest.fn().mockResolvedValue(undefined),
    on: jest.fn(),
    quit: jest.fn()
  },
  BrowserWindow: jest.fn().mockImplementation(() => ({
    loadFile: jest.fn(),
    on: jest.fn(),
    once: jest.fn(),
    webContents: {
      openDevTools: jest.fn(),
      session: {
        webRequest: {
          onHeadersReceived: jest.fn()
        }
      }
    }
  })),
  ipcMain: {
    handle: jest.fn()
  },
  ipcRenderer: {
    invoke: jest.fn()
  }
}));

// Mock DOM APIs for renderer tests
global.document = {
  getElementById: jest.fn(),
  querySelectorAll: jest.fn(),
  createElement: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn()
} as any;

global.window = {
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  location: {
    reload: jest.fn()
  }
} as any;

// Mock console methods
global.console = {
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  info: jest.fn(),
  debug: jest.fn()
} as any;

// Mock alert
global.alert = jest.fn();

// Mock URL.createObjectURL and URL.revokeObjectURL
global.URL = {
  createObjectURL: jest.fn(),
  revokeObjectURL: jest.fn()
} as any;

// Mock Blob
global.Blob = jest.fn().mockImplementation((content, options) => ({
  content,
  options,
  size: content.length
}));

// Mock fetch for external library loading
global.fetch = jest.fn();

// Setup global test utilities
(global as any).testUtils = {
  createMockArrowTable: (data: any) => {
    // Mock Arrow table creation
    const firstValue = Object.values(data)[0];
    return {
      numRows: Array.isArray(firstValue) ? firstValue.length : 0,
      numCols: Object.keys(data).length,
      schema: {
        fields: Object.keys(data).map(name => ({
          name,
          type: 'mock',
          nullable: false
        }))
      },
      getChildAt: jest.fn().mockReturnValue({
        get: jest.fn()
      })
    };
  },
  
  createMockElement: (id: string, properties: any = {}) => {
    return {
      id,
      innerHTML: '',
      textContent: '',
      className: '',
      style: { display: '' },
      classList: {
        add: jest.fn(),
        remove: jest.fn(),
        toggle: jest.fn(),
        contains: jest.fn()
      },
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      appendChild: jest.fn(),
      ...properties
    };
  }
};

// Global test timeout
jest.setTimeout(10000); 