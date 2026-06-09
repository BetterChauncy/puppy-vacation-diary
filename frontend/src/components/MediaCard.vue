<script setup lang="ts">
import type { Media } from '../types'
import { mediaUrl } from '../api'

const props = defineProps<{ media: Media }>()
const emit = defineEmits<{ click: [] }>()
</script>

<template>
  <div class="media-card" @click="emit('click')">
    <template v-if="media.media_type === 'photo'">
      <img
        :src="mediaUrl(media.thumbnail_key || media.file_key)"
        :alt="media.original_filename"
        class="media-img"
        loading="lazy"
      />
    </template>
    <template v-else>
      <video
        :src="mediaUrl(media.file_key)"
        class="media-img"
        muted
        preload="metadata"
      />
      <div class="play-icon">▶</div>
    </template>
    <div class="media-overlay">
      <span class="file-name">{{ media.original_filename }}</span>
      <span class="like-badge">❤️ {{ media.likes_count }}</span>
    </div>
  </div>
</template>

<style scoped>
.media-card {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  aspect-ratio: 1;
  cursor: pointer;
}
.media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s;
}
.media-card:hover .media-img {
  transform: scale(1.05);
}
.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 32px;
  color: #fff;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
  pointer-events: none;
}
.media-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 6px 8px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  color: #fff;
  font-size: 11px;
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.media-card:hover .media-overlay {
  opacity: 1;
}
.file-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.like-badge {
  flex-shrink: 0;
}
</style>
