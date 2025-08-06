<template>
  <div id="app">
    <el-container class="app-container">
      <!-- 侧边栏 -->
      <el-aside width="240px" class="sidebar">
        <div class="logo-section">
          <div class="logo">
            <el-icon size="24" color="#0078d4">
              <Document />
            </el-icon>
            <span class="logo-text">DocHelper</span>
          </div>
        </div>
        
        <el-menu
          :default-active="$route.path"
          router
          class="sidebar-menu"
        >
          <el-menu-item index="/home">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-menu-item index="/upload">
            <el-icon><Upload /></el-icon>
            <span>文件上传</span>
          </el-menu-item>
          
          <el-menu-item index="/generate">
            <el-icon><EditPen /></el-icon>
            <span>报告生成</span>
          </el-menu-item>
          
          <el-menu-item index="/templates">
            <el-icon><Files /></el-icon>
            <span>模板库</span>
          </el-menu-item>
          
          <el-menu-item index="/history">
            <el-icon><Clock /></el-icon>
            <span>历史记录</span>
          </el-menu-item>
          
          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <span>设置</span>
          </el-menu-item>
          
          <el-menu-item index="/ai-chat">
            <el-icon><ChatDotRound /></el-icon>
            <span>AI对话</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // 默认跳转到首页
  if (router.currentRoute.value.path === '/') {
    router.push('/home')
  }
})
</script>

<style scoped>
.app-container {
  height: 100vh;
  background-color: var(--color-bg-secondary);
}

.sidebar {
  background-color: var(--color-bg-primary);
  border-right: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
}

.logo-section {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.sidebar-menu {
  flex: 1;
  padding: var(--spacing-md) 0;
  border-right: none;
}

.main-content {
  padding: 0;
  background-color: var(--color-bg-secondary);
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 200px !important;
  }
  
  .logo-text {
    font-size: 16px;
  }
}
</style>
