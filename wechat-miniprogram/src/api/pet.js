import { get } from './request'

export async function fetchPets() {
  return get('/pets')
}

export async function fetchPet(id) {
  return get(`/pets/${id}`)
}
