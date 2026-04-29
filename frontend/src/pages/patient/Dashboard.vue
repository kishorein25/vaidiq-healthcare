<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">My Appointments</h1>
    <p class="text-gray-600 mb-8">Welcome, {{ user?.full_name }}!</p>

    <!-- Book Appointment Button -->
    <div class="mb-8">
      <router-link to="/appointment" class="btn-primary inline-block">
        + Book New Appointment
      </router-link>
    </div>

    <!-- Appointments List -->
    <div class="space-y-4">
      <div v-for="i in 3" :key="i" class="card">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-bold text-gray-900">Dr. Rajesh Kumar</h3>
            <p class="text-gray-600">Cardiologist</p>
            <div class="mt-2 flex items-center gap-4 text-sm text-gray-500">
              <span>📅 May 15, 2026</span>
              <span>🕐 10:30 AM</span>
              <span>🏥 Room 201</span>
            </div>
          </div>
          <span class="badge badge-success">Confirmed</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '../../stores/auth'

export default defineComponent({
  name: 'PatientDashboard',
  setup() {
    const authStore = useAuthStore()

    return {
      user: authStore.user,
    }
  },
})
</script>
