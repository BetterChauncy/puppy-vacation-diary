<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { mediaUrl, toggleLike, fetchComments, addComment, deleteComment } from '../api'
import type { Comment, Media } from '../types'

const props = defineProps<{ media: Media | null }>()
const emit = defineEmits<{ close: [] }>()

const liked = ref(false)
const likesCount = ref(0)
const comments = ref<Comment[]>([])
const newComment = ref('')

watch(
  () => props.media,
  async (m) => {
    if (!m) return
    likesCount.value = m.likes_count
    liked.value = localStorage.getItem(`liked_${m.id}`) === '1'
    comments.value = await fetchComments(m.id)
    newComment.value = ''
  },
  { immediate: true },
)

async function handleLike() {
  if (!props.media) return
  const newLiked = !liked.value
  const { likes_count } = await toggleLike(props.media.id, newLiked)
  likesCount.value = likes_count
  liked.value = newLiked
  localStorage.setItem(`liked_${props.media.id}`, liked.value ? '1' : '0')
}

async function handleComment() {
  if (!props.media || !newComment.value.trim()) return
  const c = await addComment(props.media.id, newComment.value.trim())
  comments.value.unshift(c)
  newComment.value = ''
}

async function handleDeleteComment(id: number) {
  await deleteComment(id)
  comments.value = comments.value.filter((c) => c.id !== id)
}

function handleShare() {
  if (!props.media) return
  const url = `${window.location.origin}${mediaUrl(props.media.file_key)}`
  navigator.clipboard.writeText(url).catch(() => {})
  alert('链接已复制！')
}

function onBackdrop(e: MouseEvent) {
  if ((e.target as HTMLElement).classList.contains('preview-backdrop')) {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') emit('close')
  })
})
</script>

<template>
  <Teleport to="body">
    <div v-if="media" class="preview-backdrop" @click="onBackdrop">
      <div class="preview-overlay">
        <div class="preview-main">
          <button class="close-btn" @click="emit('close')">✕</button>

          <div class="media-area">
            <img
              v-if="media.media_type === 'photo'"
              :src="mediaUrl(media.file_key)"
              class="preview-img"
              alt=""
            />
            <video
              v-else
              :src="mediaUrl(media.file_key)"
              class="preview-video"
              controls
              autoplay
            />
          </div>

          <div class="action-bar">
            <button class="action-btn" :class="{ liked }" @click="handleLike">
              {{ liked ? '❤️' : '🤍' }} {{ likesCount }}
            </button>
            <a
              :href="mediaUrl(media.file_key)"
              :download="media.original_filename"
              class="action-btn"
            >
              ⬇️ 下载
            </a>
            <button class="action-btn" @click="handleShare">🔗 分享</button>
          </div>

          <div class="comments-section">
            <form class="comment-form" @submit.prevent="handleComment">
              <input
                v-model="newComment"
                placeholder="写评论..."
                maxlength="500"
              />
              <button type="submit" :disabled="!newComment.trim()" class="btn btn-primary btn-sm">
                发送
              </button>
            </form>
            <div v-if="comments.length === 0" class="no-comments">暂无评论</div>
            <div v-for="c in comments" :key="c.id" class="comment-item">
              <p class="comment-text">{{ c.content }}</p>
              <div class="comment-meta">
                <span class="comment-time">{{ c.created_at.slice(0, 16) }}</span>
                <button class="del-comment" @click="handleDeleteComment(c.id)">删除</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.preview-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}
.preview-overlay {
  background: var(--card);
  border-radius: 16px;
  max-width: 640px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}
.preview-main {
  padding: 16px;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}
.media-area {
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
  background: #000;
}
.preview-img {
  width: 100%;
  display: block;
}
.preview-video {
  width: 100%;
  display: block;
  max-height: 60vh;
}
.action-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--card);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: inherit;
}
.action-btn:hover {
  background: var(--bg);
  border-color: var(--primary);
}
.action-btn.liked {
  background: #fef2f2;
  border-color: #f43f5e;
  color: #f43f5e;
}
.comments-section {
  border-top: 1px solid var(--border);
  padding-top: 12px;
}
.comment-form {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.comment-form input {
  flex: 1;
}
.no-comments {
  text-align: center;
  color: var(--text-secondary);
  font-size: 13px;
  padding: 16px;
}
.comment-item {
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
}
.comment-item:last-child {
  border-bottom: none;
}
.comment-text {
  font-size: 14px;
  margin-bottom: 4px;
}
.comment-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--text-secondary);
}
.del-comment {
  border: none;
  background: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 11px;
}
.del-comment:hover {
  text-decoration: underline;
}
</style>
