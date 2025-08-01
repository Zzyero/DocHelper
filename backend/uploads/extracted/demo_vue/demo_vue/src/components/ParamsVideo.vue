<template>
  <div class="params-video">
    <el-form-item label="提示词" required>
      <el-input
        v-model="modelValue.prompt"
        type="textarea"
        :rows="4"
        placeholder="请输入视频描述"
        resize="none"
      />
    </el-form-item>
    
    <el-form-item label="负面提示词">
      <el-input
        v-model="modelValue.negative_prompt"
        type="textarea"
        :rows="2"
        placeholder="请输入要避免的元素"
        resize="none"
      />
    </el-form-item>
    
    <div class="form-divider">基础设置</div>
    
    <el-form-item label="模型选择">
      <el-select v-model="modelValue.model" class="w-full">
        <el-option 
          v-for="option in modelOptions" 
          :key="option.value" 
          :label="option.label" 
          :value="option.value"
        />
      </el-select>
    </el-form-item>
    
    <el-form-item label="视频类型">
      <el-select v-model="modelValue.video_type" class="w-full">
        <el-option 
          v-for="option in videoTypeOptions" 
          :key="option.value" 
          :label="option.label" 
          :value="option.value"
        />
      </el-select>
    </el-form-item>
    
    <template v-if="modelValue.video_type === 'image-to-video'">
      <el-form-item label="参考图片">
        <el-upload
          class="reference-image-uploader"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleReferenceImageChange"
        >
          <img v-if="referenceImageUrl" :src="referenceImageUrl" class="reference-image" />
          <div v-else class="upload-placeholder">
            <el-icon><Plus /></el-icon>
            <div class="placeholder-text">点击上传图片</div>
          </div>
        </el-upload>
      </el-form-item>
    </template>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="时长(秒)">
          <el-input-number 
            v-model="modelValue.duration" 
            :min="1" 
            :max="60" 
            :step="1"
            class="w-full"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="提示词服从度">
          <el-slider 
            v-model="modelValue.cfg_scale" 
            :min="0" 
            :max="20" 
            :step="0.1" 
            show-input
            class="custom-slider"
          />
        </el-form-item>
      </el-col>
    </el-row>
    
    <div class="form-divider">高级设置</div>
    
    <el-form-item label="分辨率">
      <el-select v-model="modelValue.resolution" class="w-full">
        <el-option 
          v-for="option in resolutionOptions" 
          :key="option.value" 
          :label="option.label" 
          :value="option.value"
        />
      </el-select>
    </el-form-item>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="帧率(FPS)">
          <el-select v-model="modelValue.fps" class="w-full">
            <el-option 
              v-for="option in fpsOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="镜头风格">
          <el-select v-model="modelValue.camera_motion" class="w-full">
            <el-option 
              v-for="option in cameraMotionOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="场景过渡">
          <el-select v-model="modelValue.transition" class="w-full">
            <el-option 
              v-for="option in transitionOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="动态效果">
          <el-select v-model="modelValue.motion_effect" class="w-full">
            <el-option 
              v-for="option in motionEffectOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="色彩分级">
          <el-select v-model="modelValue.color_grading" class="w-full">
            <el-option 
              v-for="option in colorGradingOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="背景音乐">
          <el-select v-model="modelValue.background_music" class="w-full">
            <el-option 
              v-for="option in backgroundMusicOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    
    <el-form-item label="种子值">
      <el-input-number 
        v-model="modelValue.seed" 
        :min="-1" 
        :max="2147483647" 
        :step="1"
        placeholder="-1为随机"
        class="w-full"
      />
    </el-form-item>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

// 参考图片
const referenceImageUrl = ref(null)

// 处理参考图片变化
const handleReferenceImageChange = (file) => {
  if (file) {
    referenceImageUrl.value = URL.createObjectURL(file.raw)
  }
}

// 选项数据
const modelOptions = [
  { label: 'Runway Gen-2', value: 'runway-gen2' },
  { label: 'Pika Labs 风格', value: 'pika-labs' },
  { label: 'Stable Video Diffusion', value: 'stable-video-diffusion' },
  { label: 'Modelscope', value: 'modelscope' },
]

const videoTypeOptions = [
  { label: '从文本生成视频', value: 'text-to-video' },
  { label: '从图像生成视频', value: 'image-to-video' },
  { label: '视频延伸/扩展', value: 'video-extension' },
]

const resolutionOptions = [
  { label: '720p (1280×720)', value: '1280×720' },
  { label: '1080p (1920×1080)', value: '1920×1080' },
  { label: '1440p (2560×1440)', value: '2560×1440' },
  { label: '2K (2048×1080)', value: '2048×1080' },
  { label: '4K (3840×2160)', value: '3840×2160' },
  { label: '垂直视频 (720×1280)', value: '720×1280' },
  { label: '垂直视频 (1080×1920)', value: '1080×1920' },
  { label: '方形视频 (1080×1080)', value: '1080×1080' },
]

const fpsOptions = [
  { label: '24 FPS (电影风格)', value: '24' },
  { label: '30 FPS (标准视频)', value: '30' },
  { label: '60 FPS (高帧率)', value: '60' },
]

const cameraMotionOptions = [
  { label: '固定镜头', value: 'static' },
  { label: '平滑推进', value: 'zoom-in' },
  { label: '平滑拉远', value: 'zoom-out' },
  { label: '缓慢旋转', value: 'slow-rotation' },
  { label: '跟踪镜头', value: 'tracking' },
  { label: '航拍视角', value: 'aerial' },
]

const transitionOptions = [
  { label: '无过渡', value: 'none' },
  { label: '淡入淡出', value: 'fade' },
  { label: '溶解', value: 'dissolve' },
  { label: '滑动', value: 'slide' },
  { label: '缩放过渡', value: 'zoom' },
]

const motionEffectOptions = [
  { label: '正常速度', value: 'normal' },
  { label: '慢动作', value: 'slow-motion' },
  { label: '快动作', value: 'fast-motion' },
  { label: '运动模糊', value: 'motion-blur' },
  { label: '景深效果', value: 'depth-of-field' },
]

const colorGradingOptions = [
  { label: '标准 (无分级)', value: 'standard' },
  { label: '电影色调', value: 'cinematic' },
  { label: '温暖调', value: 'warm' },
  { label: '冷色调', value: 'cool' },
  { label: '复古风格', value: 'vintage' },
  { label: '黑白', value: 'black-white' },
]

const backgroundMusicOptions = [
  { label: '无背景音乐', value: 'none' },
  { label: '轻松氛围', value: 'relaxed' },
  { label: '动感节奏', value: 'energetic' },
  { label: '情感抒情', value: 'emotional' },
  { label: '史诗大气', value: 'epic' },
  { label: '自然环境音', value: 'nature' },
]
</script>

<style scoped>
.params-video {
  width: 100%;
}

.form-divider {
  font-size: 0.9rem;
  font-weight: 500;
  margin: var(--space-lg) 0 var(--space-md);
  padding-bottom: var(--space-xs);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
}

.w-full {
  width: 100%;
}

.reference-image-uploader {
  width: 100%;
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.reference-image {
  width: 100%;
  height: 150px;
  object-fit: contain;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl) 0;
  color: var(--text-tertiary);
}

.placeholder-text {
  margin-top: var(--space-sm);
  font-size: 0.9rem;
}

/* 自定义滑块样式 */
.custom-slider :deep(.el-tooltip__popper) {
  background-color: var(--bg-dark) !important;
  border: 1px solid var(--primary-color) !important;
  color: var(--text-primary) !important;
  box-shadow: 0 0 8px rgba(94, 98, 209, 0.4) !important;
  font-weight: 500;
}

.custom-slider :deep(.el-slider__button) {
  border: 2px solid var(--primary-color) !important;
  background-color: var(--primary-color) !important;
}

.custom-slider :deep(.el-slider__bar) {
  background-color: var(--primary-color) !important;
}

.custom-slider :deep(.el-slider__input) {
  width: 60px !important;
  margin-left: 12px !important;
}

.custom-slider :deep(.el-slider__input .el-input__wrapper) {
  background-color: rgba(42, 42, 74, 0.7) !important;
}

.custom-slider :deep(.el-slider__input .el-input__inner) {
  color: var(--primary-light) !important;
  font-weight: 500;
}
</style> 