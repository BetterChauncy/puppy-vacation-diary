<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else-if="error" class="error">
      <text>加载失败</text>
      <button class="retry-btn" @click="load">重试</button>
    </view>
    <view v-else-if="pets.length === 0" class="empty">
      <text class="empty-icon">🐾</text>
      <text>还没有宠物</text>
      <button class="add-btn" @click="onAdd">添加小狗</button>
    </view>
    <view v-else class="list">
      <PetCard v-for="pet in pets" :key="pet.id" :pet="pet" />
      <view class="add-card" @click="onAdd">
        <text class="add-icon">+</text>
        <text class="add-text">添加小狗</text>
      </view>
    </view>
  </view>
</template>

<script>
import { fetchPets } from '../../api/pet'
import PetCard from '../../components/PetCard.vue'

export default {
  components: { PetCard },
  data() {
    return {
      pets: [],
      loading: true,
      error: false,
    }
  },
  onShow() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      this.error = false
      try {
        this.pets = await fetchPets()
      } catch (e) {
        console.error('发现页加载失败:', e)
        this.error = true
      } finally {
        this.loading = false
      }
    },
    onAdd() {
      uni.navigateTo({ url: '/pages/pet-add/pet-add' })
    },
  },
}
</script>

<style scoped>
.loading,
.empty,
.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 64px 16px;
  color: #999;
  font-size: 14px;
  gap: 12px;
}
.empty-icon {
  font-size: 48px;
}
.error {
  color: #ef4444;
}
.retry-btn {
  margin-top: 4px;
  padding: 6px 20px;
  border-radius: 16px;
  border: 1px solid #ef4444;
  color: #ef4444;
  background: #fff;
  font-size: 13px;
}
.add-btn {
  margin-top: 4px;
  padding: 8px 24px;
  border-radius: 20px;
  background: #07c160;
  color: #fff;
  font-size: 14px;
}
.list {
  padding: 12px 0;
}
.add-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  margin: 0 12px;
  border-radius: 12px;
  border: 2px dashed #ddd;
  background: #fafafa;
}
.add-icon {
  font-size: 24px;
  color: #07c160;
  font-weight: bold;
}
.add-text {
  font-size: 14px;
  color: #07c160;
  font-weight: 500;
}
</style>
