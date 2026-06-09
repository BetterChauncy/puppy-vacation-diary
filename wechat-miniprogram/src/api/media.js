import { BASE_URL } from '../utils/constants'
import { get, post, del } from './request'

function getToken() {
  return uni.getStorageSync('token') || ''
}

export async function fetchMedia(petId, limit = 20, offset = 0) {
  return get(`/pets/${petId}/media?limit=${limit}&offset=${offset}`)
}

export async function fetchMediaItem(mediaId) {
  return get(`/media/${mediaId}`)
}

export async function toggleLike(mediaId, liked) {
  return post(`/media/${mediaId}/like?liked=${liked}`)
}

export async function fetchComments(mediaId) {
  return get(`/media/${mediaId}/comments`)
}

export async function addComment(mediaId, content) {
  return post(`/media/${mediaId}/comments`, { content })
}

export async function deleteComment(commentId) {
  return del(`/media/comments/${commentId}`)
}
