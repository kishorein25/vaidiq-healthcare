import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const isAuthenticated = ref(!!token.value)

  const login = (userData, accessToken) => {
    user.value = userData
    token.value = accessToken
    isAuthenticated.value = true
    localStorage.setItem('access_token', accessToken)
  }

  const logout = () => {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem('access_token')
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
  }
})
