<template>
  <aside class="w-64 bg-gradient-to-b from-primary-700 to-primary-900 text-white shadow-lg">
    <!-- Logo -->
    <div class="p-6 border-b border-primary-600">
      <div class="flex items-center gap-2">
        <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
          <span class="text-primary-700 font-bold text-xl">V</span>
        </div>
        <div>
          <h1 class="text-xl font-bold">VaidiQ</h1>
          <p class="text-xs text-primary-200">Healthcare</p>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="p-4 space-y-2">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-primary-600 transition-colors"
        :class="{ 'bg-primary-600': isActive(item.path) }"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span class="font-medium">{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- User Info -->
    <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-primary-600 bg-primary-800">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
          <span class="text-sm font-bold">{{ user?.full_name?.charAt(0) }}</span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium truncate">{{ user?.full_name }}</p>
          <p class="text-xs text-primary-300 truncate">{{ user?.role }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'
import { HomeIcon, UserGroupIcon, UserIcon, CalendarIcon, ClipboardListIcon } from '@heroicons/vue/24/outline'

export default defineComponent({
  name: 'Sidebar',
  props: {
    user: Object,
  },
  setup() {
    const route = useRoute()

    const navItems = [
      { label: 'Dashboard', path: '/admin', icon: HomeIcon },
      { label: 'Doctors', path: '/admin/doctors', icon: UserIcon },
      { label: 'Appointments', path: '/appointment', icon: CalendarIcon },
      { label: 'Queue', path: '/queue', icon: ClipboardListIcon },
    ]

    const isActive = (path) => route.path.startsWith(path)

    return {
      navItems,
      isActive,
    }
  },
})
</script>
