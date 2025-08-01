import { describe, it, expect, beforeEach } from 'jest';
import * as arrow from 'apache-arrow';
import { processArrowFile, extractColumnData, formatFileSize, formatCellValue } from '../../src/utils/arrow';
import { ArrowData, ColumnData } from '../../src/types';

describe('Arrow Utilities', () => {
  let sampleBuffer: Buffer;
  let sampleTable: arrow.Table;

  beforeEach(() => {
    // Create a sample Arrow table for testing
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

    sampleTable = arrow.tableFromArrays(vectors);
    sampleBuffer = arrow.tableToIPC(sampleTable);
  });

  describe('processArrowFile', () => {
    it('should process Arrow file and extract metadata correctly', () => {
      const result = processArrowFile(sampleBuffer);

      expect(result).toBeDefined();
      expect(result.numRows).toBe(5);
      expect(result.numCols).toBe(5);
      expect(result.fields).toHaveLength(5);
      expect(result.sampleData).toHaveLength(5);

      // Check field information
      const fieldNames = result.fields.map(f => f.name);
      expect(fieldNames).toContain('id');
      expect(fieldNames).toContain('name');
      expect(fieldNames).toContain('age');
      expect(fieldNames).toContain('salary');
      expect(fieldNames).toContain('active');

      // Check sample data
      expect(result.sampleData[0]).toHaveProperty('id');
      expect(result.sampleData[0]).toHaveProperty('name');
      expect(result.sampleData[0]).toHaveProperty('age');
      expect(result.sampleData[0]).toHaveProperty('salary');
      expect(result.sampleData[0]).toHaveProperty('active');
    });

    it('should handle empty Arrow table', () => {
      const emptyTable = arrow.tableFromArrays({});
      const emptyBuffer = arrow.tableToIPC(emptyTable);
      
      const result = processArrowFile(emptyBuffer);
      
      expect(result.numRows).toBe(0);
      expect(result.numCols).toBe(0);
      expect(result.fields).toHaveLength(0);
      expect(result.sampleData).toHaveLength(0);
    });

    it('should limit sample data to 1000 rows', () => {
      // Create a large dataset
      const largeData = {
        id: Array.from({ length: 2000 }, (_, i) => i),
        value: Array.from({ length: 2000 }, (_, i) => Math.random())
      };

      const largeVectors = {
        id: arrow.vectorFromArray(largeData.id, new arrow.Int32()),
        value: arrow.vectorFromArray(largeData.value, new arrow.Float64())
      };

      const largeTable = arrow.tableFromArrays(largeVectors);
      const largeBuffer = arrow.tableToIPC(largeTable);

      const result = processArrowFile(largeBuffer);

      expect(result.numRows).toBe(2000);
      expect(result.sampleData).toHaveLength(1000); // Should be limited to 1000
    });
  });

  describe('extractColumnData', () => {
    it('should extract column data correctly', () => {
      const result = extractColumnData(sampleBuffer, 'age');

      expect(result).toBeDefined();
      expect(result.values).toHaveLength(5);
      expect(result.totalRows).toBe(5);
      expect(result.sampled).toBe(false);
      expect(result.values).toEqual([25, 30, 35, 28, 32]);
    });

    it('should handle non-existent column', () => {
      expect(() => {
        extractColumnData(sampleBuffer, 'nonexistent');
      }).toThrow('Column nonexistent not found');
    });

    it('should sample large datasets', () => {
      // Create a large dataset
      const largeData = {
        id: Array.from({ length: 150000 }, (_, i) => i),
        value: Array.from({ length: 150000 }, (_, i) => Math.random())
      };

      const largeVectors = {
        id: arrow.vectorFromArray(largeData.id, new arrow.Int32()),
        value: arrow.vectorFromArray(largeData.value, new arrow.Float64())
      };

      const largeTable = arrow.tableFromArrays(largeVectors);
      const largeBuffer = arrow.tableToIPC(largeTable);

      const result = extractColumnData(largeBuffer, 'id', 100000);

      expect(result.totalRows).toBe(150000);
      expect(result.values).toHaveLength(100000); // Should be limited
      expect(result.sampled).toBe(true);
    });

    it('should handle different data types', () => {
      const stringResult = extractColumnData(sampleBuffer, 'name');
      expect(stringResult.values).toEqual(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']);

      const boolResult = extractColumnData(sampleBuffer, 'active');
      expect(boolResult.values).toEqual([true, false, true, true, false]);

      const floatResult = extractColumnData(sampleBuffer, 'salary');
      expect(floatResult.values).toEqual([50000, 60000, 70000, 55000, 65000]);
    });
  });

  describe('formatFileSize', () => {
    it('should format file sizes correctly', () => {
      expect(formatFileSize(0)).toBe('0 Bytes');
      expect(formatFileSize(1024)).toBe('1 KB');
      expect(formatFileSize(1024 * 1024)).toBe('1 MB');
      expect(formatFileSize(1024 * 1024 * 1024)).toBe('1 GB');
      expect(formatFileSize(1500)).toBe('1.46 KB');
      expect(formatFileSize(1500000)).toBe('1.43 MB');
    });
  });

  describe('formatCellValue', () => {
    it('should format cell values correctly', () => {
      expect(formatCellValue(null)).toBe('');
      expect(formatCellValue(undefined)).toBe('');
      expect(formatCellValue(1234)).toBe('1,234');
      expect(formatCellValue(1234.56)).toBe('1,234.56');
      expect(formatCellValue('short')).toBe('short');
      expect(formatCellValue('a'.repeat(60))).toBe('a'.repeat(50) + '...');
      expect(formatCellValue(true)).toBe('true');
      expect(formatCellValue(false)).toBe('false');
    });
  });
}); 