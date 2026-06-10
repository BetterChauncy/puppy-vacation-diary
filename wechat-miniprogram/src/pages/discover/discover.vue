<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else-if="error" class="error">
      <text>加载失败</text>
      <button class="retry-btn" @click="load">重试</button>
    </view>
    <view v-else-if="pets.length === 0" class="empty">还没有宠物 🐾</view>
    <PetCard v-for="pet in pets" :key="pet.id" :pet="pet" />
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
  },
}
</script>

<style scoped>
.loading,
.empty,
.error {
  text-align: center;
  padding: 64px 16px;
  color: #999;
  font-size: 14px;
}
.error {
  color: #ef4444;
}
.retry-btn {
  margin-top: 12px;
  padding: 6px 20px;
  border-radius: 16px;
  border: 1px solid #ef4444;
  color: #ef4444;
  background: #fff;
  font-size: 13px;
}
</style>
