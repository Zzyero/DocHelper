<template>
  <div class="upload-container">
    <div class="page-header">
      <h1>文件上传</h1>
      <p>支持上传压缩文档（.zip, .rar）自动解压，或直接上传实验文件</p>
    </div>

    <!-- 上传选项卡 -->
    <div class="upload-tabs">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="压缩包上传" name="archive">
          <div class="tab-content">
            <p class="tab-description">上传ZIP/RAR压缩包，系统将自动解压获取实验文件</p>
            
            <!-- 压缩包上传区域 -->
            <div class="upload-section">
              <el-card class="upload-card">
                <template #header>
                  <div class="card-header">
                    <span>拖拽上传压缩包</span>
                    <el-button type="primary" @click="selectArchiveFiles">
                      <el-icon><Plus /></el-icon>
                      选择压缩包
                    </el-button>
                  </div>
                </template>

                <div
                  class="upload-area"
                  :class="{ 'drag-over': isDragOver }"
                  @drop="handleArchiveDrop"
                  @dragover="handleDragOver"
                  @dragleave="handleDragLeave"
                  @click="selectArchiveFiles"
                >
                  <div class="upload-content">
                    <el-icon size="48" color="#8a8886"><Upload /></el-icon>
                    <h3>拖拽压缩包到此处，或点击选择文件</h3>
                    <p>仅支持 .zip, .rar 格式</p>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="文件上传" name="files">
          <div class="tab-content">
            <p class="tab-description">直接上传实验文件（代码、文档、图片等）</p>
            
            <!-- 文件上传区域 -->
            <div class="upload-section">
              <el-card class="upload-card">
                <template #header>
                  <div class="card-header">
                    <span>拖拽文件上传</span>
                    <el-button type="primary" @click="selectNormalFiles">
                      <el-icon><Plus /></el-icon>
                      选择文件
                    </el-button>
                  </div>
                </template>

                <div
                  class="upload-area"
                  :class="{ 'drag-over': isDragOver }"
                  @drop="handleFilesDrop"
                  @dragover="handleDragOver"
                  @dragleave="handleDragLeave"
                  @click="selectNormalFiles"
                >
                  <div class="upload-content">
                    <el-icon size="48" color="#8a8886"><Upload /></el-icon>
                    <h3>拖拽文件到此处，或点击选择文件</h3>
                    <p>支持多种文件格式</p>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 解压加载指示器 -->
    <div v-if="isExtracting" class="extracting-indicator">
      <el-card>
        <div class="extracting-content">
          <div class="loading-overlay">
            <el-icon class="is-loading" size="48" color="#409eff"><Loading /></el-icon>
            <h3>正在解压文件中...</h3>
            <p>请稍候，系统正在处理您的文件</p>
          </div>
        </div>
      </el-card>
    </div>


    <!-- 操作按钮 -->
    <div class="action-buttons" v-if="currentStep === 1 && hasFiles">
      <el-button @click="clearAllFiles">
        <el-icon><Delete /></el-icon>
        清空文件
      </el-button>
    </div>
    
    <div class="action-buttons" v-if="currentStep === 2">
      <el-button type="primary" @click="proceedToGenerate">
        <el-icon><ArrowRight /></el-icon>
        确认并继续
      </el-button>
    </div>

    <!-- 解压后文件列表 -->
    <div v-if="currentStep === 2" class="extracted-files">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>解压后的文件</span>
            <el-button type="primary" @click="resetUpload">
              <el-icon><Refresh /></el-icon>
              重新上传
            </el-button>
          </div>
        </template>
        
        <div class="file-list">
          <div v-for="(file, index) in extractedFiles" :key="index" class="file-item">
            <el-icon><Document /></el-icon>
            <span class="file-name">{{ file.name }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
          </div>
          
          <div v-if="extractedFiles.length === 0" class="no-files">
            <el-icon><Warning /></el-icon>
            <p>解压后未找到有效文件</p>
          </div>
        </div>
      </el-card>
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
const currentStep = ref(1) // 1: 上传, 2: 解压完成
const extractedFiles = ref([])
const isExtracting = ref(false) // 解压状态
const activeTab = ref('archive') // 默认选中压缩包上传

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
    // 创建文件输入元素
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.zip,.rar';
    input.onchange = async (e) => {
      const files = Array.from(e.target.files);
      if (files.length > 0) {
        await addFiles(files);
      }
    };
    input.click();
  } catch (error) {
    console.error('选择文件失败:', error);
    ElMessage.error('选择文件失败');
  }
}

// 普通文件上传相关函数
const selectNormalFiles = async () => {
  try {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    input.onchange = async (e) => {
      const files = Array.from(e.target.files);
      if (files.length > 0) {
        await uploadNormalFiles(files);
      }
    };
    input.click();
  } catch (error) {
    console.error('选择文件失败:', error);
    ElMessage.error('选择文件失败');
  }
}

const handleFilesDrop = (e) => {
  e.preventDefault();
  isDragOver.value = false;
  
  const files = Array.from(e.dataTransfer.files);
  uploadNormalFiles(files);
}

const uploadNormalFiles = async (files) => {
  try {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    const response = await fetch('/api/v1/files/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}: 上传失败`);
    }

    const data = await response.json();
    
    // 直接跳转到生成页面
    router.push({
      name: 'Generate',
      query: {
        files: JSON.stringify(data.files.map(f => ({
          id: Date.now() + Math.random(),
          name: f.name,
          path: f.path,
          size: f.size,
          type: f.type,
          category: f.category
        })))
      }
    });
    
    ElMessage.success(`成功上传 ${data.files.length} 个文件`);
  } catch (error) {
    console.error('文件上传失败:', error);
    ElMessage.error(`文件上传失败: ${error.message}`);
  }
}

// 压缩包上传相关函数
const selectArchiveFiles = async () => {
  try {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.zip,.rar';
    input.onchange = async (e) => {
      const files = Array.from(e.target.files);
      if (files.length > 0) {
        await addFiles(files);
      }
    };
    input.click();
  } catch (error) {
    console.error('选择文件失败:', error);
    ElMessage.error('选择文件失败');
  }
}

const handleArchiveDrop = (e) => {
  e.preventDefault();
  isDragOver.value = false;
  
  const files = Array.from(e.dataTransfer.files);
  addFiles(files);
}

const addFiles = async (files) => {
  const validFiles = files.filter(file =>
    file.name.toLowerCase().endsWith('.zip') ||
    file.name.toLowerCase().endsWith('.rar')
  );
  
  if (validFiles.length === 0) {
    ElMessage.error('仅支持上传ZIP或RAR格式的压缩文件');
    return;
  }
  
  // 只允许上传一个压缩包
  if (uploadedFiles.value.length > 0) {
    ElMessage.warning('已存在压缩包，将替换为新上传的文件');
    uploadedFiles.value = [];
  }
  
  const file = validFiles[0];
  const fileObj = {
    id: Date.now() + Math.random(),
    name: file.name,
    size: file.size,
    type: file.type || getFileType(file.name),
    lastModified: file.lastModified || Date.now(),
    url: file.path ? `file://${file.path}` : URL.createObjectURL(file),
    originalFile: file // 保存原始文件引用
  };
  uploadedFiles.value.push(fileObj);
  
  // 保存上传的文件信息到后端
  await saveUploadedFiles();
  
  // 自动解压
  await extractArchive(fileObj);
}

const extractArchive = async (fileObj) => {
  // 设置解压状态为true
  isExtracting.value = true;
  
  try {
    // 需要重新获取原始的File对象
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.zip,.rar';
    
    // 创建一个Promise来处理文件选择
    const getFile = () => {
      return new Promise((resolve, reject) => {
        input.onchange = (e) => {
          const files = Array.from(e.target.files);
          if (files.length > 0) {
            resolve(files[0]);
          } else {
            reject(new Error('未选择文件'));
          }
        };
        input.click();
      });
    };
    
    // 如果fileObj有原始文件引用，直接使用
    let actualFile;
    if (fileObj.originalFile) {
      actualFile = fileObj.originalFile;
    } else {
      // 否则提示用户重新选择
      ElMessage.warning('请重新选择文件进行上传');
      actualFile = await getFile();
    }
    
    const formData = new FormData();
    formData.append('file', actualFile);
    
    const response = await fetch('/api/v1/files/upload-and-extract', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}: 解压失败`);
    }
    
    const data = await response.json();
    extractedFiles.value = data.extracted_files;
    currentStep.value = 2;
    ElMessage.success(`解压成功，共 ${data.count} 个文件`);
  } catch (error) {
    console.error('解压失败:', error);
    ElMessage.error(`解压失败: ${error.message}`);
    uploadedFiles.value = []; // 清空无效的压缩包
  } finally {
    // 无论成功还是失败，都将解压状态设置为false
    isExtracting.value = false;
  }
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
    
    // 同时清除后端保存的文件信息
    await saveUploadedFiles()
    
    ElMessage.success('已清空所有文件')
  } catch {
    // 用户取消操作
  }
}

const proceedToGenerate = async () => {
  try {
    // 创建项目记录
    const projectData = new FormData();
    projectData.append('name', '实验报告项目');
    projectData.append('description', '通过文件上传自动生成的项目');
    
    // 添加文件路径
    extractedFiles.value.forEach(file => {
      projectData.append('file_paths', file.path);
    });

    const response = await fetch('/api/v1/projects', {
      method: 'POST',
      body: projectData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}: 创建项目失败`);
    }

    const projectResult = await response.json();
    const projectId = projectResult.project.id;

    // 跳转到生成页面，传递项目ID
    router.push({
      name: 'Generate',
      query: {
        projectId: projectId,
        files: JSON.stringify(extractedFiles.value.map(f => ({
          id: Date.now() + Math.random(),
          name: f.name,
          path: f.path,
          size: f.size,
          type: getFileType(f.name)
        })))
      }
    });
    
    ElMessage.success('项目创建成功，正在跳转到生成页面...');
  } catch (error) {
    console.error('创建项目失败:', error);
    ElMessage.error('创建项目失败: ' + error.message);
  }
}

const resetUpload = async () => {
  uploadedFiles.value = [];
  extractedFiles.value = [];
  currentStep.value = 1;
  
  // 同时清除后端保存的文件信息
  await saveUploadedFiles();
}


const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 保存上传的文件信息到后端
const saveUploadedFiles = async () => {
  try {
    const filesToSave = uploadedFiles.value.map(file => ({
      id: file.id,
      name: file.name,
      size: file.size,
      type: file.type,
      lastModified: file.lastModified,
      url: file.url
    }));
    
    const response = await fetch('/api/v1/settings/user-settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        uploaded_files: filesToSave
      })
    });
    
    if (!response.ok) {
      console.warn('保存上传文件信息失败');
    }
  } catch (error) {
    console.error('保存上传文件信息失败:', error);
  }
}

onMounted(async () => {
  // 页面加载时从后端加载已保存的文件信息
  try {
    const response = await fetch('/api/v1/settings/user-settings');
    if (response.ok) {
      const data = await response.json();
      if (data.uploaded_files && data.uploaded_files.length > 0) {
        uploadedFiles.value = data.uploaded_files.map(file => ({
          ...file,
          originalFile: null // 原始文件对象无法序列化，需要重新选择
        }));
      }
    }
  } catch (error) {
    console.error('加载上传文件信息失败:', error);
  }
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

.extracted-files {
  margin-bottom: var(--spacing-xl);
}

.file-list {
  max-height: 400px;
  overflow-y: auto;
}

.file-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border-light);
  transition: background-color 0.2s ease;
}

.file-item:hover {
  background-color: var(--color-bg-secondary);
}

.file-item:last-child {
  border-bottom: none;
}

.file-item .el-icon {
  margin-right: var(--spacing-sm);
  color: var(--color-text-secondary);
}

.file-name {
  flex: 1;
  margin-right: var(--spacing-md);
  font-weight: 500;
  color: var(--color-text-primary);
}

.file-size {
  color: var(--color-text-secondary);
  font-size: 14px;
}

.no-files {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.no-files .el-icon {
  margin-bottom: var(--spacing-sm);
  color: var(--color-warning);
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
  
  .file-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
  
  .file-name {
    margin-right: 0;
  }
}

.extracting-indicator {
  margin-bottom: var(--spacing-xl);
}

.extracting-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  text-align: center;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-overlay h3 {
  margin: var(--spacing-md) 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
}

.loading-overlay p {
  color: var(--color-text-secondary);
  margin: 0;
}

.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
