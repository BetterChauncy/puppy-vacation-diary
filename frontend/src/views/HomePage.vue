<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { fetchConfig, fetchPet, fetchMedia, fetchMediaItem } from '../api'
import type { Media, Pet } from '../types'
import PetProfile from '../components/PetProfile.vue'
import TabBar from '../components/TabBar.vue'
import MediaGrid from '../components/MediaGrid.vue'
import MediaPreview from '../components/MediaPreview.vue'

const pet = ref<Pet | null>(null)
const allMedia = ref<Media[]>([])
const activeTab = ref<'recommend' | 'all'>('recommend')
const loading = ref(true)
const previewMedia = ref<Media | null>(null)

const tabs = [
  { key: 'recommend', label: '🌟 推荐' },
  { key: 'all', label: '📋 全部' },
]

const displayMedia = computed(() => {
  if (activeTab.value === 'recommend') {
    const sorted = [...allMedia.value].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )
    const photos = sorted.filter((m) => m.media_type === 'photo')
    const videos = sorted.filter((m) => m.media_type === 'video')
    return [...photos, ...videos].slice(0, 20)
  }
  return [...allMedia.value].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  )
})

async function openPreview(media: Media) {
  const fresh = await fetchMediaItem(media.id)
  previewMedia.value = fresh
}

function closePreview() {
  previewMedia.value = null
  if (pet.value) {
    fetchMedia(pet.value.id).then((m) => (allMedia.value = m))
  }
}

onMounted(async () => {
  try {
    const cfg = await fetchConfig()
    if (cfg.homepage_pet_id) {
      pet.value = await fetchPet(cfg.homepage_pet_id)
      allMedia.value = await fetchMedia(cfg.homepage_pet_id)
    }
  } catch {
    // no pet configured yet
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div v-if="loading" class="loading">加载中...</div>
  <div v-else-if="!pet" class="empty-state">
    <p>还没有添加小狗 🐾</p>
    <router-link to="/admin" class="btn btn-primary">去添加</router-link>
  </div>
  <template v-else>
    <PetProfile :pet="pet" />
    <TabBar :tabs="tabs" :active="activeTab" @change="activeTab = $event as 'recommend' | 'all'" />
    <MediaGrid :items="displayMedia" @preview="openPreview" />
    <MediaPreview :media="previewMedia" @close="closePreview" />
  </template>
</template>

<style scoped>
.loading {
  text-align: center;
  padding: 48px;
  color: var(--text-secondary);
}
.empty-state {
  text-align: center;
  padding: 64px 16px;
}
.empty-state p {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}
</style>
