<template>
  <div class="upload-container">
    <div class="page-header">
      <h1>文件上传</h1>
      <p>请上传压缩文档（.zip, .rar），系统将自动解压获取实验文件。仅支持ZIP/RAR格式。</p>
    </div>

    <!-- 上传区域 -->
    <div class="upload-section">
      <el-card class="upload-card">
        <template #header>
          <div class="card-header">
            <span>拖拽上传</span>
            <el-button type="primary" @click="selectFiles">
              <el-icon><Plus /></el-icon>
              选择文件
            </el-button>
          </div>
        </template>

        <div 
          class="upload-area"
          :class="{ 'drag-over': isDragOver }"
          @drop="handleDrop"
          @dragover="handleDragOver"
          @dragleave="handleDragLeave"
        >
          <div class="upload-content">
            <el-icon size="48" color="#8a8886"><Upload /></el-icon>
            <h3>拖拽文件到此处，或点击选择文件</h3>
            <p>仅支持压缩文档 (.zip, .rar)</p>
          </div>
        </div>
      </el-card>
    </div>


    <!-- 操作按钮 -->
    <div class="action-buttons" v-if="hasFiles">
      <el-button @click="clearAllFiles">
        <el-icon><Delete /></el-icon>
        清空所有文件
      </el-button>
      <el-button type="primary" @click="proceedToGenerate">
        <el-icon><ArrowRight /></el-icon>
        继续生成报告
      </el-button>
    </div>

    <!-- 文件预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      :title="previewFile?.name"
      width="80%"
      center
    >
      <div class="file-preview">
        <div v-if="previewFile?.type.startsWith('image/')" class="image-preview">
          <img :src="previewFile.url" :alt="previewFile.name" />
        </div>
        <div v-else-if="previewFile?.type === 'text/plain'" class="text-preview">
          <pre>{{ previewContent }}</pre>
        </div>
        <div v-else class="unsupported-preview">
          <el-icon size="48"><Document /></el-icon>
          <p>暂不支持预览此文件类型</p>
          <p>文件名: {{ previewFile?.name }}</p>
          <p>文件大小: {{ formatFileSize(previewFile?.size) }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import FileList from '../components/FileList.vue'

const router = useRouter()

// 响应式数据
const isDragOver = ref(false)
const uploadedFiles = ref([])
const previewVisible = ref(false)
const previewFile = ref(null)
const previewContent = ref('')

// 计算属性
const hasFiles = computed(() => uploadedFiles.value.length > 0)


// 文件预览函数
const previewSelectedFile = (file) => {
  previewFile.value = file
  previewVisible.value = true
  
  // 如果是文本文件，尝试读取内容
  if (file.type === 'text/plain' || file.type === 'text/markdown') {
    // 这里需要实际读取文件内容
    previewContent.value = '文件内容预览功能待实现...'
  }
}

// 文件分类逻辑

// 事件处理
const handleDragOver = (e) => {
  e.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = (e) => {
  e.preventDefault()
  isDragOver.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDragOver.value = false
  
  const files = Array.from(e.dataTransfer.files)
  addFiles(files)
}

const selectFiles = async () => {
  try {
    const { ipcRenderer } = window.require('electron')
    const result = await ipcRenderer.invoke('select-files')
    
    if (!result.canceled && result.filePaths.length > 0) {
      // 这里需要将文件路径转换为File对象
      // 在实际应用中，需要读取文件内容
      const files = result.filePaths.map(path => {
        const name = path.split(/[/\\]/).pop()
        return {
          name,
          path,
          size: 0, // 需要实际获取文件大小
          type: getFileType(name),
          lastModified: Date.now()
        }
      })
      addFiles(files)
    }
  } catch (error) {
    console.error('选择文件失败:', error)
    ElMessage.error('选择文件失败')
  }
}

const addFiles = (files) => {
  const validFiles = files.filter(file =>
    file.name.toLowerCase().endsWith('.zip') ||
    file.name.toLowerCase().endsWith('.rar')
  );
  
  if (validFiles.length === 0) {
    ElMessage.error('仅支持上传ZIP或RAR格式的压缩文件');
    return;
  }
  
  validFiles.forEach(file => {
    // 检查文件是否已存在
    const exists = uploadedFiles.value.some(f => f.name === file.name && f.size === file.size)
    if (!exists) {
      const fileObj = {
        id: Date.now() + Math.random(),
        name: file.name,
        size: file.size,
        type: file.type || getFileType(file.name),
        lastModified: file.lastModified || Date.now(),
        url: file.path ? `file://${file.path}` : URL.createObjectURL(file),
      }
      uploadedFiles.value.push(fileObj)
    }
  });
  
  ElMessage.success(`成功添加 ${validFiles.length} 个压缩文件`);
}

const getFileType = (fileName) => {
  const ext = fileName.split('.').pop().toLowerCase()
  const typeMap = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'md': 'text/markdown',
    'py': 'text/x-python',
    'js': 'text/javascript',
    'java': 'text/x-java',
    'cpp': 'text/x-c++src',
    'c': 'text/x-csrc',
    'h': 'text/x-chdr'
  }
  return typeMap[ext] || 'application/octet-stream'
}

const removeFile = (fileId) => {
  const index = uploadedFiles.value.findIndex(f => f.id === fileId)
  if (index > -1) {
    uploadedFiles.value.splice(index, 1)
    ElMessage.success('文件已删除')
  }
}


const clearAllFiles = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有文件吗？', '确认操作', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    uploadedFiles.value = []
    ElMessage.success('已清空所有文件')
  } catch {
    // 用户取消操作
  }
}

const proceedToGenerate = () => {
  // 将文件信息传递给生成页面
  router.push({
    name: 'Generate',
    query: {
      files: JSON.stringify(uploadedFiles.value.map(f => ({
        id: f.id,
        name: f.name,
        type: f.type
      })))
    }
  })
}


const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

onMounted(() => {
  // 页面加载时的初始化操作
})
</script>

<style scoped>
.upload-container {
  padding: var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.page-header p {
  color: var(--color-text-secondary);
  margin: 0;
}

.upload-section {
  margin-bottom: var(--spacing-xl);
}

.upload-card {
  border-radius: var(--radius-card);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-area {
  min-height: 200px;
  border: 2px dashed var(--color-border-light);
  border-radius: var(--radius-large);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover,
.upload-area.drag-over {
  border-color: var(--color-primary);
  background-color: rgba(0, 120, 212, 0.05);
}

.upload-content {
  text-align: center;
  padding: var(--spacing-xl);
}

.upload-content h3 {
  margin: var(--spacing-md) 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
}

.upload-content p {
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-md) 0;
}

.supported-formats {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: center;
  flex-wrap: wrap;
}

.file-categories {
  margin-bottom: var(--spacing-xl);
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background-color: var(--color-bg-primary);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border-light);
}

.file-preview {
  max-height: 60vh;
  overflow-y: auto;
}

.image-preview img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-medium);
}

.text-preview pre {
  background-color: var(--color-bg-tertiary);
  padding: var(--spacing-md);
  border-radius: var(--radius-medium);
  overflow-x: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.5;
}

.unsupported-preview {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.unsupported-preview p {
  margin: var(--spacing-sm) 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-container {
    padding: var(--spacing-lg);
  }
  
  .card-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: stretch;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .supported-formats {
    flex-direction: column;
    align-items: center;
  }
}
</style>
