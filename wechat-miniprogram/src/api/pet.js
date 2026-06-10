import { get, post } from './request'

export async function fetchPets() {
  return get('/pets')
}

export async function fetchPet(id) {
  return get(`/pets/${id}`)
}

export async function createPet(data) {
  return post('/pets', data)
}
