<template>
  <view class="page">
    <view v-if="loading" class="loading">加载中...</view>
    <template v-else-if="media">
      <view class="media-area">
        <image
          v-if="media.media_type === 'photo'"
          :src="mediaUrl"
          mode="widthFix"
          class="preview-img"
          show-menu-by-longpress
        />
        <video
          v-else
          :src="mediaUrl"
          class="preview-video"
          controls
          autoplay
          :show-fullscreen-btn="true"
          :enable-play-gesture="true"
        />
      </view>

      <view class="action-bar">
        <view class="action-btn" :class="{ liked }" @click="handleLike">
          <text>{{ liked ? '❤️' : '🤍' }}</text>
          <text>{{ likesCount }}</text>
        </view>
        <view class="action-btn" @click="handleShare">🔗 分享</view>
      </view>

      <view class="comments-section">
        <view class="comment-input">
          <input v-model="newComment" placeholder="写评论..." maxlength="500" confirm-type="send" @confirm="handleComment" />
          <button class="send-btn" :disabled="!newComment.trim()" @click="handleComment">发送</button>
        </view>
        <view v-if="comments.length === 0" class="no-comments">暂无评论</view>
        <CommentItem
          v-for="c in comments"
          :key="c.id"
          :comment="c"
          :is-owner="c.user_id === currentUserId"
          @delete="handleDeleteComment"
        />
      </view>
    </template>
  </view>
</template>

<script>
import { fetchMediaItem, toggleLike, fetchComments, addComment, deleteComment } from '../../api/media'
import { MEDIA_URL } from '../../utils/constants'
import CommentItem from '../../components/CommentItem.vue'

export default {
  components: { CommentItem },
  data() {
    return {
      media: null,
      liked: false,
      likesCount: 0,
      comments: [],
      newComment: '',
      loading: true,
      currentUserId: 0,
    }
  },
  computed: {
    mediaUrl() {
      return this.media ? MEDIA_URL(this.media.file_key) : ''
    },
  },
  onLoad(options) {
    this.mediaId = Number(options.mediaId)
  },
  onShow() {
    if (this.mediaId) this.load()
  },
  methods: {
    async load() {
      this.loading = true
      try {
        this.media = await fetchMediaItem(this.mediaId)
        this.likesCount = this.media.likes_count
        const key = `liked_${this.media.id}`
        this.liked = uni.getStorageSync(key) === '1'
        this.comments = await fetchComments(this.mediaId)
        const token = uni.getStorageSync('token') || ''
        // extract user id from token if possible — for now use 0
        this.currentUserId = 0
      } catch {
        uni.showToast({ title: '加载失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    async handleLike() {
      const newLiked = !this.liked
      try {
        const res = await toggleLike(this.media.id, newLiked)
        this.likesCount = res.likes_count
        this.liked = newLiked
        uni.setStorageSync(`liked_${this.media.id}`, newLiked ? '1' : '0')
      } catch {
        uni.showToast({ title: '操作失败', icon: 'none' })
      }
    },
    async handleComment() {
      if (!this.newComment.trim()) return
      try {
        const c = await addComment(this.media.id, this.newComment.trim())
        this.comments.unshift(c)
        this.newComment = ''
      } catch {
        uni.showToast({ title: '发送失败', icon: 'none' })
      }
    },
    async handleDeleteComment(id) {
      try {
        await deleteComment(id)
        this.comments = this.comments.filter((c) => c.id !== id)
      } catch {
        uni.showToast({ title: '删除失败', icon: 'none' })
      }
    },
    handleShare() {
      uni.setClipboardData({
        data: this.mediaUrl,
        success: () => uni.showToast({ title: '链接已复制', icon: 'success' }),
      })
    },
  },
}
</script>

<style scoped>
.page {
  padding-bottom: 24px;
}
.loading {
  text-align: center;
  padding: 64px 16px;
  color: #999;
}
.media-area {
  background: #000;
  display: flex;
  justify-content: center;
}
.preview-img {
  width: 100%;
}
.preview-video {
  width: 100%;
  max-height: 60vh;
}
.action-bar {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
}
.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
  font-size: 14px;
}
.action-btn.liked {
  background: #fef2f2;
  border-color: #f43f5e;
  color: #f43f5e;
}
.comments-section {
  padding: 0 16px;
}
.comment-input {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.comment-input input {
  flex: 1;
  height: 36px;
  border: 1px solid #e0e0e0;
  border-radius: 18px;
  padding: 0 14px;
  font-size: 14px;
}
.send-btn {
  height: 36px;
  padding: 0 16px;
  border-radius: 18px;
  background: #4caf50;
  color: #fff;
  font-size: 14px;
  line-height: 36px;
  border: none;
}
.send-btn[disabled] {
  opacity: 0.5;
}
.no-comments {
  text-align: center;
  padding: 24px;
  color: #bbb;
  font-size: 13px;
}
</style>
