<template>
  <div class="params-audio">
    <el-form-item label="提示词" required>
      <el-input
        v-model="modelValue.prompt"
        type="textarea"
        :rows="4"
        placeholder="请输入音频描述"
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
    
    <el-form-item label="音频类型">
      <el-select v-model="modelValue.audio_type" class="w-full">
        <el-option 
          v-for="option in audioTypeOptions" 
          :key="option.value" 
          :label="option.label" 
          :value="option.value"
        />
      </el-select>
    </el-form-item>
    
    <template v-if="modelValue.audio_type === 'voice-clone'">
      <el-form-item label="声音克隆样本">
        <el-upload
          class="voice-clone-uploader"
          action="#"
          accept="audio/*"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleVoiceCloneChange"
        >
          <div v-if="voiceCloneFileUrl" class="voice-sample-preview">
            <audio :src="voiceCloneFileUrl" controls class="voice-sample-audio"></audio>
            <el-button size="small" type="danger" @click.stop="removeVoiceClone">移除</el-button>
          </div>
          <div v-else class="upload-placeholder">
            <el-icon><Microphone /></el-icon>
            <div class="placeholder-text">点击上传声音样本</div>
            <div class="placeholder-hint">支持MP3、WAV格式，10秒以上</div>
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
            :max="120" 
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
            :max="10" 
            :step="0.1" 
            show-input
          />
        </el-form-item>
      </el-col>
    </el-row>
    
    <div class="form-divider">高级设置</div>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="语速">
          <el-slider 
            v-model="modelValue.speech_speed" 
            :min="0.5" 
            :max="2.0" 
            :step="0.1" 
            show-input
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="音调">
          <el-slider 
            v-model="modelValue.pitch" 
            :min="-10" 
            :max="10" 
            :step="1" 
            show-input
          />
        </el-form-item>
      </el-col>
    </el-row>
    
    <el-row :gutter="12">
      <el-col :span="12">
        <el-form-item label="情感强度">
          <el-select v-model="modelValue.emotion" class="w-full">
            <el-option 
              v-for="option in emotionOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="口音">
          <el-select v-model="modelValue.accent" class="w-full">
            <el-option 
              v-for="option in accentOptions" 
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
        <el-form-item label="音乐风格">
          <el-select v-model="modelValue.music_genre" class="w-full">
            <el-option 
              v-for="option in musicGenreOptions" 
              :key="option.value" 
              :label="option.label" 
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="环境音">
          <el-select v-model="modelValue.ambient_sound" class="w-full">
            <el-option 
              v-for="option in ambientSoundOptions" 
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
import { Microphone } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

// 声音克隆文件
const voiceCloneFileUrl = ref(null)
const voiceCloneFile = ref(null)

// 处理声音克隆文件变化
const handleVoiceCloneChange = (file) => {
  if (file) {
    voiceCloneFile.value = file.raw
    voiceCloneFileUrl.value = URL.createObjectURL(file.raw)
  }
}

// 移除声音克隆文件
const removeVoiceClone = () => {
  voiceCloneFile.value = null
  voiceCloneFileUrl.value = null
}

// 选项数据
const modelOptions = [
  { label: 'AudioLDM 2', value: 'audioldm2' },
  { label: 'AudioGen', value: 'audiogen' },
  { label: 'MusicGen', value: 'musicgen' },
  { label: 'XTTS/TorToiSe', value: 'xtts-tortoise' },
]

const audioTypeOptions = [
  { label: '音频克隆', value: 'voice-clone' },
  { label: '语音生成', value: 'speech' },
  { label: '音乐生成', value: 'music' },
  { label: '环境音效生成', value: 'ambient' },
  { label: '音效设计', value: 'sound-design' },
]

const emotionOptions = [
  { label: '中性', value: 'neutral' },
  { label: '开心', value: 'happy' },
  { label: '悲伤', value: 'sad' },
  { label: '愤怒', value: 'angry' },
  { label: '惊讶', value: 'surprised' },
  { label: '恐惧', value: 'fearful' },
]

const accentOptions = [
  { label: '普通话', value: 'mandarin' },
  { label: '英式英语', value: 'british' },
  { label: '美式英语', value: 'american' },
  { label: '港式粤语', value: 'hk-cantonese' },
  { label: '日语口音', value: 'japanese' },
  { label: '韩语口音', value: 'korean' },
]

const musicGenreOptions = [
  { label: '无 (非音乐)', value: 'none' },
  { label: '流行', value: 'pop' },
  { label: '摇滚', value: 'rock' },
  { label: '电子', value: 'electronic' },
  { label: '古典', value: 'classical' },
  { label: '爵士', value: 'jazz' },
  { label: '嘻哈', value: 'hip-hop' },
  { label: '民谣', value: 'folk' },
]

const ambientSoundOptions = [
  { label: '禁用', value: 'disabled' },
  { label: '小房间', value: 'small-room' },
  { label: '大厅', value: 'hall' },
  { label: '户外空间', value: 'outdoor' },
  { label: '电话/无线电', value: 'telephone' },
  { label: '新闻发布会', value: 'press-conference' },
  { label: '城市嘈杂音', value: 'city-noise' },
  { label: '咖啡厅', value: 'cafe' },
  { label: '办公室环境', value: 'office' },
  { label: '自然环境', value: 'nature' },
  { label: '体育场', value: 'stadium' },
  { label: '演唱会', value: 'concert' },
]
</script>

<style scoped>
.params-audio {
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

.voice-clone-uploader {
  width: 100%;
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.voice-sample-preview {
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
}

.voice-sample-audio {
  width: 100%;
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

.placeholder-hint {
  margin-top: var(--space-xs);
  font-size: 0.8rem;
  opacity: 0.7;
}
</style> 