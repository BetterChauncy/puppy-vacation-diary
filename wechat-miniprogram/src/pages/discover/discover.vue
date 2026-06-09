<template>
  <view>
    <view v-if="loading" class="loading">加载中...</view>
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
    }
  },
  onShow() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      try {
        this.pets = await fetchPets()
      } catch {
        uni.showToast({ title: '加载失败', icon: 'none' })
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
</style>
