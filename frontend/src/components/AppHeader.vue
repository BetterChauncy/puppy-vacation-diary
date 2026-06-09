<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">🐕 小狗的度假日记</router-link>
      <nav class="nav">
        <router-link to="/" class="nav-link" :class="{ active: route.name === 'home' }">
          主页
        </router-link>
        <router-link to="/admin" class="nav-link" :class="{ active: route.name === 'admin' }">
          管理
        </router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: var(--card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  max-width: 640px;
  margin: 0 auto;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}
.nav {
  display: flex;
  gap: 12px;
}
.nav-link {
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}
.nav-link:hover,
.nav-link.active {
  background: var(--primary-light);
  color: var(--primary);
}
</style>
