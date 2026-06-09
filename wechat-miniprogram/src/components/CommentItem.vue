<template>
  <view class="comment">
    <view class="content">
      <text class="nickname">{{ comment.user?.nickname || '匿名' }}</text>
      <text class="text">{{ comment.content }}</text>
    </view>
    <view class="footer">
      <text class="time">{{ formatDate(comment.created_at) }}</text>
      <text v-if="isOwner" class="del" @click.stop="onDelete">删除</text>
    </view>
  </view>
</template>

<script>
import { formatDate } from '../utils/format'

export default {
  props: {
    comment: { type: Object, required: true },
    isOwner: { type: Boolean, default: false },
  },
  methods: {
    formatDate,
    onDelete() {
      this.$emit('delete', this.comment.id)
    },
  },
}
</script>

<style scoped>
.comment {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.comment:last-child {
  border-bottom: none;
}
.content {
  display: flex;
  flex-direction: column;
}
.nickname {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  margin-bottom: 2px;
}
.text {
  font-size: 14px;
  color: #333;
}
.footer {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}
.time {
  font-size: 11px;
  color: #bbb;
}
.del {
  font-size: 11px;
  color: #ef4444;
}
</style>
