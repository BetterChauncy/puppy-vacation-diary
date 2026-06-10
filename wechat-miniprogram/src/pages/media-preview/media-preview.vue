<template>
  <view class="fullscreen">
    <view v-if="loading" class="state-overlay">
      <text>加载中...</text>
    </view>
    <view v-else-if="error" class="state-overlay error">
      <text>加载失败</text>
      <button class="retry-btn" @click="load">重试</button>
    </view>
    <view v-else-if="!petMedia.length" class="state-overlay">
      <text>暂无内容</text>
    </view>
    <template v-else>
      <swiper
        vertical
        :current="currentIndex"
        class="swiper"
        @change="onSwiperChange"
      >
        <swiper-item
          v-for="(item, idx) in petMedia"
          :key="item.id"
          class="swiper-item"
        >
          <image
            v-if="item.media_type === 'photo'"
            :src="mediaUrl(item.file_key)"
            mode="aspectFill"
            class="media-full"
            show-menu-by-longpress
          />
          <video
            v-else
            :id="'v-' + item.id"
            :src="mediaUrl(item.file_key)"
            :poster="item.thumbnail_key ? mediaUrl(item.thumbnail_key) : ''"
            class="media-full video-full"
            object-fit="cover"
            :controls="false"
            :show-center-play-btn="true"
            :enable-progress-gesture="true"
            :show-fullscreen-btn="false"
            @tap="toggleVideoPlay(idx)"
            @ended="onVideoEnded"
          />
        </swiper-item>
      </swiper>

      <view class="right-actions">
        <view class="action-btn" hover-class="btn-press" @click="handleLike">
          <text class="action-icon" :class="{ 'heart-pop': heartAnimating }">{{ isLiked ? '❤️' : '🤍' }}</text>
          <text class="action-count">{{ currentItemLikes }}</text>
        </view>
        <view class="action-btn" hover-class="btn-press" @click="openComment">
          <text class="action-icon">💬</text>
          <text class="action-count">{{ commentCount }}</text>
        </view>
        <view class="action-btn" hover-class="btn-press" @click="handleShare">
          <text class="action-icon">•••</text>
        </view>
      </view>

      <view class="top-bar">
        <text class="back-btn" @click="goBack">←</text>
        <text class="counter">{{ currentIndex + 1 }} / {{ petMedia.length }}</text>
      </view>
    </template>

    <view
      v-if="showComment"
      class="comment-mask"
      :class="{ active: maskAnim }"
      @click="closeComment"
    >
      <view class="comment-sheet" @click.stop>
        <view class="comment-header">
          <text class="comment-title">评论 {{ commentCount }}</text>
          <text class="comment-close" @click="closeComment">✕</text>
        </view>
        <scroll-view scroll-y class="comment-list">
          <view v-for="c in comments" :key="c.id" class="comment-item">
            <text class="comment-user">{{ c.user?.nickname || '匿名' }}</text>
            <text class="comment-text">{{ c.content }}</text>
            <text v-if="c.user?.id === currentUserId" class="comment-del" @click="handleDeleteComment(c.id)">删除</text>
          </view>
          <view v-if="comments.length === 0 && !commentsLoading" class="no-comments">暂无评论</view>
          <view v-if="commentsLoading" class="no-comments">加载中...</view>
        </scroll-view>
        <view class="comment-input-row">
          <input
            v-model="newComment"
            placeholder="写评论..."
            maxlength="500"
            confirm-type="send"
            class="comment-input"
            @confirm="handleComment"
          />
          <button
            class="send-btn"
            :disabled="!newComment.trim() || commentSending"
            @click="handleComment"
          >{{ commentSending ? '...' : '发送' }}</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { fetchMediaItem, fetchMedia, toggleLike, fetchComments, addComment, deleteComment } from '../../api/media'
import { MEDIA_URL } from '../../utils/constants'

export default {
  components: {},
  data() {
    return {
      mediaId: 0,
      petId: 0,
      petMedia: [],
      currentIndex: 0,
      likedMap: {},
      heartAnimating: false,
      loading: true,
      error: false,
      showComment: false,
      maskAnim: false,
      comments: [],
      commentCount: 0,
      newComment: '',
      commentsLoading: false,
      commentSending: false,
      currentUserId: 0,
      commentMediaId: 0,
      autoAdvancing: false,
    }
  },
  computed: {
    currentItem() {
      return this.petMedia[this.currentIndex] || null
    },
    currentItemLikes() {
      return this.currentItem?.likes_count ?? 0
    },
    isLiked() {
      return !!this.likedMap[this.currentItem?.id]
    },
  },
  onLoad(options) {
    this.mediaId = Number(options.mediaId)
    this.petId = Number(options.petId || 0)
  },
  onShow() {
    if (this.mediaId) this.load()
  },
  onUnload() {
    this._cleanupVideos()
  },
  onShareAppMessage() {
    const item = this.currentItem
    if (!item) return {}
    return {
      title: '来看看我家小狗的照片！',
      imageUrl: item.thumbnail_key ? this.mediaUrl(item.thumbnail_key) : '',
      path: `/pages/media-preview/media-preview?mediaId=${item.id}&petId=${this.petId}`,
    }
  },
  onShareTimeline() {
    const item = this.currentItem
    if (!item) return {}
    return {
      title: '来看看我家小狗的照片！',
      imageUrl: item.thumbnail_key ? this.mediaUrl(item.thumbnail_key) : '',
    }
  },
  methods: {
    mediaUrl(key) {
      return MEDIA_URL(key)
    },
    async load() {
      this.loading = true
      this.error = false
      try {
        const item = await fetchMediaItem(this.mediaId)
        const pid = this.petId || item.pet_id
        const [mediaRes, initialComments] = await Promise.all([
          fetchMedia(pid, 100, 0),
          fetchComments(this.mediaId),
        ])
        this.petMedia = mediaRes.items || mediaRes
        this.comments = initialComments
        this.commentCount = initialComments.length

        this.likedMap = {}
        for (const m of this.petMedia) {
          const k = `liked_${m.id}`
          this.$set(this.likedMap, m.id, uni.getStorageSync(k) === '1')
        }

        const idx = this.petMedia.findIndex((m) => m.id === this.mediaId)
        this.currentIndex = idx >= 0 ? idx : 0
        this.currentUserId = 0

        this.$nextTick(() => {
          if (this.currentItem?.media_type === 'video') {
            setTimeout(() => {
              const ctx = uni.createVideoContext('v-' + this.currentItem.id, this)
              if (ctx) ctx.play()
            }, 300)
          }
        })
      } catch (e) {
        console.error('预览加载失败:', e)
        this.error = true
      } finally {
        this.loading = false
      }
    },
    onSwiperChange(e) {
      if (this.autoAdvancing) {
        this.autoAdvancing = false
        return
      }
      const prevIdx = this.currentIndex
      const curIdx = e.detail.current
      this.currentIndex = curIdx

      const prev = this.petMedia[prevIdx]
      if (prev?.media_type === 'video') {
        const ctx = uni.createVideoContext('v-' + prev.id, this)
        if (ctx) ctx.pause()
      }

      this.$nextTick(() => {
        const cur = this.petMedia[curIdx]
        if (cur?.media_type === 'video') {
          setTimeout(() => {
            const ctx = uni.createVideoContext('v-' + cur.id, this)
            if (ctx) ctx.play()
          }, 100)
        }
      })
    },
    onVideoEnded() {
      const next = this.currentIndex + 1
      if (next >= this.petMedia.length) return
      this.autoAdvancing = true
      this.currentIndex = next
      this.$nextTick(() => {
        const cur = this.petMedia[next]
        if (cur?.media_type === 'video') {
          setTimeout(() => {
            const ctx = uni.createVideoContext('v-' + cur.id, this)
            if (ctx) ctx.play()
          }, 300)
        }
      })
    },
    toggleVideoPlay(idx) {
      const item = this.petMedia[idx]
      if (!item || item.media_type !== 'video') return
      const ctx = uni.createVideoContext('v-' + item.id, this)
      if (!ctx) return
      ctx.play()
    },
    async handleLike() {
      const item = this.currentItem
      if (!item) return
      const newLiked = !this.isLiked
      const delta = newLiked ? 1 : -1

      this.likedMap[item.id] = newLiked
      item.likes_count += delta
      if (newLiked) {
        this.heartAnimating = true
        setTimeout(() => { this.heartAnimating = false }, 400)
      }

      try {
        const res = await toggleLike(item.id, newLiked)
        item.likes_count = res.likes_count
        uni.setStorageSync(`liked_${item.id}`, newLiked ? '1' : '0')
      } catch (e) {
        console.error('点赞失败:', e)
        this.likedMap[item.id] = !newLiked
        item.likes_count -= delta
        uni.showToast({ title: '操作失败', icon: 'none' })
      }
    },
    async openComment() {
      const item = this.currentItem
      if (!item) return
      this.commentMediaId = item.id
      this.showComment = true
      this.$nextTick(() => { this.maskAnim = true })
      this.commentsLoading = true
      try {
        if (item.id !== this.commentMediaId) {
          this.comments = await fetchComments(item.id)
        } else {
          const fresh = await fetchComments(item.id)
          this.comments = fresh
        }
        this.commentCount = this.comments.length
      } catch (e) {
        console.error('获取评论失败:', e)
        uni.showToast({ title: '获取评论失败', icon: 'none' })
      } finally {
        this.commentsLoading = false
      }
    },
    closeComment() {
      this.maskAnim = false
      setTimeout(() => {
        this.showComment = false
        this.newComment = ''
      }, 250)
    },
    async handleComment() {
      if (!this.newComment.trim() || this.commentSending) return
      this.commentSending = true
      try {
        const c = await addComment(this.commentMediaId, this.newComment.trim())
        this.comments.unshift(c)
        this.commentCount = this.comments.length
        this.newComment = ''
      } catch (e) {
        console.error('评论失败:', e)
        uni.showToast({ title: '发送失败', icon: 'none' })
      } finally {
        this.commentSending = false
      }
    },
    async handleDeleteComment(id) {
      try {
        await deleteComment(id)
        this.comments = this.comments.filter((c) => c.id !== id)
        this.commentCount = this.comments.length
      } catch (e) {
        console.error('删除评论失败:', e)
        uni.showToast({ title: '删除失败', icon: 'none' })
      }
    },
    handleShare() {
      const item = this.currentItem
      if (!item) return
      uni.showActionSheet({
        itemList: ['分享给朋友', '分享到朋友圈', '复制链接'],
        success: (res) => {
          if (res.tapIndex === 0) {
            uni.showToast({ title: '点击右上角 ··· 分享', icon: 'none' })
          } else if (res.tapIndex === 1) {
            uni.showToast({ title: '点击右上角 ··· 分享到朋友圈', icon: 'none' })
          } else if (res.tapIndex === 2) {
            uni.setClipboardData({
              data: this.mediaUrl(item.file_key),
              success: () => uni.showToast({ title: '链接已复制', icon: 'success' }),
            })
          }
        },
      })
    },
    goBack() {
      uni.navigateBack()
    },
    _cleanupVideos() {
      for (const item of this.petMedia) {
        if (item.media_type === 'video') {
          const ctx = uni.createVideoContext('v-' + item.id, this)
          if (ctx) ctx.stop()
        }
      }
    },
  },
}
</script>

<style scoped>
.fullscreen {
  width: 100vw;
  height: 100vh;
  background: #000;
  overflow: hidden;
  position: relative;
}

.state-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 14px;
}
.state-overlay.error {
  color: #ef4444;
}
.retry-btn {
  margin-top: 12px;
  padding: 6px 20px;
  border-radius: 16px;
  border: 1px solid #ef4444;
  color: #ef4444;
  background: transparent;
  font-size: 13px;
}

.swiper {
  width: 100%;
  height: 100%;
}
.swiper-item {
  width: 100%;
  height: 100%;
}
.media-full {
  width: 100%;
  height: 100%;
}

/* ── Right-edge TikTok actions ── */
.right-actions {
  position: absolute;
  right: 12px;
  bottom: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 22px;
  z-index: 10;
}
.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 4px;
  -webkit-tap-highlight-color: transparent;
}
.action-icon {
  font-size: 28px;
  color: #fff;
  text-shadow: 0 2px 6px rgba(0,0,0,0.4);
  transition: transform 0.15s ease;
}
.action-count {
  font-size: 11px;
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.4);
}
.btn-press {
  transform: scale(0.82);
  transition: transform 0.08s;
}

/* ── Heart pop animation (TikTok-style) ── */
@keyframes heartPop {
  0%   { transform: scale(1); }
  25%  { transform: scale(1.35); }
  50%  { transform: scale(1); }
  75%  { transform: scale(1.15); }
  100% { transform: scale(1); }
}
.heart-pop {
  animation: heartPop 0.4s cubic-bezier(0.2, 0, 0, 1);
}

/* ── Top bar ── */
.top-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 48px 16px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
  background: linear-gradient(to bottom, rgba(0,0,0,0.45), transparent);
}
.back-btn {
  font-size: 22px;
  color: #fff;
  padding: 4px 8px;
}
.counter {
  font-size: 13px;
  color: rgba(255,255,255,0.8);
}

/* ── Comment bottom sheet ── */
.comment-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 100;
  display: flex;
  align-items: flex-end;
  opacity: 0;
  transition: opacity 0.25s ease;
}
.comment-mask.active {
  opacity: 1;
}
.comment-sheet {
  width: 100%;
  max-height: 70vh;
  background: #1c1c1e;
  border-radius: 16px 16px 0 0;
  display: flex;
  flex-direction: column;
  transform: translateY(100%);
  transition: transform 0.25s ease;
}
.comment-mask.active .comment-sheet {
  transform: translateY(0);
}
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #333;
}
.comment-title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}
.comment-close {
  font-size: 18px;
  color: #999;
  padding: 4px;
}
.comment-list {
  flex: 1;
  padding: 12px 16px;
  max-height: 40vh;
}
.comment-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 0;
  border-bottom: 1px solid #2c2c2e;
}
.comment-user {
  font-size: 13px;
  color: #8e8e93;
  white-space: nowrap;
  flex-shrink: 0;
}
.comment-text {
  font-size: 14px;
  color: #fff;
  flex: 1;
  word-break: break-word;
}
.comment-del {
  font-size: 12px;
  color: #ef4444;
  flex-shrink: 0;
  padding: 2px 6px;
}
.no-comments {
  text-align: center;
  padding: 24px 0;
  color: #666;
  font-size: 13px;
}
.comment-input-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-top: 1px solid #333;
}
.comment-input {
  flex: 1;
  height: 36px;
  border: 1px solid #3a3a3c;
  border-radius: 18px;
  padding: 0 14px;
  font-size: 14px;
  color: #fff;
  background: #2c2c2e;
}
.send-btn {
  height: 36px;
  padding: 0 16px;
  border-radius: 18px;
  background: #007aff;
  color: #fff;
  font-size: 14px;
  line-height: 36px;
  border: none;
  flex-shrink: 0;
}
.send-btn[disabled] {
  opacity: 0.4;
}
</style>
