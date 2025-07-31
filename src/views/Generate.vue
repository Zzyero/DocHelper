<template>
  <div class="generate-container">
    <div class="page-header">
      <h1>报告生成</h1>
      <p>基于上传的文件生成实验报告</p>
    </div>

    <!-- 项目信息 -->
    <el-card class="project-info-card" v-if="projectFiles.length > 0">
      <template #header>
        <div class="card-header">
          <el-icon size="20" color="#0078d4"><Files /></el-icon>
          <span>项目文件 ({{ projectFiles.length }})</span>
        </div>
      </template>
      
      <div class="files-summary">
        <div class="file-categories">
          <div class="category-item" v-for="(count, category) in fileCategorySummary" :key="category">
            <el-tag :type="getCategoryTagType(category)" size="small">
              {{ getCategoryLabel(category) }}: {{ count }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 生成配置 -->
    <el-card class="config-card">
      <template #header>
        <div class="card-header">
          <el-icon size="20" color="#107c10"><Setting /></el-icon>
          <span>生成配置</span>
        </div>
      </template>

      <el-form :model="generateConfig" label-width="120px" label-position="left">
        <el-form-item label="报告标题">
          <el-input
            v-model="generateConfig.title"
            placeholder="请输入报告标题"
            clearable
          />
        </el-form-item>

        <el-form-item label="输出格式">
          <el-radio-group v-model="generateConfig.format">
            <el-radio label="markdown">Markdown</el-radio>
            <el-radio label="latex">LaTeX</el-radio>
            <el-radio label="word">Word</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="选择模板">
          <el-select
            v-model="generateConfig.templateId"
            placeholder="选择报告模板"
            clearable
          >
            <el-option
              v-for="template in templates"
              :key="template.id"
              :label="template.name"
              :value="template.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="自定义提示">
          <el-input
            v-model="generateConfig.customPrompt"
            type="textarea"
            :rows="4"
            placeholder="可选：添加特殊要求或说明"
          />
        </el-form-item>

        <el-form-item label="包含内容">
          <el-checkbox-group v-model="generateConfig.includeOptions">
            <el-checkbox label="toc">目录</el-checkbox>
            <el-checkbox label="code">代码片段</el-checkbox>
            <el-checkbox label="images">图片</el-checkbox>
            <el-checkbox label="references">参考文献</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 生成按钮 -->
    <div class="action-section">
      <el-button
        type="primary"
        size="large"
        @click="startGeneration"
        :loading="isGenerating"
        :disabled="!canGenerate"
      >
        <el-icon><Magic /></el-icon>
        {{ isGenerating ? '生成中...' : '开始生成报告' }}
      </el-button>
    </div>

    <!-- 生成进度 -->
    <el-card class="progress-card" v-if="isGenerating || generationComplete">
      <template #header>
        <div class="card-header">
          <el-icon size="20" color="#ff8c00"><Loading /></el-icon>
          <span>生成进度</span>
        </div>
      </template>

      <div class="progress-content">
        <el-steps :active="currentStep" finish-status="success">
          <el-step title="分析文件" description="解析上传的文件内容" />
          <el-step title="AI 生成" description="调用大语言模型生成报告" />
          <el-step title="格式转换" description="转换为目标格式" />
          <el-step title="完成" description="报告生成完成" />
        </el-steps>

        <div class="progress-details" v-if="isGenerating">
          <el-progress
            :percentage="progressPercentage"
            :status="progressStatus"
            :stroke-width="8"
          />
          <p class="progress-text">{{ progressText }}</p>
        </div>

        <!-- 生成结果 -->
        <div class="generation-result" v-if="generationComplete">
          <el-result
            icon="success"
            title="报告生成成功"
            :sub-title="`已生成 ${generateConfig.format.toUpperCase()} 格式报告`"
          >
            <template #extra>
              <div class="result-actions">
                <el-button type="primary" @click="previewReport">
                  <el-icon><View /></el-icon>
                  预览报告
                </el-button>
                <el-button @click="downloadReport">
                  <el-icon><Download /></el-icon>
                  下载报告
                </el-button>
                <el-button @click="saveToHistory">
                  <el-icon><FolderAdd /></el-icon>
                  保存到历史
                </el-button>
              </div>
            </template>
          </el-result>
        </div>
      </div>
    </el-card>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="报告预览"
      width="90%"
      center
    >
      <div class="report-preview">
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
        
        <div class="preview-content">
          <div v-if="previewMode === 'source'" class="source-view">
            <pre><code>{{ generatedContent }}</code></pre>
          </div>
          <div v-else class="rendered-view" v-html="renderedContent"></div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

// 响应式数据
const projectFiles = ref([])
const isGenerating = ref(false)
const generationComplete = ref(false)
const currentStep = ref(0)
const progressPercentage = ref(0)
const progressStatus = ref('')
const progressText = ref('')
const previewVisible = ref(false)
const previewMode = ref('rendered')
const generatedContent = ref('')
const renderedContent = ref('')

const generateConfig = ref({
  title: '',
  format: 'markdown',
  templateId: '',
  customPrompt: '',
  includeOptions: ['toc', 'code', 'images']
})

const templates = ref([
  { id: 'default', name: '默认模板' },
  { id: 'academic', name: '学术论文模板' },
  { id: 'lab-report', name: '实验报告模板' },
  { id: 'technical', name: '技术文档模板' }
])

// 计算属性
const canGenerate = computed(() => {
  return projectFiles.value.length > 0 && generateConfig.value.title.trim() !== ''
})

const fileCategorySummary = computed(() => {
  const summary = {}
  projectFiles.value.forEach(file => {
    const category = file.category || 'others'
    summary[category] = (summary[category] || 0) + 1
  })
  return summary
})

// 生命周期
onMounted(() => {
  loadProjectFiles()
})

// 方法
const loadProjectFiles = () => {
  // 从路由参数获取文件信息
  if (route.query.files) {
    try {
      projectFiles.value = JSON.parse(route.query.files)
      
      // 根据文件生成默认标题
      if (projectFiles.value.length > 0) {
        generateConfig.value.title = `实验报告 - ${new Date().toLocaleDateString()}`
      }
    } catch (error) {
      console.error('解析文件信息失败:', error)
      ElMessage.error('加载项目文件失败')
    }
  }
  
  if (projectFiles.value.length === 0) {
    ElMessage.warning('未找到项目文件，请先上传文件')
    router.push('/upload')
  }
}

const getCategoryLabel = (category) => {
  const labels = {
    code: '代码文件',
    guide: '指导书',
    images: '图片',
    others: '其他'
  }
  return labels[category] || '未知'
}

const getCategoryTagType = (category) => {
  const types = {
    code: 'primary',
    guide: 'success',
    images: 'warning',
    others: 'info'
  }
  return types[category] || 'info'
}

const startGeneration = async () => {
  if (!canGenerate.value) {
    ElMessage.warning('请完善生成配置')
    return
  }

  isGenerating.value = true
  generationComplete.value = false
  currentStep.value = 0
  progressPercentage.value = 0

  try {
    // 步骤1: 分析文件
    progressText.value = '正在分析上传的文件...'
    await simulateStep(1, 25)

    // 步骤2: AI 生成
    currentStep.value = 1
    progressText.value = '正在调用 AI 生成报告内容...'
    await simulateStep(2, 70)

    // 步骤3: 格式转换
    currentStep.value = 2
    progressText.value = '正在转换为目标格式...'
    await simulateStep(3, 90)

    // 步骤4: 完成
    currentStep.value = 3
    progressText.value = '报告生成完成！'
    progressPercentage.value = 100
    progressStatus.value = 'success'

    // 模拟生成的内容
    generatedContent.value = generateMockContent()
    renderedContent.value = renderContent(generatedContent.value)

    setTimeout(() => {
      isGenerating.value = false
      generationComplete.value = true
      ElMessage.success('报告生成成功！')
    }, 1000)

  } catch (error) {
    console.error('生成报告失败:', error)
    isGenerating.value = false
    progressStatus.value = 'exception'
    ElMessage.error('生成报告失败: ' + error.message)
  }
}

const simulateStep = async (step, targetProgress) => {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      progressPercentage.value += 2
      if (progressPercentage.value >= targetProgress) {
        clearInterval(interval)
        resolve()
      }
    }, 100)
  })
}

const generateMockContent = () => {
  return `# ${generateConfig.value.title}

## 1. 实验目的

本实验旨在...

## 2. 实验环境

- 操作系统: Windows 11
- 开发工具: Visual Studio Code
- 编程语言: Python 3.9

## 3. 实验内容

### 3.1 代码实现

\`\`\`python
def main():
    print("Hello, DocHelper!")
\`\`\`

### 3.2 实验结果

实验成功完成，达到预期目标。

## 4. 总结

通过本次实验，我们学习了...

## 5. 参考文献

[1] 相关文献...
`
}

const renderContent = (content) => {
  // 简单的 Markdown 渲染（实际应用中应使用专业的 Markdown 解析器）
  return content
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/```(\w+)?\n([\s\S]*?)```/gim, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/\n/gim, '<br>')
}

const previewReport = () => {
  previewVisible.value = true
}

const downloadReport = () => {
  // 创建下载链接
  const blob = new Blob([generatedContent.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${generateConfig.value.title}.${generateConfig.value.format === 'markdown' ? 'md' : generateConfig.value.format}`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  ElMessage.success('报告下载成功')
}

const saveToHistory = () => {
  // 保存到历史记录
  ElMessage.success('已保存到历史记录')
  router.push('/history')
}
</script>

<style scoped>
.generate-container {
  padding: var(--spacing-xl);
  max-width: 1000px;
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

.project-info-card,
.config-card,
.progress-card {
  margin-bottom: var(--spacing-lg);
  border-radius: var(--radius-card);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 500;
}

.files-summary {
  padding: var(--spacing-md) 0;
}

.file-categories {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.action-section {
  text-align: center;
  margin: var(--spacing-xl) 0;
}

.progress-content {
  padding: var(--spacing-lg) 0;
}

.progress-details {
  margin: var(--spacing-lg) 0;
  text-align: center;
}

.progress-text {
  margin-top: var(--spacing-md);
  color: var(--color-text-secondary);
}

.generation-result {
  margin-top: var(--spacing-xl);
}

.result-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.report-preview {
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.preview-toolbar {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border-light);
}

.preview-content {
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

.rendered-view h1,
.rendered-view h2,
.rendered-view h3 {
  color: var(--color-text-primary);
  margin: var(--spacing-lg) 0 var(--spacing-md) 0;
}

.rendered-view code {
  background-color: var(--color-bg-tertiary);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.rendered-view pre {
  background-color: var(--color-bg-tertiary);
  padding: var(--spacing-md);
  border-radius: var(--radius-medium);
  overflow-x: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .generate-container {
    padding: var(--spacing-lg);
  }
  
  .result-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .file-categories {
    flex-direction: column;
  }
}
</style>
