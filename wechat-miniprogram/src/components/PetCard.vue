<template>
  <view class="card" @click="onClick">
    <image v-if="pet.avatar" :src="avatarUrl" mode="aspectFill" class="avatar" />
    <view v-else class="avatar placeholder">🐾</view>
    <view class="info">
      <text class="name">{{ pet.name }}</text>
      <text class="meta">{{ pet.species }} · {{ pet.gender }} · {{ age }}</text>
    </view>
    <text class="arrow">›</text>
  </view>
</template>

<script>
import { MEDIA_URL } from '../utils/constants'
import { formatAge } from '../utils/format'

export default {
  props: {
    pet: { type: Object, required: true },
  },
  computed: {
    avatarUrl() {
      return this.pet.avatar ? MEDIA_URL(this.pet.avatar) : ''
    },
    age() {
      return formatAge(this.pet.age)
    },
  },
  methods: {
    onClick() {
      uni.navigateTo({
        url: `/pages/pet-detail/pet-detail?petId=${this.pet.id}`,
      })
    },
  },
}
</script>

<style scoped>
.card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #fff;
  border-radius: 12px;
  margin: 0 12px 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  flex-shrink: 0;
}
.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: #e8f5e9;
}
.info {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.name {
  font-size: 16px;
  font-weight: 600;
}
.meta {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}
.arrow {
  font-size: 20px;
  color: #ccc;
}
</style>
