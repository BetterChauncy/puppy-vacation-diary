import { post, get, put } from './request'

export async function wxLogin() {
  const { code } = await uni.login({ provider: 'weixin' })
  return post('/auth/wx-login', { code })
}

export async function getMe() {
  return get('/auth/me')
}

export async function updateProfile(nickname, avatar) {
  return put('/auth/profile', { nickname, avatar })
}
