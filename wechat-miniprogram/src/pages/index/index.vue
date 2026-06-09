<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else-if="!pet" class="empty">
      <text>还没有添加小狗 🐾</text>
    </view>
    <template v-else>
      <PetProfile :pet="pet" />
      <view class="section-title">📸 最近记录</view>
      <MediaGrid :items="media" />
    </template>
  </view>
</template>

<script>
import { fetchConfig } from '../../api/config'
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
  onShow() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      try {
        const cfg = await fetchConfig()
        if (cfg.homepage_pet_id) {
          this.pet = await fetchPet(cfg.homepage_pet_id)
          const res = await fetchMedia(cfg.homepage_pet_id, 20, 0)
          this.media = res.items || res
        }
      } catch {
        // no pet configured
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.loading,
.empty {
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
