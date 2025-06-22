import router from '@/router'
import axios from 'axios'

const request = axios.create({
  baseURL: '/',
  timeout: 5000
})

// 请求拦截器：添加 access_token
request.interceptors.request.use(config => {
  const accessToken = localStorage.getItem('access_token')
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

// 响应拦截器：处理 token 过期自动刷新
let isRefreshing = false
let pendingRequests = []

request.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // 判断 access_token 是否过期
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      // 无刷新令牌，直接清除并跳转登录页
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        localStorage.clear()
        router.push('/')
        return Promise.reject(error)
      }

      // 如果已经在刷新，则把请求加入队列
      if (isRefreshing) {
        return new Promise(resolve => {
          pendingRequests.push(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(request(originalRequest))
          })
        })
      }

      isRefreshing = true

      // 尝试刷新 token
      try {
        const res = await axios.post('/api/auth/refresh', { refresh_token: refreshToken })
        const newToken = res.data.access_token

        localStorage.setItem('access_token', newToken)

        // 继续执行所有等待的请求
        pendingRequests.forEach(cb => cb(newToken))
        pendingRequests = []
        isRefreshing = false

        // 重试原始请求
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return request(originalRequest)
      } catch (refreshErr) {
        isRefreshing = false
        pendingRequests = []

        // 刷新失败，重定向到登录页
        localStorage.clear()
        router.push('/')
        return Promise.reject(refreshErr)
      }
    }

    return Promise.reject(error)
  }
)

export default request
