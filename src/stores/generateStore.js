import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGenerateStore = defineStore('generate', () => {
  // 项目文件列表
  const projectFiles = ref([])
  
  // 生成配置
  const generateConfig = ref({
    title: '',
    format: 'markdown',
    templateId: '',
    customPrompt: '',
    includeOptions: ['toc', 'code', 'images']
  })
  
  // 生成状态
  const isGenerating = ref(false)
  const generationComplete = ref(false)
  const currentStep = ref(0)
  const progressPercentage = ref(0)
  const progressStatus = ref('')
  const progressText = ref('')
  
  // 生成结果
  const generatedContent = ref('')
  const renderedContent = ref('')
  
  // 预览状态
  const previewVisible = ref(false)
  const previewMode = ref('rendered')
  
  // 模板列表
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
  
  // Actions
  function setProjectFiles(files) {
    projectFiles.value = files
  }
  
  function addProjectFile(file) {
    projectFiles.value.push(file)
  }
  
  function removeProjectFile(fileId) {
    const index = projectFiles.value.findIndex(f => f.id === fileId)
    if (index > -1) {
      projectFiles.value.splice(index, 1)
    }
  }
  
  function clearProjectFiles() {
    projectFiles.value = []
  }
  
  function setGenerateConfig(config) {
    generateConfig.value = { ...generateConfig.value, ...config }
  }
  
  function updateGenerateConfig(key, value) {
    generateConfig.value[key] = value
  }
  
  function setTemplateId(templateId) {
    generateConfig.value.templateId = templateId
  }
  
  function setGenerating(status) {
    isGenerating.value = status
  }
  
  function setGenerationComplete(status) {
    generationComplete.value = status
  }
  
  function setCurrentStep(step) {
    currentStep.value = step
  }
  
  function setProgress(percentage, status = '', text = '') {
    progressPercentage.value = percentage
    if (status) progressStatus.value = status
    if (text) progressText.value = text
  }
  
  function setGeneratedContent(content) {
    generatedContent.value = content
  }
  
  function setRenderedContent(content) {
    renderedContent.value = content
  }
  
  function setPreviewVisible(visible) {
    previewVisible.value = visible
  }
  
  function setPreviewMode(mode) {
    previewMode.value = mode
  }
  
  function resetGeneration() {
    isGenerating.value = false
    generationComplete.value = false
    currentStep.value = 0
    progressPercentage.value = 0
    progressStatus.value = ''
    progressText.value = ''
    generatedContent.value = ''
    renderedContent.value = ''
  }
  
  function resetAll() {
    projectFiles.value = []
    generateConfig.value = {
      title: '',
      format: 'markdown',
      templateId: '',
      customPrompt: '',
      includeOptions: ['toc', 'code', 'images']
    }
    resetGeneration()
    previewVisible.value = false
    previewMode.value = 'rendered'
  }
  
  // 保存到后端 (如果需要)
  async function saveToBackend() {
    try {
      // 这里可以保存生成配置到后端
      const response = await fetch('/api/v1/settings/user-settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          generate_config: generateConfig.value
        })
      })
      
      return response.ok
    } catch (error) {
      console.error('保存生成配置到后端失败:', error)
      return false
    }
  }
  
  // 从后端加载 (如果需要)
  async function loadFromBackend() {
    try {
      const response = await fetch('/api/v1/settings/user-settings')
      if (response.ok) {
        const data = await response.json()
        if (data.generate_config) {
          generateConfig.value = { ...generateConfig.value, ...data.generate_config }
          return true
        }
      }
      return false
    } catch (error) {
      console.error('从后端加载生成配置失败:', error)
      return false
    }
  }
  
  return {
    // State
    projectFiles,
    generateConfig,
    isGenerating,
    generationComplete,
    currentStep,
    progressPercentage,
    progressStatus,
    progressText,
    generatedContent,
    renderedContent,
    previewVisible,
    previewMode,
    templates,
    
    // Getters
    canGenerate,
    fileCategorySummary,
    
    // Actions
    setProjectFiles,
    addProjectFile,
    removeProjectFile,
    clearProjectFiles,
    setGenerateConfig,
    updateGenerateConfig,
    setTemplateId,
    setGenerating,
    setGenerationComplete,
    setCurrentStep,
    setProgress,
    setGeneratedContent,
    setRenderedContent,
    setPreviewVisible,
    setPreviewMode,
    resetGeneration,
    resetAll,
    saveToBackend,
    loadFromBackend
  }
})
