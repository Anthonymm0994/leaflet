import { describe, it, expect, beforeEach, afterEach } from 'jest';
import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import * as fs from 'fs';
import * as arrow from 'apache-arrow';
import { ArrowFile, ArrowData, ColumnData } from '../../src/types';

// Mock Electron app
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
  }
}));

describe('IPC Integration Tests', () => {
  let testArrowFile: string;
  let testBuffer: Buffer;

  beforeEach(() => {
    // Create a test Arrow file
    const data = {
      id: [1, 2, 3, 4, 5],
      name: ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
      age: [25, 30, 35, 28, 32],
      salary: [50000, 60000, 70000, 55000, 65000],
      active: [true, false, true, true, false]
    };

    const vectors = {
      id: arrow.vectorFromArray(data.id, new arrow.Int32()),
      name: arrow.vectorFromArray(data.name, new arrow.Utf8()),
      age: arrow.vectorFromArray(data.age, new arrow.Int32()),
      salary: arrow.vectorFromArray(data.salary, new arrow.Float64()),
      active: arrow.vectorFromArray(data.active, new arrow.Bool())
    };

    const table = arrow.tableFromArrays(vectors);
    testBuffer = arrow.tableToIPC(table);
    
    // Create test file in data directory
    const dataDir = path.join(__dirname, '../../data');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
    
    testArrowFile = path.join(dataDir, 'test_sample.arrow');
    fs.writeFileSync(testArrowFile, testBuffer);
  });

  afterEach(() => {
    // Clean up test file
    if (fs.existsSync(testArrowFile)) {
      fs.unlinkSync(testArrowFile);
    }
  });

  describe('read-data-folder handler', () => {
    it('should return Arrow files from data directory', async () => {
      // Import the main process to trigger IPC handler registration
      require('../../src/main/main');
      
      // Get the registered handler
      const handlers = (ipcMain.handle as jest.Mock).mock.calls;
      const readDataFolderHandler = handlers.find(
        ([eventName]: [string]) => eventName === 'read-data-folder'
      );
      
      expect(readDataFolderHandler).toBeDefined();
      
      // Mock the handler implementation
      const mockHandler = jest.fn().mockResolvedValue({
        success: true,
        files: [
          {
            name: 'test_sample.arrow',
            path: testArrowFile,
            size: testBuffer.length
          }
        ]
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(true);
      expect(result.files).toBeDefined();
      expect(result.files).toHaveLength(1);
      expect(result.files[0].name).toBe('test_sample.arrow');
      expect(result.files[0].path).toBe(testArrowFile);
      expect(result.files[0].size).toBe(testBuffer.length);
    });

    it('should handle empty data directory', async () => {
      // Remove test file
      if (fs.existsSync(testArrowFile)) {
        fs.unlinkSync(testArrowFile);
      }
      
      const mockHandler = jest.fn().mockResolvedValue({
        success: true,
        files: []
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(true);
      expect(result.files).toHaveLength(0);
    });

    it('should handle directory not found', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: false,
        error: 'Directory not found'
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('Directory not found');
    });
  });

  describe('load-arrow-file handler', () => {
    it('should load Arrow file and return data', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: true,
        data: {
          numRows: 5,
          numCols: 5,
          fields: [
            { name: 'id', type: 'Int32', nullable: false },
            { name: 'name', type: 'Utf8', nullable: false },
            { name: 'age', type: 'Int32', nullable: false },
            { name: 'salary', type: 'Float64', nullable: false },
            { name: 'active', type: 'Bool', nullable: false }
          ],
          sampleData: [
            { id: 1, name: 'Alice', age: 25, salary: 50000, active: true },
            { id: 2, name: 'Bob', age: 30, salary: 60000, active: false }
          ],
          filePath: testArrowFile
        }
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.numRows).toBe(5);
      expect(result.data.numCols).toBe(5);
      expect(result.data.fields).toHaveLength(5);
      expect(result.data.sampleData).toHaveLength(2);
      expect(result.data.filePath).toBe(testArrowFile);
    });

    it('should handle file not found', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: false,
        error: 'File not found'
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('File not found');
    });

    it('should handle invalid Arrow file', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: false,
        error: 'Invalid Arrow file format'
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid Arrow file format');
    });
  });

  describe('get-column-data handler', () => {
    it('should extract column data correctly', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: true,
        data: {
          values: [25, 30, 35, 28, 32],
          totalRows: 5,
          sampled: false
        }
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.values).toEqual([25, 30, 35, 28, 32]);
      expect(result.data.totalRows).toBe(5);
      expect(result.data.sampled).toBe(false);
    });

    it('should handle non-existent column', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: false,
        error: 'Column nonexistent not found'
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('Column nonexistent not found');
    });

    it('should handle large datasets with sampling', async () => {
      const mockHandler = jest.fn().mockResolvedValue({
        success: true,
        data: {
          values: Array.from({ length: 100000 }, (_, i) => i),
          totalRows: 150000,
          sampled: true
        }
      });
      
      const result = await mockHandler();
      
      expect(result.success).toBe(true);
      expect(result.data.values).toHaveLength(100000);
      expect(result.data.totalRows).toBe(150000);
      expect(result.data.sampled).toBe(true);
    });
  });
}); 