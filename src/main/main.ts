import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import * as fs from 'fs';
import { ArrowFile, ArrowData, ColumnData } from '../types';
import { processArrowFile, extractColumnData } from '../utils/arrow';

let mainWindow: BrowserWindow | null = null;

/**
 * Create the main application window
 */
function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
      allowRunningInsecureContent: false,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'default',
    show: false
  });

  // Set Content Security Policy to allow external CDN resources with proper MIME types
  mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    const url = details.url;
    
    // Fix MIME types for CDN resources
    if ((url.includes('unpkg.com') || url.includes('cdn.jsdelivr.net')) && url.endsWith('.js')) {
      callback({
        responseHeaders: {
          ...details.responseHeaders,
          'Content-Type': ['application/javascript; charset=utf-8'],
          'Content-Security-Policy': [
            "default-src 'self'; " +
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.jsdelivr.net; " +
            "style-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net; " +
            "img-src 'self' data: https:; " +
            "connect-src 'self' https:; " +
            "font-src 'self' https:; " +
            "object-src 'none'; " +
            "base-uri 'self'; " +
            "form-action 'self';"
          ]
        }
      });
    } else {
      callback({
        responseHeaders: {
          ...details.responseHeaders,
          'Content-Security-Policy': [
            "default-src 'self'; " +
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.jsdelivr.net; " +
            "style-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net; " +
            "img-src 'self' data: https:; " +
            "connect-src 'self' https:; " +
            "font-src 'self' https:; " +
            "object-src 'none'; " +
            "base-uri 'self'; " +
            "form-action 'self';"
          ]
        }
      });
    }
  });

  // Load the index.html file
  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  // Open DevTools in development
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

/**
 * Read data folder and return Arrow files
 */
async function readDataFolder(): Promise<ArrowFile[]> {
  const dataPath = path.join(__dirname, '../../data');
  const files = fs.readdirSync(dataPath);
  const arrowFiles = files.filter(file => file.endsWith('.arrow'));
  
  return arrowFiles.map(file => ({
    name: file,
    path: path.join(dataPath, file),
    size: fs.statSync(path.join(dataPath, file)).size
  }));
}

/**
 * Load Arrow file and extract data
 */
async function loadArrowFile(filePath: string): Promise<ArrowData> {
  const buffer = fs.readFileSync(filePath);
  const data = processArrowFile(buffer);
  data.filePath = filePath;
  return data;
}

/**
 * Get column data from Arrow file
 */
async function getColumnData(filePath: string, columnName: string): Promise<ColumnData> {
  const buffer = fs.readFileSync(filePath);
  return extractColumnData(buffer, columnName);
}

// IPC Handlers
ipcMain.handle('read-data-folder', async (): Promise<{ success: boolean; files?: ArrowFile[]; error?: string }> => {
  try {
    const files = await readDataFolder();
    return { success: true, files };
  } catch (error) {
    return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
});

ipcMain.handle('load-arrow-file', async (_event, filePath: string): Promise<{ success: boolean; data?: ArrowData; error?: string }> => {
  try {
    const data = await loadArrowFile(filePath);
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
});

ipcMain.handle('get-column-data', async (_event, filePath: string, columnName: string): Promise<{ success: boolean; data?: ColumnData; error?: string }> => {
  try {
    const data = await getColumnData(filePath, columnName);
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
});

// App event handlers
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
}); 