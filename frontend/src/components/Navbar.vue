<template>
  <nav class="bg-white border-b border-gray-200 shadow-sm">
    <div class="px-6 py-4 flex items-center justify-between">
      <!-- Search -->
      <div class="flex-1 max-w-md">
        <input
          type="text"
          placeholder="Search patients, doctors..."
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
      </div>

      <!-- Right Section -->
      <div class="flex items-center gap-6">
        <!-- Notifications -->
        <button class="relative text-gray-600 hover:text-gray-900">
          <BellIcon class="w-6 h-6" />
          <span class="absolute top-0 right-0 w-2 h-2 bg-healthcare-600 rounded-full"></span>
        </button>

        <!-- User Menu -->
        <div class="flex items-center gap-3 pl-6 border-l border-gray-200">
          <div class="text-right">
            <p class="text-sm font-medium text-gray-900">{{ user?.full_name }}</p>
            <p class="text-xs text-gray-500 capitalize">{{ user?.role }}</p>
          </div>
          <button @click="logout" class="text-gray-600 hover:text-gray-900">
            <ArrowRightOnRectangleIcon class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { BellIcon, ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline'

export default defineComponent({
  name: 'Navbar',
  components: {
    BellIcon,
    ArrowRightOnRectangleIcon,
  },
  props: {
    user: Object,
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    return {
      logout,
    }
  },
})
</script>
