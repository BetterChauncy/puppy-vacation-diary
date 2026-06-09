import { get } from './request'

export async function fetchConfig() {
  return get('/config')
}
