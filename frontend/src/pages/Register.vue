<template>
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-block w-16 h-16 bg-primary-600 rounded-lg flex items-center justify-center mb-4">
          <span class="text-3xl font-bold text-white">V</span>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">VaidiQ</h1>
        <p class="text-gray-600 mt-2">Register to Get Started</p>
      </div>

      <!-- Register Form -->
      <form @submit.prevent="handleRegister" class="bg-white rounded-2xl shadow-xl p-8 space-y-4">
        <div>
          <label class="form-label">Full Name</label>
          <input
            v-model="form.full_name"
            type="text"
            placeholder="Enter your full name"
            class="input-field"
            required
          />
        </div>

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
          <label class="form-label">Phone Number</label>
          <input
            v-model="form.phone"
            type="tel"
            placeholder="9876543210"
            class="input-field"
            required
          />
        </div>

        <div>
          <label class="form-label">Role</label>
          <select v-model="form.role" class="input-field" required>
            <option value="">Select your role</option>
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div>
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Min 8 characters"
            class="input-field"
            required
          />
        </div>

        <button type="submit" class="btn-primary w-full text-lg py-3">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>

        <p class="text-center text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-primary-600 font-medium hover:text-primary-700">
            Login here
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

export default defineComponent({
  name: 'Register',
  setup() {
    const router = useRouter()
    const form = ref({ full_name: '', email: '', phone: '', role: '', password: '' })
    const loading = ref(false)

    const handleRegister = async () => {
      loading.value = true
      try {
        await api.post('/auth/register', form.value)
        alert('Registration successful! Please login.')
        router.push('/login')
      } catch (error) {
        alert('Registration failed: ' + error.response?.data?.message || error.message)
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      handleRegister,
    }
  },
})
</script>
