<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else-if="error" class="error">
      <text>加载失败</text>
      <button class="retry-btn" @click="load">重试</button>
    </view>
    <template v-else>
      <PetProfile :pet="pet" />
      <view class="section-title">📸 全部记录</view>
      <MediaGrid :items="media" :petId="petId" />
    </template>
  </view>
</template>

<script>
import { fetchPet } from '../../api/pet'
import { fetchMedia } from '../../api/media'
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
    }
  },
  onLoad(options) {
    this.petId = Number(options.petId)
  },
  onShow() {
    if (this.petId) this.load()
  },
  methods: {
    async load() {
      this.loading = true
      this.error = false
      try {
        this.pet = await fetchPet(this.petId)
        const res = await fetchMedia(this.petId, 50, 0)
        this.media = res.items || res
      } catch (e) {
        console.error('宠物详情加载失败:', e)
        this.error = true
      } finally {
        this.loading = false
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
</style>
