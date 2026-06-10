<template>
  <view v-if="items.length === 0" class="empty">暂无照片或视频</view>
  <view v-else class="grid">
    <view
      v-for="(item, index) in items"
      :key="item.id"
      class="cell"
      @click="onClick(item, index)"
    >
      <image
        v-if="item.media_type === 'photo'"
        :src="mediaUrl(item.thumbnail_key || item.file_key)"
        mode="aspectFill"
        class="thumb"
        lazy-load
      />
      <video
        v-else
        :src="mediaUrl(item.file_key)"
        class="thumb"
        muted
        :show-play-btn="false"
        :controls="false"
      />
      <view v-if="item.media_type === 'video'" class="play-badge">▶</view>
    </view>
  </view>
</template>

<script>
import { MEDIA_URL } from '../utils/constants'

export default {
  props: {
    items: { type: Array, default: () => [] },
    petId: { type: Number, default: 0 },
  },
  methods: {
    mediaUrl(key) {
      return MEDIA_URL(key)
    },
    onClick(item, index) {
      uni.navigateTo({
        url: `/pages/media-preview/media-preview?mediaId=${item.id}&index=${index}&petId=${this.petId || item.pet_id || ''}`,
      })
    },
  },
}
</script>

<style scoped>
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 0 2px;
}
.cell {
  width: calc(33.333% - 3px);
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}
.thumb {
  width: 100%;
  height: 100%;
}
.play-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  color: #fff;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
}
.empty {
  text-align: center;
  padding: 48px 16px;
  color: #999;
  font-size: 14px;
}
</style>
