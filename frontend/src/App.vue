<template>
  <div id="app" class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <Sidebar v-if="isAuthenticated" :user="currentUser" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Navbar -->
      <Navbar v-if="isAuthenticated" :user="currentUser" />

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

export default defineComponent({
  name: 'App',
  components: {
    Sidebar,
    Navbar,
  },
  computed: {
    isAuthenticated() {
      return this.authStore.isAuthenticated
    },
    currentUser() {
      return this.authStore.user
    },
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
})
</script>
