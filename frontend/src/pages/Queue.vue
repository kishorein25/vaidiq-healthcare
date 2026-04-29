<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">Queue Status</h1>
    <p class="text-gray-600 mb-8">Check your position in the queue</p>

    <div class="max-w-2xl">
      <!-- Queue Status Card -->
      <div class="card mb-8 text-center">
        <h2 class="text-gray-600 mb-4">Currently Serving</h2>
        <p class="text-6xl font-bold text-primary-600 mb-4">Token #5</p>
        <p class="text-xl text-gray-900">Consulting Room 1</p>
      </div>

      <!-- Your Position -->
      <div class="card text-center mb-8">
        <h2 class="text-gray-600 mb-4">Your Token</h2>
        <p class="text-6xl font-bold text-green-600 mb-4">Token #12</p>
        <p class="text-2xl text-gray-900 mb-2">Position: 7th</p>
        <p class="text-lg text-gray-600">Estimated Wait: 35 minutes</p>
      </div>

      <!-- Waiting List -->
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Waiting List</h2>
        <div class="space-y-2">
          <div v-for="i in [6, 7, 8, 9, 10, 11, 12]" :key="i" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            :class="{ 'bg-primary-50 border-l-4 border-primary-600': i === 12 }">
            <span class="font-bold text-lg">Token #{{ i }}</span>
            <span v-if="i === 12" class="badge badge-info">You</span>
            <span v-else class="text-gray-600">{{ i - 5 }} ahead</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Queue',
})
</script>
