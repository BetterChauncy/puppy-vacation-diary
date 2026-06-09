<script>
import { wxLogin } from './api/auth'

export default {
  globalData: {
    user: null,
  },
  onLaunch() {
    this.doLogin()
  },
  methods: {
    async doLogin() {
      const token = uni.getStorageSync('token')
      if (token) return
      try {
        const { token: newToken } = await wxLogin()
        uni.setStorageSync('token', newToken)
      } catch {
        console.warn('login failed')
      }
    },
  },
}
</script>

<style>
@import './uni.scss';
</style>
