<template>
  <div class="card text-center">
    <div :class="color" class="w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
      <component :is="icon" class="w-6 h-6" />
    </div>
    <p class="text-gray-600 text-sm font-medium">{{ title }}</p>
    <p class="text-3xl font-bold text-gray-900 mt-2">{{ value }}</p>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { UserGroupIcon, UserIcon, CalendarIcon, CurrencyRupeeIcon } from '@heroicons/vue/24/outline'

export default defineComponent({
  name: 'StatCard',
  components: {
    UserGroupIcon,
    UserIcon,
    CalendarIcon,
    CurrencyRupeeIcon,
  },
  props: {
    title: String,
    value: String,
    icon: String,
    color: String,
  },
})
</script>
