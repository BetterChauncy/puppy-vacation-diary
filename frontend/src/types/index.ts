export interface Pet {
  id: number
  name: string
  species: string
  gender: string
  age: number
  avatar: string | null
  address: string | null
  birthday: string | null
  bio: string | null
  is_homepage: boolean
}

export interface PetFormData {
  name: string
  species: string
  gender: string
  age: number
  avatar?: string | null
  address?: string | null
  birthday?: string | null
  bio?: string | null
  is_homepage?: boolean
}

export interface Media {
  id: number
  pet_id: number
  media_type: 'photo' | 'video'
  file_key: string
  thumbnail_key: string | null
  original_filename: string
  file_size: number
  mime_type: string
  likes_count: number
  created_at: string
}

export interface Comment {
  id: number
  media_id: number
  content: string
  created_at: string
}

export interface AppConfig {
  app_name: string
  homepage_pet_id: number | null
  homepage_pet_ids: number[]
  homepage_rotation: 'daily' | 'hourly'
}
