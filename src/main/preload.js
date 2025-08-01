const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  readDataFolder: () => ipcRenderer.invoke('read-data-folder'),
  loadArrowFile: (filePath) => ipcRenderer.invoke('load-arrow-file', filePath),
  getColumnData: (filePath, columnName) => ipcRenderer.invoke('get-column-data', filePath, columnName)
}); 