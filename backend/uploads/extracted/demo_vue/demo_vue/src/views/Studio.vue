<template>
  <div class="studio-container">
    <header class="studio-header glass-morphism">
      <div class="header-left">
        <router-link to="/" class="logo-link">
          <img src="/logo.png" alt="先锋·智知" class="header-logo" />
          <span class="header-title text-gradient">先锋·智知</span>
        </router-link>
      </div>
      <div class="header-right">
        <el-button type="primary" class="ai-status">
          <el-icon><Cpu /></el-icon>
          模型状态：在线
        </el-button>
      </div>
    </header>
    
    <main class="studio-main">
      <aside class="studio-sidebar glass-morphism">
        <div class="sidebar-header">
          <h3>生成类型</h3>
        </div>
        <div class="sidebar-content">
          <el-menu
            :default-active="activeFeature"
            class="feature-menu"
            @select="handleFeatureSelect"
          >
            <el-menu-item index="video">
              <el-icon><VideoCamera /></el-icon>
              <span>视频生成</span>
            </el-menu-item>
            <el-menu-item index="audio">
              <el-icon><Headset /></el-icon>
              <span>音频生成</span>
            </el-menu-item>
            <el-menu-item index="image">
              <el-icon><Picture /></el-icon>
              <span>图片生成</span>
            </el-menu-item>
          </el-menu>
        </div>
      </aside>
      
      <section class="studio-content">
        <div class="params-panel glass-morphism">
          <div class="panel-header">
            <h2>参数配置</h2>
            <div class="panel-controls">
              <el-button type="primary" @click="handleGenerate">生成</el-button>
              <el-button @click="resetParams">重置</el-button>
            </div>
          </div>
          
          <div class="panel-body">
            <el-form :model="formData" label-position="top">
              <!-- 视频生成参数 -->
              <template v-if="activeFeature === 'video'">
                <ParamsVideo v-model="formData" />
              </template>
              
              <!-- 音频生成参数 -->
              <template v-else-if="activeFeature === 'audio'">
                <ParamsAudio v-model="formData" />
              </template>

              <!-- 图片生成参数 -->
              <template v-else-if="activeFeature === 'image'">
                <ParamsImage v-model="formData" />
              </template>
            </el-form>
          </div>
        </div>
        
        <div class="result-panel glass-morphism">
          <div class="panel-header">
            <h2>生成结果</h2>
            <div class="panel-controls">
              <el-button v-if="result" type="success" plain @click="downloadResult">
                <el-icon><Download /></el-icon>
                下载
              </el-button>
            </div>
          </div>
          
          <div class="panel-body result-container">
            <div v-if="!result" class="no-result">
              <el-empty description="请先设置参数并点击生成">
                <el-button type="primary" @click="handleGenerate">立即生成</el-button>
              </el-empty>
            </div>
            
            <div v-else-if="result && activeFeature === 'video'" class="video-result">
              <div class="media-preview neon-border">
                <video :src="result.mediaUrl" controls class="preview-video"></video>
              </div>
              <div class="result-info">
                <div class="info-item">
                  <span class="info-label">提示词：</span>
                  <span class="info-value">{{ formData.prompt }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">模型：</span>
                  <span class="info-value">{{ getModelName(formData.model) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">分辨率：</span>
                  <span class="info-value">{{ formData.resolution }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">生成时间：</span>
                  <span class="info-value">{{ result.generationTime }}</span>
                </div>
              </div>
            </div>
            
            <div v-else-if="result && activeFeature === 'audio'" class="audio-result">
              <div class="media-preview neon-border">
                <audio :src="result.mediaUrl" controls class="preview-audio"></audio>
                <div class="audio-waveform"></div>
              </div>
              <div class="result-info">
                <div class="info-item">
                  <span class="info-label">提示词：</span>
                  <span class="info-value">{{ formData.prompt }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">模型：</span>
                  <span class="info-value">{{ getModelName(formData.model) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">时长：</span>
                  <span class="info-value">{{ formData.duration }}秒</span>
                </div>
                <div class="info-item">
                  <span class="info-label">生成时间：</span>
                  <span class="info-value">{{ result.generationTime }}</span>
                </div>
              </div>
            </div>

            <div v-else-if="result && activeFeature === 'image'" class="image-result">
              <div class="media-preview neon-border">
                <img :src="result.mediaUrl" class="preview-image" />
              </div>
              <div class="result-info">
                <div class="info-item">
                  <span class="info-label">提示词：</span>
                  <span class="info-value">{{ formData.prompt }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">模型：</span>
                  <span class="info-value">{{ getModelName(formData.model) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">长宽比：</span>
                  <span class="info-value">{{ formData.aspect_ratio }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">生成时间：</span>
                  <span class="info-value">{{ result.generationTime }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { VideoCamera, Headset, Picture, Cpu, Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import ParamsVideo from '../components/ParamsVideo.vue'
import ParamsAudio from '../components/ParamsAudio.vue'
import ParamsImage from '../components/ParamsImage.vue'

// 激活的功能
const activeFeature = ref('video')

// 表单数据
const formData = reactive({
  // 通用参数
  prompt: '',
  negative_prompt: '',
  model: '',
  
  // 视频参数
  video_type: 'text-to-video',
  camera_motion: 'static',
  transition: 'none',
  motion_effect: 'normal',
  cfg_scale: 7.5,
  duration: 5,
  fps: '30',
  resolution: '1920×1080',
  color_grading: 'standard',
  background_music: 'none',
  seed: -1,
  
  // 音频参数
  audio_type: 'voice-clone',
  speech_speed: 1.0,
  pitch: 0,
  emotion: 'neutral',
  accent: 'mandarin',
  music_genre: 'none',
  ambient_sound: 'disabled',

  // 图片参数
  style: 'cinematic',
  aspect_ratio: '16:9',
  sampling_steps: 20
})

// 生成结果
const result = ref(null)

// 切换功能
const handleFeatureSelect = (key) => {
  activeFeature.value = key
  result.value = null
}

// 重置参数
const resetParams = () => {
  if (activeFeature.value === 'video') {
    formData.prompt = ''
    formData.negative_prompt = ''
    formData.model = 'stable-video-diffusion'
    formData.video_type = 'text-to-video'
    formData.camera_motion = 'static'
    formData.transition = 'none'
    formData.motion_effect = 'normal'
    formData.cfg_scale = 7.5
    formData.duration = 5
    formData.fps = '30'
    formData.resolution = '1920×1080'
    formData.color_grading = 'standard'
    formData.background_music = 'none'
    formData.seed = -1
  } else if (activeFeature.value === 'audio') {
    formData.prompt = ''
    formData.negative_prompt = ''
    formData.model = 'audioldm2'
    formData.audio_type = 'voice-clone'
    formData.cfg_scale = 7.0
    formData.duration = 5
    formData.speech_speed = 1.0
    formData.pitch = 0
    formData.emotion = 'neutral'
    formData.accent = 'mandarin'
    formData.music_genre = 'none'
    formData.ambient_sound = 'disabled'
    formData.seed = -1
  } else if (activeFeature.value === 'image') {
    formData.prompt = ''
    formData.negative_prompt = ''
    formData.model = 'sdxl'
    formData.style = 'cinematic'
    formData.aspect_ratio = '16:9'
    formData.sampling_steps = 20
    formData.cfg_scale = 7.0
    formData.seed = -1
  }
  
  ElMessage.success('参数已重置')
}

// 生成处理
const handleGenerate = () => {
  if (!formData.prompt) {
    ElMessage.warning('请填写提示词')
    return
  }
  
  // 模拟生成中
  ElMessage({
    message: '正在生成中，请稍候...',
    type: 'info',
    duration: 2000
  })
  
  // 模拟API调用延迟
  setTimeout(() => {
    const currentTime = new Date().toLocaleString()
    
    if (activeFeature.value === 'video') {
      result.value = {
        type: 'video',
        mediaUrl: '/data/videos/placeholder.mp4',
        generationTime: currentTime
      }
    } else if (activeFeature.value === 'audio') {
      result.value = {
        type: 'audio',
        mediaUrl: '/data/audios/placeholder.mp3',
        generationTime: currentTime
      }
    } else if (activeFeature.value === 'image') {
      result.value = {
        type: 'image',
        mediaUrl: '/data/images/placeholder.png',
        generationTime: currentTime
      }
    }
    
    ElMessage.success('生成完成！')
  }, 3000)
}

// 获取模型名称
const getModelName = (modelKey) => {
  const modelMap = {
    'runway-gen2': 'Runway Gen-2',
    'pika-labs': 'Pika Labs 风格',
    'stable-video-diffusion': 'Stable Video Diffusion',
    'modelscope': 'Modelscope',
    'audioldm2': 'AudioLDM 2',
    'audiogen': 'AudioGen',
    'musicgen': 'MusicGen',
    'xtts-tortoise': 'XTTS/TorToiSe',
    'sdxl': 'Stable Diffusion XL',
    'dalle3': 'DALL-E 3',
    'midjourney': 'Midjourney v6'
  }
  
  return modelMap[modelKey] || modelKey
}

// 下载结果
const downloadResult = () => {
  if (!result.value) return
  
  ElMessage({
    message: '开始下载...',
    type: 'success'
  })
  
  // 实际应用中这里应该触发真实下载
  // 这里只是模拟
  setTimeout(() => {
    ElMessage.success('下载完成！')
  }, 1500)
}

// 组件挂载后初始化
onMounted(() => {
  // 初始化默认参数
  resetParams()
})
</script>

<style scoped>
.studio-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.studio-header {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-lg);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
}

.header-left:hover {
  background: rgba(42, 42, 74, 0.3);
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
}

.header-logo {
  width: 40px;
  height: 40px;
  margin-right: var(--space-xs);
}

.header-title {
  font-size: 1.6rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-left: var(--space-xs);
}

.ai-status {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.studio-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.studio-sidebar {
  width: 200px;
  height: calc(100vh - 70px);
  overflow-y: auto;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar-header {
  padding: var(--space-md);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar-content {
  padding: var(--space-sm) 0;
}

.feature-menu {
  border: none;
  background: transparent;
}

.studio-content {
  flex: 1;
  display: flex;
  overflow: hidden;
  padding: var(--space-md);
  gap: var(--space-md);
}

.params-panel,
.result-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: var(--space-md);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.panel-header h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin: 0;
}

.panel-controls {
  display: flex;
  gap: var(--space-sm);
}

.panel-body {
  flex: 1;
  padding: var(--space-md);
  overflow-y: auto;
}

.result-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.no-result {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-result,
.audio-result,
.image-result {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.media-preview {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-lg);
}

.preview-video,
.preview-image {
  width: 100%;
  max-width: 640px;
  border-radius: var(--radius-md);
  background: #000;
}

.preview-audio {
  width: 100%;
  max-width: 500px;
  border-radius: var(--radius-md);
  background: rgba(26, 26, 58, 0.5);
}

.audio-waveform {
  width: 100%;
  max-width: 500px;
  height: 80px;
  margin-top: var(--space-md);
  background: linear-gradient(90deg, 
    var(--primary-color) 0%, 
    var(--secondary-color) 50%, 
    var(--primary-color) 100%);
  mask-image: url("data:image/svg+xml,%3Csvg width='500' height='80' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,40 Q125,0 250,40 T500,40' stroke='black' fill='none' stroke-width='2'/%3E%3C/svg%3E");
  mask-size: cover;
  mask-repeat: repeat-x;
  opacity: 0.7;
  border-radius: var(--radius-md);
}

.result-info {
  padding: var(--space-md);
  background: rgba(26, 26, 58, 0.3);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.info-item {
  display: flex;
  align-items: flex-start;
}

.info-label {
  min-width: 80px;
  font-weight: 500;
  color: var(--text-secondary);
}

.info-value {
  flex: 1;
  word-break: break-word;
}

@media (max-width: 1200px) {
  .studio-content {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .studio-sidebar {
    width: 60px;
  }
  
  .sidebar-header h3 {
    display: none;
  }
  
  .el-menu-item span {
    display: none;
  }
}
</style>
