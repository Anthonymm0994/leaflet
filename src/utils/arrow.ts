import * as arrow from 'apache-arrow';
import { ArrowData, ArrowField, ColumnData } from '../types';

/**
 * Process Arrow file and extract metadata and sample data
 */
export function processArrowFile(buffer: Buffer): ArrowData {
  const table = arrow.tableFromIPC(buffer);
  const schema = table.schema;
  
  // Extract field information
  const fields: ArrowField[] = schema.fields.map(field => ({
    name: field.name,
    type: field.type.toString(),
    nullable: field.nullable
  }));
  
  // Get basic statistics
  const numRows = table.numRows;
  const numCols = table.numCols;
  
  // Sample data for preview (first 1000 rows)
  const sampleSize = Math.min(1000, numRows);
  const sampleData: Record<string, any>[] = [];
  
  for (let i = 0; i < sampleSize; i++) {
    const row: Record<string, any> = {};
    for (let j = 0; j < numCols; j++) {
      const column = table.getChildAt(j);
      const field = fields[j];
      if (column && field) {
        row[field.name] = column.get(i);
      }
    }
    sampleData.push(row);
  }
  
  return {
    numRows,
    numCols,
    fields,
    sampleData,
    filePath: ''
  };
}

/**
 * Extract column data from Arrow table
 */
export function extractColumnData(
  buffer: Buffer, 
  columnName: string, 
  maxValues: number = 100000
): ColumnData {
  const table = arrow.tableFromIPC(buffer);
  
  // Find the column
  const columnIndex = table.schema.fields.findIndex(f => f.name === columnName);
  if (columnIndex === -1) {
    throw new Error(`Column ${columnName} not found`);
  }
  
  const column = table.getChildAt(columnIndex);
  if (!column) {
    throw new Error(`Column ${columnName} not found`);
  }
  
  const data: any[] = [];
  
  // Get all values (for smaller datasets) or sample (for large datasets)
  const numRows = Math.min(table.numRows, maxValues);
  
  for (let i = 0; i < numRows; i++) {
    data.push(column.get(i));
  }
  
  return {
    values: data,
    totalRows: table.numRows,
    sampled: table.numRows > maxValues
  };
}

/**
 * Format file size in human readable format
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Format cell value for display
 */
export function formatCellValue(value: any): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'number') return value.toLocaleString();
  if (typeof value === 'string') {
    return value.length > 50 ? value.substring(0, 50) + '...' : value;
  }
  return String(value);
} 