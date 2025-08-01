// Arrow file and data types
export interface ArrowFile {
  name: string;
  path: string;
  size: number;
}

export interface ArrowField {
  name: string;
  type: string;
  nullable: boolean;
}

export interface ArrowData {
  numRows: number;
  numCols: number;
  fields: ArrowField[];
  sampleData: Record<string, any>[];
  filePath: string;
}

export interface ColumnData {
  values: any[];
  totalRows: number;
  sampled: boolean;
}

// IPC response types
export interface IpcResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface FileListResponse extends IpcResponse<ArrowFile[]> {}
export interface ArrowDataResponse extends IpcResponse<ArrowData> {}
export interface ColumnDataResponse extends IpcResponse<ColumnData> {}

// Chart types
export type ChartType = 'histogram' | 'scatter' | 'line' | 'bar' | 'box';

export interface ChartData {
  x: any[];
  y?: any[];
  type: ChartType;
  name: string;
  [key: string]: any;
}

// Application state
export interface AppState {
  currentFile: ArrowFile | null;
  currentData: ArrowData | null;
  currentFields: ArrowField[];
} 