<script setup lang="ts">
import type { Media } from '../types'
import MediaCard from './MediaCard.vue'

defineProps<{ items: Media[] }>()
const emit = defineEmits<{ preview: [media: Media] }>()
</script>

<template>
  <div v-if="items.length === 0" class="empty">
    还没有照片或视频，去 <router-link to="/admin">管理页面</router-link> 上传吧 ✨
  </div>
  <div v-else class="grid">
    <MediaCard
      v-for="item in items"
      :key="item.id"
      :media="item"
      @click="emit('preview', item)"
    />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.empty {
  text-align: center;
  padding: 48px 16px;
  color: var(--text-secondary);
  font-size: 14px;
}
.empty a {
  color: var(--primary);
}
</style>
