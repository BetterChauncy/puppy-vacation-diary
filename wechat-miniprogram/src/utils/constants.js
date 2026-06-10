const DEV = false
const DEV_URL = 'http://localhost:8000'
const PROD_URL = 'https://puddy-2117605-1313120572.ap-shanghai.run.tcloudbase.com'

export const BASE_URL = DEV ? DEV_URL : PROD_URL
export const MEDIA_URL = (key) => `${BASE_URL}/uploads/${key}`
