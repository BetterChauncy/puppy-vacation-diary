import axios from 'axios'
import type { AppConfig, Comment, Media, Pet, PetFormData } from '../types'

const BASE = import.meta.env.DEV ? '/api' : ''

const http = axios.create({
  baseURL: BASE,
})

export async function fetchConfig(): Promise<AppConfig> {
  const { data } = await http.get('/config')
  return data
}

export async function updateConfig(rotation: string): Promise<void> {
  await http.put('/config', { homepage_rotation: rotation })
}

export async function fetchPets(): Promise<Pet[]> {
  const { data } = await http.get('/pets')
  return data
}

export async function fetchPet(id: number): Promise<Pet> {
  const { data } = await http.get(`/pets/${id}`)
  return data
}

export async function createPet(pet: PetFormData): Promise<Pet> {
  const { data } = await http.post('/pets', pet)
  return data
}

export async function updatePet(id: number, pet: Partial<PetFormData>): Promise<Pet> {
  const { data } = await http.put(`/pets/${id}`, pet)
  return data
}

export async function deletePet(id: number): Promise<void> {
  await http.delete(`/pets/${id}`)
}

export async function fetchMedia(petId: number): Promise<Media[]> {
  const { data } = await http.get(`/pets/${petId}/media`)
  return data.items
}

export async function fetchMediaItem(id: number): Promise<Media> {
  const { data } = await http.get(`/media/${id}`)
  return data
}

export async function uploadMedia(
  petId: number,
  files: File[],
  onProgress?: (pct: number) => void,
): Promise<Media[]> {
  const form = new FormData()
  files.forEach((f) => form.append('files', f))
  const { data } = await http.post(`/pets/${petId}/media`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress(e) {
      if (e.total && onProgress) onProgress(Math.round((e.loaded / e.total) * 100))
    },
  })
  return data
}

export async function deleteMedia(id: number): Promise<void> {
  await http.delete(`/media/${id}`)
}

export async function toggleLike(mediaId: number, liked: boolean): Promise<{ likes_count: number }> {
  const { data } = await http.post(`/media/${mediaId}/like?liked=${liked}`)
  return data
}

export async function fetchComments(mediaId: number): Promise<Comment[]> {
  const { data } = await http.get(`/media/${mediaId}/comments`)
  return data
}

export async function addComment(mediaId: number, content: string): Promise<Comment> {
  const { data } = await http.post(`/media/${mediaId}/comments`, { content })
  return data
}

export async function deleteComment(commentId: number): Promise<void> {
  await http.delete(`/media/comments/${commentId}`)
}

export function mediaUrl(key: string): string {
  return `/uploads/${key}`
}
