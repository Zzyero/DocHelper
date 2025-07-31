const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

let mainWindow
let backendProcess

// 创建主窗口
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 1000,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    titleBarStyle: 'default',
    frame: true,
    show: false,
    backgroundColor: '#f5f5f5'
  })

  // 开发环境加载本地服务器，生产环境加载打包后的文件
  const isDev = process.env.NODE_ENV === 'development'
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// 启动后端服务
function startBackend() {
  const backendPath = path.join(__dirname, '../backend/main.py')
  backendProcess = spawn('python', [backendPath], {
    cwd: path.join(__dirname, '../backend')
  })

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`)
  })

  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`)
  })
}

// 应用准备就绪
app.whenReady().then(() => {
  createWindow()
  startBackend()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

// 所有窗口关闭时退出应用
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (backendProcess) {
      backendProcess.kill()
    }
    app.quit()
  }
})

// IPC 通信处理
ipcMain.handle('select-files', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile', 'multiSelections'],
    filters: [
      { name: '所有文件', extensions: ['*'] },
      { name: '代码文件', extensions: ['py', 'js', 'java', 'cpp', 'c', 'h'] },
      { name: '文档文件', extensions: ['pdf', 'doc', 'docx', 'txt', 'md'] },
      { name: '图片文件', extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp'] }
    ]
  })
  return result
})

ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory']
  })
  return result
})

ipcMain.handle('save-file', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options)
  return result
})
