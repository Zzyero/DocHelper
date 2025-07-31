<template>
  <div class="templates-container">
    <div class="page-header">
      <h1>模板库</h1>
      <p>管理和使用文档模板</p>
    </div>

    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索模板..."
          clearable
          style="width: 300px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select v-model="filterCategory" placeholder="分类筛选" clearable style="width: 150px">
          <el-option label="全部" value="" />
          <el-option label="学术论文" value="academic" />
          <el-option label="实验报告" value="lab" />
          <el-option label="技术文档" value="technical" />
          <el-option label="自定义" value="custom" />
        </el-select>
      </div>
      
      <div class="toolbar-right">
        <el-button type="primary" @click="showUploadDialog = true">
          <el-icon><Plus /></el-icon>
          上传模板
        </el-button>
      </div>
    </div>

    <!-- 模板网格 -->
    <div class="templates-grid">
      <div
        v-for="template in filteredTemplates"
        :key="template.id"
        class="template-card fluent-card"
        @click="selectTemplate(template)"
        :class="{ 'selected': selectedTemplate?.id === template.id }"
      >
        <div class="template-preview">
          <div class="template-icon">
            <el-icon size="32" :color="getTemplateIconColor(template.category)">
              <component :is="getTemplateIcon(template.category)" />
            </el-icon>
          </div>
          <div class="template-badge" v-if="template.isDefault">
            <el-tag size="small" type="primary">默认</el-tag>
          </div>
        </div>
        
        <div class="template-info">
          <h3 class="template-name">{{ template.name }}</h3>
          <p class="template-description">{{ template.description }}</p>
          
          <div class="template-meta">
            <div class="template-category">
              <el-tag size="small" :type="getCategoryTagType(template.category)">
                {{ getCategoryLabel(template.category) }}
              </el-tag>
            </div>
            <div class="template-stats">
              <span class="usage-count">
                <el-icon size="14"><View /></el-icon>
                {{ template.usageCount || 0 }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="template-actions">
          <el-button text size="small" @click.stop="previewTemplate(template)">
            <el-icon><View /></el-icon>
          </el-button>
          <el-button text size="small" @click.stop="useTemplate(template)">
            <el-icon><Check /></el-icon>
          </el-button>
          <el-dropdown @command="handleTemplateAction" trigger="click" v-if="!template.isDefault">
            <el-button text size="small" @click.stop>
              <el-icon><MoreFilled /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item :command="{ action: 'edit', template }">编辑</el-dropdown-item>
                <el-dropdown-item :command="{ action: 'duplicate', template }">复制</el-dropdown-item>
                <el-dropdown-item :command="{ action: 'delete', template }" divided>删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredTemplates.length === 0" class="empty-state">
      <el-icon size="48" color="#8a8886"><Document /></el-icon>
      <p>{{ searchKeyword ? '未找到匹配的模板' : '暂无模板' }}</p>
      <el-button type="primary" @click="showUploadDialog = true">
        上传第一个模板
      </el-button>
    </div>

    <!-- 模板详情侧边栏 -->
    <el-drawer
      v-model="detailDrawerVisible"
      title="模板详情"
      direction="rtl"
      size="400px"
    >
      <div v-if="selectedTemplate" class="template-detail">
        <div class="detail-header">
          <div class="template-icon-large">
            <el-icon size="48" :color="getTemplateIconColor(selectedTemplate.category)">
              <component :is="getTemplateIcon(selectedTemplate.category)" />
            </el-icon>
          </div>
          <div class="template-title">
            <h2>{{ selectedTemplate.name }}</h2>
            <p>{{ selectedTemplate.description }}</p>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="info-item">
              <span class="label">分类:</span>
              <el-tag size="small" :type="getCategoryTagType(selectedTemplate.category)">
                {{ getCategoryLabel(selectedTemplate.category) }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">格式:</span>
              <span>{{ selectedTemplate.format || 'Markdown' }}</span>
            </div>
            <div class="info-item">
              <span class="label">使用次数:</span>
              <span>{{ selectedTemplate.usageCount || 0 }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间:</span>
              <span>{{ formatDate(selectedTemplate.createdAt) }}</span>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedTemplate.variables">
            <h4>模板变量</h4>
            <div class="variables-list">
              <div
                v-for="variable in selectedTemplate.variables"
                :key="variable.name"
                class="variable-item"
              >
                <code>{{ variable.name }}</code>
                <span class="variable-desc">{{ variable.description }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-actions">
            <el-button type="primary" @click="useTemplate(selectedTemplate)">
              <el-icon><Check /></el-icon>
              使用此模板
            </el-button>
            <el-button @click="previewTemplate(selectedTemplate)">
              <el-icon><View /></el-icon>
              预览模板
            </el-button>
          </div>
        </div>
      </div>
    </el-drawer>

    <!-- 上传模板对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传模板"
      width="600px"
      center
    >
      <el-form :model="uploadForm" label-width="100px" label-position="left">
        <el-form-item label="模板名称" required>
          <el-input v-model="uploadForm.name" placeholder="请输入模板名称" />
        </el-form-item>
        
        <el-form-item label="模板描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入模板描述"
          />
        </el-form-item>
        
        <el-form-item label="模板分类">
          <el-select v-model="uploadForm.category" placeholder="选择分类">
            <el-option label="学术论文" value="academic" />
            <el-option label="实验报告" value="lab" />
            <el-option label="技术文档" value="technical" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="模板文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :show-file-list="true"
            :limit="1"
            accept=".docx,.md,.tex"
            @change="handleFileChange"
          >
            <el-button>
              <el-icon><Upload /></el-icon>
              选择文件
            </el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 .docx, .md, .tex 格式文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="uploadTemplate" :loading="uploading">
          上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 模板预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="模板预览"
      width="80%"
      center
    >
      <div class="template-preview-content">
        <div class="preview-toolbar">
          <el-button-group>
            <el-button @click="previewMode = 'source'" :type="previewMode === 'source' ? 'primary' : ''">
              源码
            </el-button>
            <el-button @click="previewMode = 'rendered'" :type="previewMode === 'rendered' ? 'primary' : ''">
              预览
            </el-button>
          </el-button-group>
        </div>
        
        <div class="preview-body">
          <div v-if="previewMode === 'source'" class="source-view">
            <pre><code>{{ previewContent }}</code></pre>
          </div>
          <div v-else class="rendered-view" v-html="renderedPreviewContent"></div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const searchKeyword = ref('')
const filterCategory = ref('')
const selectedTemplate = ref(null)
const detailDrawerVisible = ref(false)
const showUploadDialog = ref(false)
const previewDialogVisible = ref(false)
const previewMode = ref('rendered')
const previewContent = ref('')
const renderedPreviewContent = ref('')
const uploading = ref(false)

const uploadForm = ref({
  name: '',
  description: '',
  category: 'custom',
  file: null
})

// 模拟模板数据
const templates = ref([
  {
    id: 'default',
    name: '默认模板',
    description: '通用的实验报告模板，适用于大多数场景',
    category: 'lab',
    format: 'Markdown',
    isDefault: true,
    usageCount: 156,
    createdAt: new Date('2024-01-01'),
    variables: [
      { name: '{{title}}', description: '报告标题' },
      { name: '{{author}}', description: '作者姓名' },
      { name: '{{date}}', description: '创建日期' }
    ]
  },
  {
    id: 'academic',
    name: '学术论文模板',
    description: '符合学术规范的论文模板，包含摘要、关键词等',
    category: 'academic',
    format: 'LaTeX',
    isDefault: true,
    usageCount: 89,
    createdAt: new Date('2024-01-02'),
    variables: [
      { name: '{{title}}', description: '论文标题' },
      { name: '{{abstract}}', description: '摘要内容' },
      { name: '{{keywords}}', description: '关键词' }
    ]
  },
  {
    id: 'technical',
    name: '技术文档模板',
    description: '适用于技术文档和API文档的模板',
    category: 'technical',
    format: 'Markdown',
    isDefault: true,
    usageCount: 67,
    createdAt: new Date('2024-01-03')
  },
  {
    id: 'custom1',
    name: '自定义模板1',
    description: '用户上传的自定义模板',
    category: 'custom',
    format: 'Word',
    isDefault: false,
    usageCount: 12,
    createdAt: new Date('2024-01-10')
  }
])

// 计算属性
const filteredTemplates = computed(() => {
  let result = templates.value

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(template =>
      template.name.toLowerCase().includes(keyword) ||
      template.description.toLowerCase().includes(keyword)
    )
  }

  // 分类筛选
  if (filterCategory.value) {
    result = result.filter(template => template.category === filterCategory.value)
  }

  return result
})

// 生命周期
onMounted(() => {
  // 初始化操作
})

// 方法
const getTemplateIcon = (category) => {
  const iconMap = {
    academic: 'Document',
    lab: 'Experiment',
    technical: 'Tools',
    custom: 'User'
  }
  return iconMap[category] || 'Document'
}

const getTemplateIconColor = (category) => {
  const colorMap = {
    academic: '#0078d4',
    lab: '#107c10',
    technical: '#ff8c00',
    custom: '#8a8886'
  }
  return colorMap[category] || '#605e5c'
}

const getCategoryLabel = (category) => {
  const labelMap = {
    academic: '学术论文',
    lab: '实验报告',
    technical: '技术文档',
    custom: '自定义'
  }
  return labelMap[category] || '未知'
}

const getCategoryTagType = (category) => {
  const typeMap = {
    academic: 'primary',
    lab: 'success',
    technical: 'warning',
    custom: 'info'
  }
  return typeMap[category] || 'info'
}

const selectTemplate = (template) => {
  selectedTemplate.value = template
  detailDrawerVisible.value = true
}

const useTemplate = (template) => {
  ElMessage.success(`已选择模板: ${template.name}`)
  // 这里可以将模板信息传递给生成页面
  router.push({
    name: 'Generate',
    query: {
      templateId: template.id
    }
  })
}

const previewTemplate = (template) => {
  previewContent.value = generateTemplatePreview(template)
  renderedPreviewContent.value = renderTemplatePreview(previewContent.value)
  previewDialogVisible.value = true
}

const generateTemplatePreview = (template) => {
  // 生成模板预览内容
  return `# {{title}}

**作者**: {{author}}  
**日期**: {{date}}

## 摘要

{{abstract}}

## 1. 引言

{{introduction}}

## 2. 方法

{{methodology}}

## 3. 结果

{{results}}

## 4. 讨论

{{discussion}}

## 5. 结论

{{conclusion}}

## 参考文献

{{references}}`
}

const renderTemplatePreview = (content) => {
  // 简单的 Markdown 渲染
  return content
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\n/gim, '<br>')
}

const handleTemplateAction = ({ action, template }) => {
  switch (action) {
    case 'edit':
      editTemplate(template)
      break
    case 'duplicate':
      duplicateTemplate(template)
      break
    case 'delete':
      deleteTemplate(template)
      break
  }
}

const editTemplate = (template) => {
  ElMessage.info('编辑功能待实现')
}

const duplicateTemplate = (template) => {
  const newTemplate = {
    ...template,
    id: `${template.id}_copy_${Date.now()}`,
    name: `${template.name} (副本)`,
    isDefault: false,
    usageCount: 0,
    createdAt: new Date()
  }
  
  templates.value.push(newTemplate)
  ElMessage.success('模板复制成功')
}

const deleteTemplate = async (template) => {
  try {
    await ElMessageBox.confirm(`确定要删除模板 "${template.name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const index = templates.value.findIndex(t => t.id === template.id)
    if (index > -1) {
      templates.value.splice(index, 1)
      ElMessage.success('模板删除成功')
    }
  } catch {
    // 用户取消操作
  }
}

const handleFileChange = (file) => {
  uploadForm.value.file = file.raw
}

const uploadTemplate = async () => {
  if (!uploadForm.value.name || !uploadForm.value.file) {
    ElMessage.warning('请填写模板名称并选择文件')
    return
  }

  uploading.value = true
  
  try {
    // 模拟上传过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const newTemplate = {
      id: `custom_${Date.now()}`,
      name: uploadForm.value.name,
      description: uploadForm.value.description,
      category: uploadForm.value.category,
      format: getFileFormat(uploadForm.value.file.name),
      isDefault: false,
      usageCount: 0,
      createdAt: new Date()
    }
    
    templates.value.push(newTemplate)
    
    // 重置表单
    uploadForm.value = {
      name: '',
      description: '',
      category: 'custom',
      file: null
    }
    
    showUploadDialog.value = false
    ElMessage.success('模板上传成功')
    
  } catch (error) {
    ElMessage.error('模板上传失败: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const getFileFormat = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const formatMap = {
    'md': 'Markdown',
    'tex': 'LaTeX',
    'docx': 'Word'
  }
  return formatMap[ext] || 'Unknown'
}

const formatDate = (date) => {
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.templates-container {
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

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-md);
}

.toolbar-left {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.template-card {
  padding: var(--spacing-lg);
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.template-card:hover {
  transform: translateY(-2px);
}

.template-card.selected {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(0, 120, 212, 0.1);
}

.template-preview {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.template-badge {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
}

.template-info {
  flex: 1;
}

.template-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.template-description {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 var(--spacing-md) 0;
}

.template-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.usage-count {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.template-actions {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  display: flex;
  gap: var(--spacing-xs);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.template-card:hover .template-actions {
  opacity: 1;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xxl);
  color: var(--color-text-secondary);
}

.empty-state p {
  margin: var(--spacing-md) 0 var(--spacing-lg) 0;
}

.template-detail {
  padding: var(--spacing-md);
}

.detail-header {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.template-title h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.template-title p {
  color: var(--color-text-secondary);
  margin: 0;
}

.detail-section {
  margin-bottom: var(--spacing-lg);
}

.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md) 0;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--color-border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.variables-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.variable-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  background-color: var(--color-bg-tertiary);
  border-radius: var(--radius-medium);
}

.variable-item code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  color: var(--color-primary);
}

.variable-desc {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.detail-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.template-preview-content {
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.preview-toolbar {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border-light);
}

.preview-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

.source-view pre {
  background-color: var(--color-bg-tertiary);
  padding: var(--spacing-md);
  border-radius: var(--radius-medium);
  overflow-x: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

.rendered-view {
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .templates-container {
    padding: var(--spacing-lg);
  }
  
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .toolbar-left {
    flex-direction: column;
  }
  
  .templates-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-actions {
    flex-direction: column;
  }
}
</style>
