<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
    <p class="text-gray-600 mb-8">Welcome back, {{ user?.full_name }}!</p>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard
        title="Total Doctors"
        value="24"
        icon="UserGroupIcon"
        color="bg-blue-100 text-blue-600"
      />
      <StatCard title="Total Patients" value="156" icon="UserIcon" color="bg-green-100 text-green-600" />
      <StatCard
        title="Appointments Today"
        value="12"
        icon="CalendarIcon"
        color="bg-yellow-100 text-yellow-600"
      />
      <StatCard title="Revenue" value="₹45,000" icon="CurrencyRupeeIcon" color="bg-purple-100 text-purple-600" />
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Appointments This Month</h2>
        <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <p class="text-gray-500">Chart will display here</p>
        </div>
      </div>
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Department Distribution</h2>
        <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <p class="text-gray-500">Chart will display here</p>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
      <div class="space-y-4">
        <div class="flex items-center justify-between py-3 border-b border-gray-200">
          <div>
            <p class="font-medium text-gray-900">New appointment booked</p>
            <p class="text-sm text-gray-500">Patient: Rajesh Kumar</p>
          </div>
          <span class="text-xs bg-primary-100 text-primary-700 px-3 py-1 rounded-full">2 mins ago</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '../../stores/auth'
import StatCard from '../../components/StatCard.vue'

export default defineComponent({
  name: 'AdminDashboard',
  components: {
    StatCard,
  },
  setup() {
    const authStore = useAuthStore()

    return {
      user: authStore.user,
    }
  },
})
</script>
