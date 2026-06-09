<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
    <template v-else>
      <PetProfile :pet="pet" />
      <view class="section-title">📸 全部记录</view>
      <MediaGrid :items="media" />
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
      try {
        this.pet = await fetchPet(this.petId)
        const res = await fetchMedia(this.petId, 50, 0)
        this.media = res.items || res
      } catch {
        uni.showToast({ title: '加载失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 64px 16px;
  color: #999;
  font-size: 14px;
}
.section-title {
  font-size: 15px;
  font-weight: 600;
  padding: 12px 16px 8px;
}
</style>
