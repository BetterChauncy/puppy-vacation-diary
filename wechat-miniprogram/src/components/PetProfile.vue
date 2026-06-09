<template>
  <view class="profile">
    <view class="header">
      <image v-if="pet.avatar" :src="avatarUrl" mode="aspectFill" class="avatar" />
      <view v-else class="avatar placeholder">🐾</view>
      <view class="info">
        <text class="name">{{ pet.name }}</text>
        <text class="bio">{{ pet.bio || '' }}</text>
      </view>
    </view>
    <view class="stats">
      <view class="stat">
        <text class="stat-val">{{ pet.species }}</text>
        <text class="stat-label">品种</text>
      </view>
      <view class="stat">
        <text class="stat-val">{{ pet.gender }}</text>
        <text class="stat-label">性别</text>
      </view>
      <view class="stat">
        <text class="stat-val">{{ age }}</text>
        <text class="stat-label">年龄</text>
      </view>
    </view>
    <view v-if="pet.address" class="address">📍 {{ pet.address }}</view>
  </view>
</template>

<script>
import { MEDIA_URL } from '../utils/constants'
import { formatAge } from '../utils/format'

export default {
  props: { pet: { type: Object, required: true } },
  computed: {
    avatarUrl() {
      return this.pet.avatar ? MEDIA_URL(this.pet.avatar) : ''
    },
    age() {
      return formatAge(this.pet.age)
    },
  },
}
</script>

<style scoped>
.profile {
  background: #fff;
  border-radius: 16px;
  margin: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  flex-shrink: 0;
}
.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  background: #e8f5e9;
}
.info {
  flex: 1;
}
.name {
  font-size: 20px;
  font-weight: 700;
}
.bio {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
  display: block;
}
.stats {
  display: flex;
  gap: 0;
  background: #f5f5f5;
  border-radius: 10px;
  overflow: hidden;
}
.stat {
  flex: 1;
  text-align: center;
  padding: 10px 0;
}
.stat + .stat {
  border-left: 1px solid #e0e0e0;
}
.stat-val {
  display: block;
  font-size: 15px;
  font-weight: 600;
}
.stat-label {
  display: block;
  font-size: 11px;
  color: #999;
  margin-top: 2px;
}
.address {
  font-size: 13px;
  color: #999;
  margin-top: 8px;
}
</style>
