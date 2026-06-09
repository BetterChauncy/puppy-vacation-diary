<template>
  <view class="page">
    <view v-if="!user" class="login-prompt">
      <view class="avatar-big">👤</view>
      <text class="login-text">正在登录...</text>
    </view>
    <view v-else class="profile-card">
      <image v-if="user.avatar" :src="user.avatar" mode="aspectFill" class="avatar" />
      <view v-else class="avatar placeholder">🐾</view>
      <text class="nickname">{{ user.nickname || '微信用户' }}</text>
      <text class="user-id">ID: {{ user.id }}</text>
      <button class="logout-btn" @click="onLogout">退出登录</button>
    </view>
    <view class="about">
      <text class="about-title">小狗的度假日记</text>
      <text class="about-ver">v1.0.0</text>
    </view>
  </view>
</template>

<script>
import { getMe } from '../../api/auth'

export default {
  data() {
    return {
      user: null,
    }
  },
  onShow() {
    this.loadUser()
  },
  methods: {
    async loadUser() {
      try {
        this.user = await getMe()
      } catch {
        // not logged in
      }
    },
    onLogout() {
      uni.removeStorageSync('token')
      this.user = null
      uni.showToast({ title: '已退出', icon: 'success' })
    },
  },
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 64px 0;
  gap: 12px;
}
.avatar-big {
  font-size: 64px;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: #e8f5e9;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-text {
  font-size: 14px;
  color: #999;
}
.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px;
  gap: 8px;
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}
.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  background: #e8f5e9;
}
.nickname {
  font-size: 18px;
  font-weight: 600;
}
.user-id {
  font-size: 12px;
  color: #bbb;
}
.logout-btn {
  margin-top: 16px;
  padding: 8px 24px;
  border-radius: 20px;
  border: 1px solid #ef4444;
  color: #ef4444;
  background: #fff;
  font-size: 14px;
}
.about {
  margin-top: auto;
  padding: 16px;
  text-align: center;
}
.about-title {
  display: block;
  font-size: 13px;
  color: #999;
}
.about-ver {
  display: block;
  font-size: 11px;
  color: #ccc;
  margin-top: 4px;
}
</style>
