<template>
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-block w-16 h-16 bg-primary-600 rounded-lg flex items-center justify-center mb-4">
          <span class="text-3xl font-bold text-white">V</span>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">VaidiQ</h1>
        <p class="text-gray-600 mt-2">Healthcare Clinic Management</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="bg-white rounded-2xl shadow-xl p-8 space-y-6">
        <div>
          <label class="form-label">Email Address</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="Enter your email"
            class="input-field"
            required
          />
        </div>

        <div>
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            class="input-field"
            required
          />
        </div>

        <button type="submit" class="btn-primary w-full text-lg py-3">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>

        <p class="text-center text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-primary-600 font-medium hover:text-primary-700">
            Register here
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import api from '../services/api'

export default defineComponent({
  name: 'Login',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const form = ref({ email: '', password: '' })
    const loading = ref(false)

    const handleLogin = async () => {
      loading.value = true
      try {
        const response = await api.post('/auth/login', form.value)
        const { access_token, user } = response.data.data
        authStore.login(user, access_token)
        router.push(`/${user.role}`)
      } catch (error) {
        alert('Login failed: ' + error.response?.data?.message || error.message)
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      handleLogin,
    }
  },
})
</script>
