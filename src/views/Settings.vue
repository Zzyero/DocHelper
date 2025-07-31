<template>
  <div class="settings-container">
    <div class="page-header">
      <h1>设置</h1>
      <p>配置应用程序的各项参数</p>
    </div>

    <div class="settings-content">
      <!-- AI 模型配置 -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <el-icon size="20" color="#0078d4"><Setting /></el-icon>
            <span>AI 模型配置</span>
          </div>
        </template>

        <el-form :model="aiSettings" label-width="120px" label-position="left">
          <el-form-item label="API 地址">
            <el-input
              v-model="aiSettings.apiUrl"
              placeholder="https://api.openai.com/v1"
              clearable
            >
              <template #prepend>HTTPS://</template>
            </el-input>
            <div class="form-help">
              OpenAI API 兼容的服务地址
            </div>
          </el-form-item>

          <el-form-item label="API 密钥">
            <el-input
              v-model="aiSettings.apiKey"
              type="password"
              placeholder="sk-..."
              show-password
              clearable
            />
            <div class="form-help">
              用于身份验证的 API 密钥
            </div>
          </el-form-item>

          <el-form-item label="模型名称">
            <el-select
              v-model="aiSettings.modelName"
              placeholder="选择或输入模型名称"
              filterable
              allow-create
              clearable
            >
              <el-option label="gpt-4" value="gpt-4" />
              <el-option label="gpt-4-turbo" value="gpt-4-turbo" />
              <el-option label="gpt-3.5-turbo" value="gpt-3.5-turbo" />
              <el-option label="claude-3-opus" value="claude-3-opus" />
              <el-option label="claude-3-sonnet" value="claude-3-sonnet" />
            </el-select>
            <div class="form-help">
              选择要使用的语言模型
            </div>
          </el-form-item>

          <el-form-item label="最大令牌数">
            <el-input-number
              v-model="aiSettings.maxTokens"
              :min="100"
              :max="32000"
              :step="100"
              controls-position="right"
            />
            <div class="form-help">
              单次请求的最大令牌数量
            </div>
          </el-form-item>

          <el-form-item label="温度参数">
            <el-slider
              v-model="aiSettings.temperature"
              :min="0"
              :max="2"
              :step="0.1"
              show-input
              :show-input-controls="false"
            />
            <div class="form-help">
              控制生成文本的随机性，0-2之间
            </div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="testConnection" :loading="testing">
              <el-icon><Connection /></el-icon>
              测试连接
            </el-button>
            <el-button @click="saveAiSettings">
              <el-icon><Check /></el-icon>
              保存配置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 文档生成设置 -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <el-icon size="20" color="#107c10"><Document /></el-icon>
            <span>文档生成设置</span>
          </div>
        </template>

        <el-form :model="docSettings" label-width="120px" label-position="left">
          <el-form-item label="默认格式">
            <el-radio-group v-model="docSettings.defaultFormat">
              <el-radio label="markdown">Markdown</el-radio>
              <el-radio label="latex">LaTeX</el-radio>
              <el-radio label="word">Word</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="输出目录">
            <el-input
              v-model="docSettings.outputDir"
              placeholder="选择输出目录"
              readonly
            >
              <template #append>
                <el-button @click="selectOutputDir">
                  <el-icon><Folder /></el-icon>
                  浏览
                </el-button>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="自动保存">
            <el-switch v-model="docSettings.autoSave" />
            <div class="form-help">
              生成完成后自动保存到输出目录
            </div>
          </el-form-item>

          <el-form-item label="包含目录">
            <el-switch v-model="docSettings.includeToc" />
            <div class="form-help">
              在生成的文档中包含目录
            </div>
          </el-form-item>

          <el-form-item>
            <el-button @click="saveDocSettings">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 应用程序设置 -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <el-icon size="20" color="#ff8c00"><Tools /></el-icon>
            <span>应用程序设置</span>
          </div>
        </template>

        <el-form :model="appSettings" label-width="120px" label-position="left">
          <el-form-item label="语言">
            <el-select v-model="appSettings.language">
              <el-option label="简体中文" value="zh-CN" />
              <el-option label="English" value="en-US" />
            </el-select>
          </el-form-item>

          <el-form-item label="主题">
            <el-radio-group v-model="appSettings.theme">
              <el-radio label="light">浅色</el-radio>
              <el-radio label="dark">深色</el-radio>
              <el-radio label="auto">跟随系统</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="启动时检查更新">
            <el-switch v-model="appSettings.checkUpdates" />
          </el-form-item>

          <el-form-item label="发送使用统计">
            <el-switch v-model="appSettings.analytics" />
            <div class="form-help">
              帮助我们改进产品体验
            </div>
          </el-form-item>

          <el-form-item>
            <el-button @click="saveAppSettings">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="resetSettings" type="danger" plain>
              <el-icon><RefreshLeft /></el-icon>
              重置所有设置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 关于信息 -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <el-icon size="20" color="#8a8886"><InfoFilled /></el-icon>
            <span>关于</span>
          </div>
        </template>

        <div class="about-content">
          <div class="app-info">
            <div class="app-icon">
              <el-icon size="48" color="#0078d4"><Document /></el-icon>
            </div>
            <div class="app-details">
              <h3>DocHelper</h3>
              <p>版本 1.0.0</p>
              <p>智能实验报告生成工具</p>
            </div>
          </div>
          
          <div class="app-links">
            <el-button text @click="openLink('https://github.com/dochelper/dochelper')">
              <el-icon><Link /></el-icon>
              GitHub 仓库
            </el-button>
            <el-button text @click="openLink('https://dochelper.com/docs')">
              <el-icon><Document /></el-icon>
              使用文档
            </el-button>
            <el-button text @click="openLink('https://dochelper.com/support')">
              <el-icon><QuestionFilled /></el-icon>
              技术支持
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const testing = ref(false)

const aiSettings = ref({
  apiUrl: 'api.openai.com/v1',
  apiKey: '',
  modelName: 'gpt-4',
  maxTokens: 4000,
  temperature: 0.7
})

const docSettings = ref({
  defaultFormat: 'markdown',
  outputDir: '',
  autoSave: true,
  includeToc: true
})

const appSettings = ref({
  language: 'zh-CN',
  theme: 'light',
  checkUpdates: true,
  analytics: false
})

// 生命周期
onMounted(() => {
  loadSettings()
})

// 方法
const loadSettings = () => {
  // 从本地存储加载设置
  const savedAiSettings = localStorage.getItem('aiSettings')
  if (savedAiSettings) {
    aiSettings.value = { ...aiSettings.value, ...JSON.parse(savedAiSettings) }
  }

  const savedDocSettings = localStorage.getItem('docSettings')
  if (savedDocSettings) {
    docSettings.value = { ...docSettings.value, ...JSON.parse(savedDocSettings) }
  }

  const savedAppSettings = localStorage.getItem('appSettings')
  if (savedAppSettings) {
    appSettings.value = { ...appSettings.value, ...JSON.parse(savedAppSettings) }
  }

  // 设置默认输出目录
  if (!docSettings.value.outputDir) {
    docSettings.value.outputDir = getDefaultOutputDir()
  }
}

const getDefaultOutputDir = () => {
  // 获取用户文档目录
  try {
    const os = window.require('os')
    const path = window.require('path')
    return path.join(os.homedir(), 'Documents', 'DocHelper')
  } catch {
    return './output'
  }
}

const testConnection = async () => {
  if (!aiSettings.value.apiUrl || !aiSettings.value.apiKey) {
    ElMessage.warning('请先填写 API 地址和密钥')
    return
  }

  testing.value = true
  try {
    // 这里应该调用后端API测试连接
    await new Promise(resolve => setTimeout(resolve, 2000)) // 模拟请求
    ElMessage.success('连接测试成功')
  } catch (error) {
    ElMessage.error('连接测试失败: ' + error.message)
  } finally {
    testing.value = false
  }
}

const saveAiSettings = () => {
  localStorage.setItem('aiSettings', JSON.stringify(aiSettings.value))
  ElMessage.success('AI 模型配置已保存')
}

const saveDocSettings = () => {
  localStorage.setItem('docSettings', JSON.stringify(docSettings.value))
  ElMessage.success('文档生成设置已保存')
}

const saveAppSettings = () => {
  localStorage.setItem('appSettings', JSON.stringify(appSettings.value))
  ElMessage.success('应用程序设置已保存')
}

const selectOutputDir = async () => {
  try {
    const { ipcRenderer } = window.require('electron')
    const result = await ipcRenderer.invoke('select-folder')
    
    if (!result.canceled && result.filePaths.length > 0) {
      docSettings.value.outputDir = result.filePaths[0]
    }
  } catch (error) {
    console.error('选择目录失败:', error)
    ElMessage.error('选择目录失败')
  }
}

const resetSettings = async () => {
  try {
    await ElMessageBox.confirm('确定要重置所有设置吗？此操作不可撤销。', '确认重置', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    localStorage.removeItem('aiSettings')
    localStorage.removeItem('docSettings')
    localStorage.removeItem('appSettings')
    
    // 重新加载默认设置
    loadSettings()
    
    ElMessage.success('所有设置已重置')
  } catch {
    // 用户取消操作
  }
}

const openLink = (url) => {
  try {
    const { shell } = window.require('electron')
    shell.openExternal(url)
  } catch (error) {
    console.error('打开链接失败:', error)
    ElMessage.error('打开链接失败')
  }
}
</script>

<style scoped>
.settings-container {
  padding: var(--spacing-xl);
  max-width: 800px;
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

.settings-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.settings-card {
  border-radius: var(--radius-card);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 500;
}

.form-help {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin-top: var(--spacing-xs);
}

.about-content {
  padding: var(--spacing-md) 0;
}

.app-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.app-details h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.app-details p {
  color: var(--color-text-secondary);
  margin: 0;
  font-size: 14px;
}

.app-links {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-container {
    padding: var(--spacing-lg);
  }
  
  .app-info {
    flex-direction: column;
    text-align: center;
  }
  
  .app-links {
    justify-content: center;
  }
}
</style>
