<script setup lang="ts">
defineProps<{ tabs: { key: string; label: string }[]; active: string }>()
const emit = defineEmits<{ change: [key: string] }>()
</script>

<template>
  <div class="tab-bar">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      class="tab"
      :class="{ active: active === tab.key }"
      @click="emit('change', tab.key)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<style scoped>
.tab-bar {
  display: flex;
  gap: 0;
  background: var(--card);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
  margin-bottom: 16px;
}
.tab {
  flex: 1;
  padding: 10px;
  border: none;
  background: transparent;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  font-weight: 500;
}
.tab.active {
  background: var(--primary);
  color: #fff;
}
.tab:not(.active):hover {
  background: var(--primary-light);
}
</style>
