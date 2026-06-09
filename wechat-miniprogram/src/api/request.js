import { BASE_URL } from '../utils/constants'

function getToken() {
  return uni.getStorageSync('token') || ''
}

async function request(method, path, data = null, options = {}) {
  const url = BASE_URL + path
  const token = getToken()
  const header = { 'Content-Type': 'application/json' }
  if (token) header['Authorization'] = `Bearer ${token}`

  return new Promise((resolve, reject) => {
    uni.request({
      url,
      method,
      data,
      header,
      timeout: options.timeout || 15000,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 204) {
          resolve(null)
        } else {
          const detail = res.data?.detail || `请求失败 (${res.statusCode})`
          reject(new Error(detail))
        }
      },
      fail: (err) => {
        reject(new Error('网络异常'))
      },
    })
  })
}

export const get = (path, options) => request('GET', path, null, options)
export const post = (path, data, options) => request('POST', path, data, options)
export const put = (path, data, options) => request('PUT', path, data, options)
export const del = (path, options) => request('DELETE', path, null, options)
