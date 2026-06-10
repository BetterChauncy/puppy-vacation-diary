const DEV = true
const DEV_URL = 'http://localhost:8000'
const PROD_URL = 'https://your-production-domain.com'

export const BASE_URL = DEV ? DEV_URL : PROD_URL
export const MEDIA_URL = (key) => `${BASE_URL}/uploads/${key}`
