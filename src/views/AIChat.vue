<template>
  <div class="ai-chat-container">
    <div class="chat-header">
      <div class="header-content">
        <h2>AI 对话助手</h2>
        <p>与AI助手进行智能对话</p>
      </div>
      <div class="header-actions">
        <el-dropdown @command="handleHistoryCommand">
          <el-button size="small" type="primary" plain>
            <el-icon><Clock /></el-icon>
            历史记录
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item 
                v-for="session in chatHistory" 
                :key="session.id"
                :command="session.id"
              >
                {{ session.title || '对话记录' }} - {{ formatTime(session.timestamp) }}
              </el-dropdown-item>
              <el-dropdown-item v-if="chatHistory.length === 0" disabled>
                暂无历史记录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button size="small" @click="saveCurrentSession">
          <el-icon><Save /></el-icon>
          保存对话
        </el-button>
        <el-button size="small" @click="exportChat">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
      </div>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="message in messages" 
        :key="message.id"
        :class="['message', message.role]"
      >
        <div class="message-content">
          <div class="avatar">
            <el-icon v-if="message.role === 'user'"><User /></el-icon>
            <el-icon v-else><Avatar /></el-icon>
          </div>
          <div class="text">
            <div class="username">
              {{ message.role === 'user' ? '我' : 'AI助手' }}
              <span class="timestamp">{{ formatMessageTime(message.timestamp) }}</span>
            </div>
            <div class="content" v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>
      
      <div v-if="isLoading" class="message ai">
        <div class="message-content">
          <div class="avatar">
            <el-icon><Avatar /></el-icon>
          </div>
          <div class="text">
            <div class="username">AI助手</div>
            <div class="content">
              <el-skeleton :rows="2" animated />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <el-input
        v-model="inputMessage"
        type="textarea"
        :rows="3"
        placeholder="请输入您的问题...按 Ctrl+Enter 换行，Enter 发送"
        :disabled="isLoading"
        @keydown.ctrl.enter.exact.prevent="addLineBreak"
        @keydown.enter.exact.prevent="sendMessage"
      />
      <div class="input-actions">
        <div class="input-hints">
          <el-tag size="small" type="info">Ctrl+Enter 换行</el-tag>
        </div>
        <div class="action-buttons">
          <el-button @click="clearChat">清空对话</el-button>
          <el-button 
            type="primary" 
            @click="sendMessage"
            :disabled="!inputMessage.trim() || isLoading"
            :loading="isLoading"
          >
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Avatar, Clock, Download } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'

// 使用字符串表示Save图标
const Save = 'save'

// 初始化markdown解析器
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)
const chatHistory = ref([])

// 格式化消息内容（支持Markdown）
const formatMessage = (content) => {
  try {
    // 使用markdown-it解析markdown内容
    return md.render(content)
  } catch (error) {
    console.error('Markdown解析失败:', error)
    // 如果解析失败，回退到简单的换行处理
    return content.replace(/\n/g, '<br>')
  }
}

// 添加换行
const addLineBreak = () => {
  inputMessage.value += '\n'
}

// 发送消息
const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if (!message || isLoading.value) return

  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: message,
    timestamp: new Date()
  }
  messages.value.push(userMessage)
  
  // 保存到本地存储
  saveToLocalStorage()
  
  // 清空输入框
  inputMessage.value = ''
  
  // 滚动到底部
  scrollToBottom()
  
  try {
    isLoading.value = true
    
    // 调用后端API
    const response = await fetch('/api/v1/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        history: messages.value.slice(-10) // 只发送最近10条消息作为上下文
      })
    })
    
    if (!response.ok) {
      throw new Error('网络请求失败')
    }
    
    const data = await response.json()
    
    // 添加AI回复
    const aiMessage = {
      id: Date.now() + 1,
      role: 'ai',
      content: data.reply || '抱歉，我没有理解您的问题。',
      timestamp: new Date()
    }
    messages.value.push(aiMessage)
    
    // 保存到本地存储
    saveToLocalStorage()
    
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送消息失败：' + error.message)
    
    // 添加错误消息
    const errorMessage = {
      id: Date.now() + 1,
      role: 'ai',
      content: '抱歉，我遇到了一些问题，请稍后重试。',
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

// 清空对话
const clearChat = () => {
  ElMessageBox.confirm('确定要清空当前对话吗？', '确认清空', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    messages.value = []
    saveToLocalStorage()
    ElMessage.success('对话已清空')
  }).catch(() => {
    // 用户取消
  })
}

// 保存到本地存储
const saveToLocalStorage = () => {
  try {
    const chatData = {
      messages: messages.value,
      lastUpdated: new Date().toISOString()
    }
    localStorage.setItem('ai-chat-current', JSON.stringify(chatData))
  } catch (error) {
    console.error('保存聊天记录失败:', error)
  }
}

// 从本地存储加载
const loadFromLocalStorage = () => {
  try {
    const savedData = localStorage.getItem('ai-chat-current')
    if (savedData) {
      const chatData = JSON.parse(savedData)
      messages.value = chatData.messages || []
    }
  } catch (error) {
    console.error('加载聊天记录失败:', error)
  }
}

// 保存当前会话
const saveCurrentSession = async () => {
  if (messages.value.length === 0) {
    ElMessage.warning('当前没有对话内容可保存')
    return
  }
  
  try {
    const title = await ElMessageBox.prompt('请输入对话标题', '保存对话', {
      confirmButtonText: '保存',
      cancelButtonText: '取消',
      inputValue: `对话记录 ${new Date().toLocaleDateString()}`
    }).then(({ value }) => value).catch(() => null)
    
    if (title) {
      const session = {
        id: Date.now(),
        title: title,
        messages: messages.value,
        timestamp: new Date().toISOString()
      }
      
      // 保存到历史记录
      let history = JSON.parse(localStorage.getItem('ai-chat-history') || '[]')
      history.unshift(session)
      // 限制历史记录数量
      if (history.length > 50) {
        history = history.slice(0, 50)
      }
      localStorage.setItem('ai-chat-history', JSON.stringify(history))
      
      ElMessage.success('对话已保存')
      loadChatHistory()
    }
  } catch (error) {
    // 用户取消
  }
}

// 加载聊天历史
const loadChatHistory = () => {
  try {
    const history = JSON.parse(localStorage.getItem('ai-chat-history') || '[]')
    chatHistory.value = history
  } catch (error) {
    console.error('加载历史记录失败:', error)
    chatHistory.value = []
  }
}

// 处理历史记录命令
const handleHistoryCommand = (command) => {
  try {
    const history = JSON.parse(localStorage.getItem('ai-chat-history') || '[]')
    const session = history.find(s => s.id === command)
    if (session) {
      messages.value = session.messages
      saveToLocalStorage()
      scrollToBottom()
      ElMessage.success('已加载历史对话')
    }
  } catch (error) {
    console.error('加载历史对话失败:', error)
    ElMessage.error('加载历史对话失败')
  }
}

// 导出聊天记录
const exportChat = () => {
  if (messages.value.length === 0) {
    ElMessage.warning('当前没有对话内容可导出')
    return
  }
  
  try {
    let content = '# AI 对话记录\n\n'
    content += `导出时间: ${new Date().toLocaleString()}\n\n`
    
    messages.value.forEach(msg => {
      const role = msg.role === 'user' ? '用户' : 'AI助手'
      const time = msg.timestamp ? new Date(msg.timestamp).toLocaleString() : ''
      content += `## ${role} (${time})\n`
      content += `${msg.content}\n\n`
    })
    
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `AI对话记录_${new Date().toLocaleDateString()}.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    ElMessage.success('对话记录已导出')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleDateString()
}

const formatMessageTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString()
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 组件挂载时
onMounted(() => {
  loadFromLocalStorage()
  loadChatHistory()
  
  // 如果没有消息，添加欢迎消息
  if (messages.value.length === 0) {
    messages.value.push({
      id: 1,
      role: 'ai',
      content: '您好！我是AI助手，有什么我可以帮助您的吗？',
      timestamp: new Date()
    })
  }
  scrollToBottom()
})

// 组件卸载前
onUnmounted(() => {
  saveToLocalStorage()
})
</script>

<style scoped>
.ai-chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--color-bg-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.chat-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
  background-color: var(--color-bg-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.header-content h2 {
  margin: 0 0 var(--spacing-xs);
  color: var(--color-text-primary);
  font-size: 22px;
  font-weight: 600;
}

.header-content p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
  background-color: var(--color-bg-secondary);
  background-image: radial-gradient(circle, var(--color-border-light) 1px, transparent 1px);
  background-size: 20px 20px;
}

.message {
  margin-bottom: var(--spacing-md);
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-content {
  display: flex;
  gap: var(--spacing-sm);
  max-width: 90%;
}

@media (max-width: 768px) {
  .message-content {
    max-width: 95%;
  }
}

.message.user .message-content {
  margin-left: auto;
}

.avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message.ai .avatar {
  background: linear-gradient(135deg, var(--color-success), #2d9596);
}

.text {
  flex: 1;
  max-width: calc(100% - 46px);
}

.username {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.timestamp {
  font-size: 11px;
  color: var(--color-text-tertiary);
}

.content {
  padding: var(--spacing-md);
  border-radius: 12px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
  font-size: 14px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message.user .content {
  background: linear-gradient(135deg, var(--color-primary-light), #e3f2fd);
  color: var(--color-text-primary);
  border-bottom-right-radius: 4px;
}

.message.ai .content {
  background: white;
  border-bottom-left-radius: 4px;
}

.chat-input {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--color-border-light);
  background-color: var(--color-bg-primary);
}

.input-actions {
  margin-top: var(--spacing-sm);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.input-hints {
  display: flex;
  gap: var(--spacing-xs);
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: var(--color-bg-secondary);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--color-border-light);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .input-actions {
    flex-direction: column;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: center;
  }
}
</style>
