<template>
  <div class="home-container">
    <!-- 头部欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">欢迎使用 DocHelper</h1>
        <p class="welcome-subtitle">智能实验报告生成工具，让学术写作更简单高效</p>
      </div>
      <div class="welcome-actions">
        <el-button type="primary" size="large" @click="$router.push('/upload')">
          <el-icon><Upload /></el-icon>
          开始创建报告
        </el-button>
        <el-button size="large" @click="$router.push('/templates')">
          <el-icon><Files /></el-icon>
          浏览模板库
        </el-button>
      </div>
    </div>

    <!-- 功能卡片区域 -->
    <div class="features-section">
      <div class="section-title">
        <h2>主要功能</h2>
        <p>一站式实验报告生成解决方案</p>
      </div>
      
      <div class="features-grid">
        <div class="feature-card fluent-card" @click="$router.push('/upload')">
          <div class="feature-icon">
            <el-icon size="32" color="#0078d4"><Upload /></el-icon>
          </div>
          <h3>智能上传</h3>
          <p>支持多种文件格式，包括代码包、实验指导书、结果图片等</p>
          <div class="feature-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="feature-card fluent-card" @click="$router.push('/generate')">
          <div class="feature-icon">
            <el-icon size="32" color="#107c10"><EditPen /></el-icon>
          </div>
          <h3>AI 生成</h3>
          <p>基于大语言模型，自动分析实验内容并生成专业报告</p>
          <div class="feature-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="feature-card fluent-card" @click="$router.push('/templates')">
          <div class="feature-icon">
            <el-icon size="32" color="#ff8c00"><Files /></el-icon>
          </div>
          <h3>模板库</h3>
          <p>丰富的报告模板，支持自定义样式和格式标准化</p>
          <div class="feature-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="feature-card fluent-card">
          <div class="feature-icon">
            <el-icon size="32" color="#d13438"><DocumentCopy /></el-icon>
          </div>
          <h3>多格式导出</h3>
          <p>支持 PDF、Word、Markdown 等多种格式输出</p>
          <div class="feature-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近项目区域 -->
    <div class="recent-section">
      <div class="section-header">
        <h2>最近项目</h2>
        <el-button text @click="$router.push('/history')">
          查看全部
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      
      <div class="recent-projects" v-if="recentProjects.length > 0">
        <div 
          v-for="project in recentProjects" 
          :key="project.id"
          class="project-card fluent-card"
          @click="openProject(project)"
        >
          <div class="project-info">
            <h4>{{ project.name }}</h4>
            <p class="project-desc">{{ project.description }}</p>
            <div class="project-meta">
              <span class="project-date">{{ formatDate(project.updatedAt) }}</span>
              <el-tag :type="getStatusType(project.status)" size="small">
                {{ project.status }}
              </el-tag>
            </div>
          </div>
          <div class="project-actions">
            <el-button text size="small">
              <el-icon><Edit /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <el-icon size="48" color="#8a8886"><Document /></el-icon>
        <p>暂无最近项目</p>
        <el-button type="primary" @click="$router.push('/upload')">
          创建第一个项目
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 最近项目数据
const recentProjects = ref([])

// 模拟数据
const mockProjects = [
  {
    id: 1,
    name: '数据结构实验报告',
    description: '链表、栈、队列的实现与应用',
    status: '已完成',
    updatedAt: new Date('2024-01-15')
  },
  {
    id: 2,
    name: '机器学习实验',
    description: '线性回归模型的实现与分析',
    status: '进行中',
    updatedAt: new Date('2024-01-14')
  },
  {
    id: 3,
    name: '网络编程实验',
    description: 'TCP/UDP 通信协议实现',
    status: '草稿',
    updatedAt: new Date('2024-01-13')
  }
]

onMounted(() => {
  // 加载最近项目
  loadRecentProjects()
})

const loadRecentProjects = () => {
  // 这里应该从后端API获取数据
  recentProjects.value = mockProjects.slice(0, 3)
}

const openProject = (project) => {
  ElMessage.info(`打开项目: ${project.name}`)
  // 这里应该跳转到项目详情页面
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

const getStatusType = (status) => {
  const statusMap = {
    '已完成': 'success',
    '进行中': 'warning',
    '草稿': 'info'
  }
  return statusMap[status] || 'info'
}
</script>

<style scoped>
.home-container {
  padding: var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  padding: var(--spacing-xxl) 0;
  margin-bottom: var(--spacing-xl);
}

.welcome-title {
  font-size: 32px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md) 0;
}

.welcome-subtitle {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-xl) 0;
}

.welcome-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

.features-section {
  margin-bottom: var(--spacing-xxl);
}

.section-title {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.section-title h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.section-title p {
  color: var(--color-text-secondary);
  margin: 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}

.feature-card {
  padding: var(--spacing-xl);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-2px);
}

.feature-icon {
  margin-bottom: var(--spacing-md);
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.feature-card p {
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

.feature-arrow {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.feature-card:hover .feature-arrow {
  opacity: 1;
}

.recent-section {
  margin-bottom: var(--spacing-xl);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.section-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.recent-projects {
  display: grid;
  gap: var(--spacing-md);
}

.project-card {
  padding: var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.project-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.project-desc {
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-sm) 0;
  font-size: 14px;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.project-date {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xxl);
  color: var(--color-text-secondary);
}

.empty-state p {
  margin: var(--spacing-md) 0 var(--spacing-lg) 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-container {
    padding: var(--spacing-lg);
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .welcome-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
}
</style>
