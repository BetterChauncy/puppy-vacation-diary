<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  createPet,
  fetchConfig,
  fetchPets,
  updateConfig,
  updatePet,
  deletePet,
  fetchMedia,
  deleteMedia,
  fetchMediaItem,
} from '../api'
import type { AppConfig, Media, Pet, PetFormData } from '../types'
import PetForm from '../components/PetForm.vue'
import MediaUploader from '../components/MediaUploader.vue'
import MediaPreview from '../components/MediaPreview.vue'

const pets = ref<Pet[]>([])
const config = ref<AppConfig | null>(null)
const editingPet = ref<Pet | null>(null)
const showForm = ref(false)
const managingPet = ref<Pet | null>(null)
const mediaList = ref<Media[]>([])
const previewMedia = ref<Media | null>(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const [petsData, configData] = await Promise.all([fetchPets(), fetchConfig()])
    pets.value = petsData
    config.value = configData
  } finally {
    loading.value = false
  }
}

async function loadMedia(pet: Pet) {
  managingPet.value = pet
  mediaList.value = await fetchMedia(pet.id)
}

async function handleSave(data: PetFormData) {
  if (editingPet.value) {
    await updatePet(editingPet.value.id, data)
  } else {
    await createPet(data)
  }
  cancelForm()
  await load()
}

async function handleDelete(id: number) {
  if (!confirm('确定删除这只宠物？')) return
  await deletePet(id)
  if (managingPet.value?.id === id) managingPet.value = null
  await load()
}

async function toggleHomepage(pet: Pet) {
  await updatePet(pet.id, { is_homepage: !pet.is_homepage })
  await load()
}

async function handleRotationChange(rotation: string) {
  await updateConfig(rotation)
  config.value!.homepage_rotation = rotation as 'daily' | 'hourly'
}

async function handleDeleteMedia(id: number) {
  await deleteMedia(id)
  mediaList.value = mediaList.value.filter((m) => m.id !== id)
}

async function openPreview(media: Media) {
  const fresh = await fetchMediaItem(media.id)
  previewMedia.value = fresh
}

function closePreview() {
  previewMedia.value = null
  if (managingPet.value) {
    fetchMedia(managingPet.value.id).then((m) => (mediaList.value = m))
  }
}

function editPet(pet: Pet) {
  editingPet.value = pet
  showForm.value = true
}

function newPet() {
  editingPet.value = null
  showForm.value = true
}

function cancelForm() {
  showForm.value = false
  editingPet.value = null
}

onMounted(load)
</script>

<template>
  <div v-if="managingPet" class="media-manager">
    <div class="back-row">
      <button class="btn btn-outline" @click="managingPet = null">← 返回列表</button>
      <strong>{{ managingPet.name }} 的媒体</strong>
    </div>
    <MediaUploader :pet-id="managingPet.id" @uploaded="loadMedia(managingPet)" />
    <div v-if="mediaList.length === 0" class="empty">暂无媒体文件</div>
    <div v-else class="media-list">
      <div v-for="m in mediaList" :key="m.id" class="media-item" @click="openPreview(m)">
        <img
          v-if="m.media_type === 'photo'"
          :src="`/uploads/${m.thumbnail_key || m.file_key}`"
          class="media-thumb"
        />
        <video v-else :src="`/uploads/${m.file_key}`" class="media-thumb" muted />
        <div class="media-info">
          <span class="media-name">{{ m.original_filename }}</span>
          <span class="media-meta">{{ (m.file_size / 1024).toFixed(1) }} KB · ❤️ {{ m.likes_count }}</span>
        </div>
        <button class="btn btn-danger btn-sm" @click.stop="handleDeleteMedia(m.id)">删除</button>
      </div>
    </div>
    <MediaPreview :media="previewMedia" @close="closePreview" />
  </div>

  <div v-else>
    <div class="admin-header">
      <h2>宠物管理</h2>
      <button class="btn btn-primary" @click="newPet">+ 添加宠物</button>
    </div>

    <div v-if="showForm" class="card" style="margin-bottom: 16px">
      <h3 style="margin-bottom: 8px">{{ editingPet ? '编辑宠物' : '添加宠物' }}</h3>
      <PetForm :pet="editingPet" @save="handleSave" @cancel="cancelForm" />
    </div>

    <div v-if="config" class="homepage-section card">
      <h3>🌟 主页设置</h3>
      <p class="homepage-desc">选择显示在主页的宠物，选多只则自动轮换</p>
      <div class="homepage-pets">
        <button
          v-for="pet in pets"
          :key="pet.id"
          class="hp-tag"
          :class="{ active: pet.is_homepage }"
          @click="toggleHomepage(pet)"
        >
          {{ pet.is_homepage ? '⭐' : '☆' }} {{ pet.name }}
        </button>
      </div>
      <div v-if="config.homepage_pet_ids.length > 1" class="rotation-section">
        <span class="rotation-label">轮换模式：</span>
        <label class="radio-inline">
          <input
            type="radio"
            value="daily"
            :checked="config.homepage_rotation === 'daily'"
            @change="handleRotationChange('daily')"
          />
          每日
        </label>
        <label class="radio-inline">
          <input
            type="radio"
            value="hourly"
            :checked="config.homepage_rotation === 'hourly'"
            @change="handleRotationChange('hourly')"
          />
          每小时
        </label>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="pets.length === 0" class="empty">还没有宠物，点击上方按钮添加 🐾</div>
    <div v-else class="pet-list">
      <div v-for="pet in pets" :key="pet.id" class="pet-row card">
        <div class="pet-row-info">
          <div class="pet-avatar-mini">
            <img v-if="pet.avatar" :src="`/uploads/${pet.avatar}`" />
            <span v-else>🐾</span>
          </div>
          <div>
            <strong>{{ pet.name }}</strong>
            <span class="pet-meta">{{ pet.species }} · {{ pet.gender }} · {{ pet.age }}岁</span>
          </div>
        </div>
        <div class="pet-row-actions">
          <button class="btn btn-outline btn-sm" @click="loadMedia(pet)">媒体</button>
          <button class="btn btn-outline btn-sm" @click="editPet(pet)">编辑</button>
          <button class="btn btn-danger btn-sm" @click="handleDelete(pet.id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.admin-header h2 {
  font-size: 18px;
}
.loading,
.empty {
  text-align: center;
  padding: 48px 16px;
  color: var(--text-secondary);
}
.pet-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.pet-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.pet-row-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.pet-avatar-mini {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}
.pet-avatar-mini img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.pet-meta {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}
.pet-row-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}
.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.back-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.media-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.media-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--card);
  border-radius: 10px;
  padding: 8px 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
.media-thumb {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}
.media-info {
  flex: 1;
  min-width: 0;
}
.media-name {
  display: block;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.media-meta {
  font-size: 11px;
  color: var(--text-secondary);
}

.homepage-section {
  margin-bottom: 16px;
}
.homepage-section h3 {
  font-size: 15px;
  margin-bottom: 4px;
}
.homepage-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}
.homepage-pets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}
.hp-tag {
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--card);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.hp-tag.active {
  background: var(--primary-light);
  border-color: var(--primary);
  color: var(--primary);
  font-weight: 600;
}
.hp-tag:hover {
  border-color: var(--primary);
}
.rotation-section {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}
.rotation-label {
  color: var(--text-secondary);
}
.radio-inline {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}
</style>
