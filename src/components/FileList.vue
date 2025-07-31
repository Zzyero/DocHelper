<template>
  <div class="file-list">
    <div v-if="files.length === 0" class="empty-state">
      <el-icon size="32" color="#8a8886"><Folder /></el-icon>
      <p>暂无{{ getTypeLabel(type) }}文件</p>
    </div>
    
    <div v-else class="file-grid">
      <div 
        v-for="file in files" 
        :key="file.id"
        class="file-item fluent-card"
      >
        <div class="file-icon">
          <el-icon size="24" :color="getFileIconColor(file.type)">
            <component :is="getFileIcon(file.type)" />
          </el-icon>
        </div>
        
        <div class="file-info">
          <h4 class="file-name" :title="file.name">{{ file.name }}</h4>
          <p class="file-meta">
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
            <span class="file-date">{{ formatDate(file.lastModified) }}</span>
          </p>
        </div>
        
        <div class="file-actions">
          <el-button 
            text 
            size="small" 
            @click="$emit('preview', file)"
            :disabled="!canPreview(file)"
          >
            <el-icon><View /></el-icon>
          </el-button>
          <el-button 
            text 
            size="small" 
            type="danger"
            @click="$emit('remove', file.id)"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  files: {
    type: Array,
    default: () => []
  },
  type: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['remove', 'preview'])

const getTypeLabel = (type) => {
  const labels = {
    code: '代码',
    guide: '指导书',
    images: '图片',
    others: '其他'
  }
  return labels[type] || '文件'
}

const getFileIcon = (fileType) => {
  if (fileType.startsWith('image/')) return 'Picture'
  if (fileType.includes('pdf')) return 'Document'
  if (fileType.includes('word') || fileType.includes('doc')) return 'Document'
  if (fileType.includes('text')) return 'DocumentCopy'
  if (fileType.includes('javascript') || fileType.includes('python')) return 'Document'
  if (fileType.includes('zip') || fileType.includes('rar')) return 'FolderOpened'
  return 'Document'
}

const getFileIconColor = (fileType) => {
  if (fileType.startsWith('image/')) return '#ff8c00'
  if (fileType.includes('pdf')) return '#d13438'
  if (fileType.includes('word') || fileType.includes('doc')) return '#0078d4'
  if (fileType.includes('text')) return '#107c10'
  if (fileType.includes('javascript')) return '#f7df1e'
  if (fileType.includes('python')) return '#3776ab'
  if (fileType.includes('zip') || fileType.includes('rar')) return '#8a8886'
  return '#605e5c'
}

const canPreview = (file) => {
  return file.type.startsWith('image/') || 
         file.type === 'text/plain' || 
         file.type === 'text/markdown'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.file-list {
  min-height: 200px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xxl);
  color: var(--color-text-secondary);
  min-height: 200px;
}

.empty-state p {
  margin: var(--spacing-md) 0 0 0;
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.file-item {
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  transition: all 0.2s ease;
}

.file-item:hover {
  transform: translateY(-1px);
}

.file-icon {
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-meta {
  display: flex;
  gap: var(--spacing-sm);
  margin: 0;
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.file-actions {
  display: flex;
  gap: var(--spacing-xs);
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .file-grid {
    grid-template-columns: 1fr;
  }
  
  .file-item {
    padding: var(--spacing-sm);
  }
  
  .file-meta {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
}
</style>
