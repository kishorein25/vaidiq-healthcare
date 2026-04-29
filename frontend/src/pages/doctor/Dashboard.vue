<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">Doctor Dashboard</h1>
    <p class="text-gray-600 mb-8">Welcome back, {{ user?.full_name }}!</p>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="card">
        <p class="text-gray-600 text-sm font-medium">Today's Appointments</p>
        <p class="text-4xl font-bold text-primary-600 mt-2">8</p>
      </div>
      <div class="card">
        <p class="text-gray-600 text-sm font-medium">Patients Seen</p>
        <p class="text-4xl font-bold text-green-600 mt-2">5</p>
      </div>
      <div class="card">
        <p class="text-gray-600 text-sm font-medium">Pending</p>
        <p class="text-4xl font-bold text-yellow-600 mt-2">3</p>
      </div>
    </div>

    <!-- Today's Queue -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Today's Queue</h2>
      <div class="space-y-3">
        <div v-for="i in 5" :key="i" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-primary-200 rounded-full flex items-center justify-center font-bold">{{ i }}</div>
            <div>
              <p class="font-medium text-gray-900">Patient {{ i }}</p>
              <p class="text-sm text-gray-500">Consultation</p>
            </div>
          </div>
          <button class="btn-primary text-sm">Call Patient</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '../../stores/auth'

export default defineComponent({
  name: 'DoctorDashboard',
  setup() {
    const authStore = useAuthStore()

    return {
      user: authStore.user,
    }
  },
})
</script>
