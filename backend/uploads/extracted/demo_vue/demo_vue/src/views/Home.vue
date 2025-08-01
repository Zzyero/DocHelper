<template>
  <div class="home-container">
    <header class="hero">
      <div class="logo-container">
        <img src="/logo.png" alt="先锋·智知" class="logo" />
      </div>
      <h1 class="title text-gradient">先锋·智知</h1>
      <p class="subtitle">下一代 AI 生成式内容工作室</p>
      
      <div class="hero-buttons">
        <router-link to="/studio" class="btn-primary">
          <span class="btn-text">进入工作室</span>
          <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      
      <div class="floating-graphics">
        <div class="floating-cube cube1"></div>
        <div class="floating-cube cube2"></div>
        <div class="floating-circle circle1"></div>
        <div class="floating-circle circle2"></div>
      </div>
    </header>
    
    <section class="features glass-morphism">
      <h2 class="section-title">生成内容的无限可能</h2>
      
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon class="icon"><VideoCamera /></el-icon>
          </div>
          <h3>视频生成</h3>
          <p>从文本提示或图像生成高质量视频，支持多种风格和场景转换</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon class="icon"><Headset /></el-icon>
          </div>
          <h3>音频生成</h3>
          <p>生成语音、音乐和声音效果，支持多种声音风格和情感表达</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon class="icon"><Magnet /></el-icon>
          </div>
          <h3>精准控制</h3>
          <p>微调生成参数，精确控制创作过程中的每一个细节</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon class="icon"><Connection /></el-icon>
          </div>
          <h3>多模态集成</h3>
          <p>无缝连接不同生成模型，创造更加丰富的内容体验</p>
        </div>
      </div>
    </section>
    
    <footer class="home-footer">
      <p>© 2024 先锋·智知 AI 工作室</p>
    </footer>
  </div>
</template>

<script setup>
import { ArrowRight, VideoCamera, Headset, Magnet, Connection } from '@element-plus/icons-vue'
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  padding: var(--space-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: var(--space-xxl);
  overflow-y: auto;
}

.hero {
  width: 100%;
  max-width: 1200px;
  padding: var(--space-xxl) var(--space-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
}

.logo-container {
  margin-bottom: var(--space-xl);
  position: relative;
}

.logo {
  width: 180px;
  height: 180px;
  animation: pulse 4s infinite alternate;
}

@keyframes pulse {
  0% {
    filter: drop-shadow(0 0 8px rgba(94, 98, 209, 0.3));
  }
  100% {
    filter: drop-shadow(0 0 30px rgba(79, 195, 247, 0.6));
  }
}

.title {
  font-size: 5rem;
  font-weight: 700;
  margin-bottom: var(--space-md);
  letter-spacing: -0.03em;
}

.subtitle {
  font-size: 1.8rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-xl);
  max-width: 600px;
}

.hero-buttons {
  display: flex;
  gap: var(--space-lg);
  margin-top: var(--space-lg);
}

.btn-primary {
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: var(--space-md) var(--space-xl);
  border-radius: var(--radius-md);
  font-size: 1.2rem;
  font-weight: 500;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  transition: all var(--transition-normal);
  box-shadow: 0 4px 20px rgba(94, 98, 209, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(94, 98, 209, 0.6);
}

.btn-text {
  margin-right: var(--space-xs);
}

.floating-graphics {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
  overflow: hidden;
}

.floating-cube {
  position: absolute;
  background: linear-gradient(135deg, var(--primary-color), transparent);
  border-radius: var(--radius-sm);
  opacity: 0.15;
}

.floating-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--secondary-color), transparent);
  opacity: 0.15;
}

.cube1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 5%;
  animation: float 15s infinite alternate;
}

.cube2 {
  width: 150px;
  height: 150px;
  bottom: 15%;
  right: 10%;
  animation: float 20s infinite alternate-reverse;
}

.circle1 {
  width: 300px;
  height: 300px;
  bottom: 5%;
  left: 15%;
  animation: float 18s infinite alternate-reverse;
}

.circle2 {
  width: 250px;
  height: 250px;
  top: 15%;
  right: 5%;
  animation: float 22s infinite alternate;
}

@keyframes float {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }
  100% {
    transform: translate(30px, 30px) rotate(10deg);
  }
}

.features {
  width: 100%;
  max-width: 1200px;
  padding: var(--space-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: 2.4rem;
  margin-bottom: var(--space-xl);
  text-align: center;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-xl);
  width: 100%;
}

.feature-card {
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  background: rgba(26, 26, 58, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all var(--transition-normal);
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: rgba(var(--primary-color), 0.3);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.feature-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: var(--radius-circle);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-md);
}

.icon {
  font-size: 28px;
  color: white;
}

.feature-card h3 {
  font-size: 1.4rem;
  margin-bottom: var(--space-sm);
}

.feature-card p {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
}

.home-footer {
  width: 100%;
  text-align: center;
  color: var(--text-tertiary);
  padding: var(--space-lg);
}

@media (max-width: 768px) {
  .title {
    font-size: 3rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .home-container {
    padding: var(--space-md);
  }
}
</style> 