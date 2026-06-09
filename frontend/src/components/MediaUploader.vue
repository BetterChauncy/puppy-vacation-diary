<script setup lang="ts">
import { ref } from 'vue'
import { uploadMedia } from '../api'

const props = defineProps<{ petId: number }>()
const emit = defineEmits<{ uploaded: [] }>()

const uploading = ref(false)
const progress = ref(0)
const error = ref('')

async function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  uploading.value = true
  error.value = ''
  progress.value = 0
  try {
    await uploadMedia(props.petId, Array.from(input.files), (p) => (progress.value = p))
    emit('uploaded')
    input.value = ''
  } catch (e: any) {
    const detail = e?.response?.data?.detail
    error.value = detail ? `上传失败：${detail}` : '上传失败，请重试'
    console.error('Upload error:', e)
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="uploader">
    <label class="upload-btn btn btn-primary">
      {{ uploading ? `上传中 ${progress}%` : '+ 上传照片/视频' }}
      <input
        type="file"
        multiple
        accept="image/jpeg,image/png,image/gif,image/webp,video/mp4,video/quicktime"
        :disabled="uploading"
        @change="onFileChange"
      />
    </label>
    <p v-if="error" class="error">{{ error }}</p>
    <p class="hint">支持 JPG / PNG / GIF / WEBP / MP4 / MOV，单次最多 10 个文件</p>
  </div>
</template>

<style scoped>
.uploader {
  margin-bottom: 16px;
}
.upload-btn {
  display: inline-flex;
  cursor: pointer;
}
.upload-btn input {
  display: none;
}
.error {
  color: #ef4444;
  font-size: 13px;
  margin-top: 6px;
}
.hint {
  color: var(--text-secondary);
  font-size: 12px;
  margin-top: 6px;
}
</style>
