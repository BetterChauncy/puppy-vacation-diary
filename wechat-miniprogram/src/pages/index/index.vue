<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else-if="error" class="error">
      <text>加载失败，请检查网络</text>
      <button class="retry-btn" @click="load">重试</button>
    </view>
    <view v-else-if="!pet" class="empty">
      <text>还没有添加小狗 🐾</text>
    </view>
    <template v-else>
      <PetProfile :pet="pet" />
      <view class="section-title">📸 最近记录</view>
      <MediaGrid :items="media" :petId="petId" />
      <view class="upload-fab" @click="handleUpload">
        <text class="fab-icon">＋</text>
      </view>
    </template>
  </view>
</template>

<script>
import { fetchConfig } from '../../api/config'
import { fetchPet, fetchPets } from '../../api/pet'
import { fetchMedia, createFromCloud } from '../../api/media'
import PetProfile from '../../components/PetProfile.vue'
import MediaGrid from '../../components/MediaGrid.vue'

export default {
  components: { PetProfile, MediaGrid },
  data() {
    return {
      pet: null,
      media: [],
      loading: true,
      error: false,
      petId: 0,
    }
  },
  onShow() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      this.error = false
      try {
        const cfg = await fetchConfig()
        let pid = cfg.homepage_pet_id
        if (!pid) {
          const pets = await fetchPets()
          if (pets.length) pid = pets[0].id
        }
        if (pid) {
          this.petId = pid
          this.pet = await fetchPet(pid)
          const res = await fetchMedia(pid, 20, 0)
          this.media = res.items || res
        }
      } catch (e) {
        console.error('首页加载失败:', e)
        this.error = true
      } finally {
        this.loading = false
      }
    },
    handleUpload() {
      uni.showActionSheet({
        itemList: ['📷 拍照或录像', '🖼 从相册选择'],
        success: (res) => {
          if (res.tapIndex === 0) {
            this._pickMedia('camera')
          } else {
            this._pickMedia('album')
          }
        },
      })
    },
    async _pickMedia(sourceType) {
      try {
        const res = await uni.chooseMedia({
          count: 1,
          sourceType: [sourceType],
          maxDuration: 60,
        })
        const file = res.tempFiles[0]
        await this._uploadFile(file)
      } catch (e) {
        if (e.errMsg?.includes('cancel')) return
        console.error('选择失败:', e)
        uni.showToast({ title: '选择失败', icon: 'none' })
      }
    },
    async _uploadFile(file) {
      if (!this.petId) {
        uni.showToast({ title: '请先选择宠物', icon: 'none' })
        return
      }
      uni.showLoading({ title: '上传中...' })
      try {
        const ext = (file.tempFilePath || '').split('.').pop() || 'jpg'
        const cloudPath = `pets/${this.petId}/${Date.now()}_${Math.random().toString(36).slice(2, 8)}.${ext}`
        const uploadRes = await wx.cloud.uploadFile({
          cloudPath,
          filePath: file.tempFilePath,
        })
        const urlRes = await wx.cloud.getTempFileURL({
          fileList: [{ fileID: uploadRes.fileID }],
        })
        const fileObj = urlRes.fileList[0]
        const mimeType = file.fileType === 'video' ? 'video/mp4' : `image/${ext === 'png' ? 'png' : 'jpeg'}`
        await createFromCloud(this.petId, {
          file_id: uploadRes.fileID,
          temp_file_url: fileObj.tempFileURL,
          mime_type: mimeType,
          original_filename: cloudPath.split('/').pop() || 'unknown',
          file_size: file.size || 0,
        })
        uni.hideLoading()
        uni.showToast({ title: '上传成功', icon: 'success' })
        const res = await fetchMedia(this.petId, 20, 0)
        this.media = res.items || res
      } catch (e) {
        uni.hideLoading()
        console.error('上传失败:', e)
        uni.showToast({ title: e.message || '上传失败', icon: 'none' })
      }
    },
  },
}
</script>

<style scoped>
.loading,
.empty,
.error {
  text-align: center;
  padding: 64px 16px;
  color: #999;
  font-size: 14px;
}
.error {
  color: #ef4444;
}
.retry-btn {
  margin-top: 12px;
  padding: 6px 20px;
  border-radius: 16px;
  border: 1px solid #ef4444;
  color: #ef4444;
  background: #fff;
  font-size: 13px;
}
.section-title {
  font-size: 15px;
  font-weight: 600;
  padding: 12px 16px 8px;
}

.upload-fab {
  position: fixed;
  bottom: 32px;
  right: 20px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #007aff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,122,255,0.4);
  z-index: 50;
}
.fab-icon {
  font-size: 24px;
  line-height: 1;
}
</style>
