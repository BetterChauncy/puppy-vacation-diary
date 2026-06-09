<script setup lang="ts">
import type { Pet } from '../types'
import { mediaUrl } from '../api'

const props = defineProps<{ pet: Pet }>()

const speciesLabel: Record<string, string> = {
  dog: '🐶 狗',
  cat: '🐱 猫',
  rabbit: '🐰 兔',
  hamster: '🐹 仓鼠',
  bird: '🐦 鸟',
}
</script>

<template>
  <div class="profile card">
    <div class="avatar-col">
      <img
        v-if="pet.avatar"
        :src="mediaUrl(pet.avatar)"
        class="avatar"
        alt="avatar"
      />
      <div v-else class="avatar avatar-placeholder">🐾</div>
    </div>
    <div class="info-col">
      <h1 class="name">{{ pet.name }}</h1>
      <div class="info-row">
        <span>{{ speciesLabel[pet.species] || pet.species }}</span>
        <span class="dot">·</span>
        <span>{{ pet.gender }}</span>
      </div>
      <div class="info-row">
        <span>🎂 {{ pet.age }}岁</span>
        <span v-if="pet.birthday" class="dot">·</span>
        <span v-if="pet.birthday">{{ pet.birthday }}</span>
      </div>
      <div v-if="pet.address" class="info-row">📍 {{ pet.address }}</div>
      <div v-if="pet.bio" class="bio">💬 {{ pet.bio }}</div>
    </div>
  </div>
</template>

<style scoped>
.profile {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}
.avatar-col {
  flex-shrink: 0;
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-light);
}
.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  background: var(--primary-light);
}
.info-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
}
.name {
  font-size: 22px;
  font-weight: 700;
}
.info-row {
  font-size: 14px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}
.dot {
  color: var(--border);
}
.bio {
  font-size: 14px;
  color: var(--text-secondary);
  font-style: italic;
  margin-top: 2px;
}
</style>
