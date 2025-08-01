<template>
  <div class="params-image">
    <el-form-item label="提示词" required>
      <el-input
        v-model="modelValue.prompt"
        type="textarea"
        :rows="4"
        placeholder="请输入图片描述"
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
    
    <el-form-item label="图片风格">
      <el-select v-model="modelValue.style" class="w-full">
        <el-option 
          v-for="option in styleOptions" 
          :key="option.value" 
          :label="option.label" 
          :value="option.value"
        />
      </el-select>
    </el-form-item>
    
    <el-form-item label="长宽比">
      <el-select v-model="modelValue.aspect_ratio" class="w-full">
        <el-option 
          v-for="option in aspectRatioOptions" 
          :key="option.value" 
          :label="option.label" 
          :value="option.value"
        />
      </el-select>
    </el-form-item>
    
    <div class="form-divider">高级设置</div>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="采样步数">
          <el-slider 
            v-model="modelValue.sampling_steps" 
            :min="10" 
            :max="100" 
            :step="1" 
            show-input
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="提示词相关性 (CFG)">
          <el-slider 
            v-model="modelValue.cfg_scale" 
            :min="0" 
            :max="20" 
            :step="0.1" 
            show-input
          />
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

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const modelOptions = [
  { label: 'Stable Diffusion XL', value: 'sdxl' },
  { label: 'DALL-E 3', value: 'dalle3' },
  { label: 'Midjourney v6', value: 'midjourney' },
]

const styleOptions = [
  { label: '无风格', value: 'none' },
  { label: '电影', value: 'cinematic' },
  { label: '摄影', value: 'photographic' },
  { label: '动漫', value: 'anime' },
  { label: '幻想艺术', value: 'fantasy-art' },
  { label: '像素艺术', value: 'pixel-art' },
]

const aspectRatioOptions = [
  { label: '1:1 (正方形)', value: '1:1' },
  { label: '16:9 (宽屏)', value: '16:9' },
  { label: '9:16 (垂直)', value: '9:16' },
  { label: '4:3 (标准)', value: '4:3' },
  { label: '3:2 (摄影)', value: '3:2' },
]
</script>

<style scoped>
.params-image {
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
</style>
