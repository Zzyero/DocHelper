import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUploadStore = defineStore('upload', () => {
  // 上传的文件列表
  const uploadedFiles = ref([])
  
  // 解压后的文件列表
  const extractedFiles = ref([])
  
  // 当前步骤 (1: 上传, 2: 解压完成)
  const currentStep = ref(1)
  
  // 解压状态
  const isExtracting = ref(false)
  
  // 活动标签页
  const activeTab = ref('archive')
  
  // 计算属性
  const hasFiles = computed(() => uploadedFiles.value.length > 0)
  
  const fileCategorySummary = computed(() => {
    const summary = {}
    extractedFiles.value.forEach(file => {
      const category = file.category || 'others'
      summary[category] = (summary[category] || 0) + 1
    })
    return summary
  })
  
  // Actions
  function setUploadedFiles(files) {
    uploadedFiles.value = files
  }
  
  function addUploadedFile(file) {
    uploadedFiles.value.push(file)
  }
  
  function removeUploadedFile(fileId) {
    const index = uploadedFiles.value.findIndex(f => f.id === fileId)
    if (index > -1) {
      uploadedFiles.value.splice(index, 1)
    }
  }
  
  function clearUploadedFiles() {
    uploadedFiles.value = []
  }
  
  function setExtractedFiles(files) {
    extractedFiles.value = files
  }
  
  function addExtractedFile(file) {
    extractedFiles.value.push(file)
  }
  
  function clearExtractedFiles() {
    extractedFiles.value = []
  }
  
  function setCurrentStep(step) {
    currentStep.value = step
  }
  
  function setIsExtracting(extracting) {
    isExtracting.value = extracting
  }
  
  function setActiveTab(tab) {
    activeTab.value = tab
  }
  
  function resetAll() {
    uploadedFiles.value = []
    extractedFiles.value = []
    currentStep.value = 1
    isExtracting.value = false
    activeTab.value = 'archive'
  }
  
  // 保存到后端
  async function saveToBackend() {
    try {
      const filesToSave = uploadedFiles.value.map(file => ({
        id: file.id,
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
        url: file.url,
        path: file.path,
        category: file.category
      }))
      
      const response = await fetch('/api/v1/settings/user-settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          uploaded_files: filesToSave
        })
      })
      
      if (!response.ok) {
        console.warn('保存上传文件信息到后端失败')
        return false
      }
      
      return true
    } catch (error) {
      console.error('保存上传文件信息到后端失败:', error)
      return false
    }
  }
  
  // 从后端加载
  async function loadFromBackend() {
    try {
      const response = await fetch('/api/v1/settings/user-settings')
      if (response.ok) {
        const data = await response.json()
        if (data.uploaded_files && data.uploaded_files.length > 0) {
          uploadedFiles.value = data.uploaded_files.map(file => ({
            ...file,
            originalFile: null // 原始文件对象无法序列化，需要重新选择
          }))
          return true
        }
      }
      return false
    } catch (error) {
      console.error('从后端加载上传文件信息失败:', error)
      return false
    }
  }
  
  return {
    // State
    uploadedFiles,
    extractedFiles,
    currentStep,
    isExtracting,
    activeTab,
    
    // Getters
    hasFiles,
    fileCategorySummary,
    
    // Actions
    setUploadedFiles,
    addUploadedFile,
    removeUploadedFile,
    clearUploadedFiles,
    setExtractedFiles,
    addExtractedFile,
    clearExtractedFiles,
    setCurrentStep,
    setIsExtracting,
    setActiveTab,
    resetAll,
    saveToBackend,
    loadFromBackend
  }
})
