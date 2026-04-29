<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">Book Appointment</h1>
    <p class="text-gray-600 mb-8">Schedule your consultation with our doctors</p>

    <div class="max-w-2xl">
      <form @submit.prevent="handleBookAppointment" class="card space-y-6">
        <!-- Select Doctor -->
        <div>
          <label class="form-label">Select Doctor</label>
          <select v-model="form.doctor_id" class="input-field" required>
            <option value="">-- Choose a doctor --</option>
            <option value="1">Dr. Rajesh Kumar - Cardiology</option>
            <option value="2">Dr. Priya Sharma - Neurology</option>
            <option value="3">Dr. Amit Patel - Orthopedics</option>
          </select>
        </div>

        <!-- Date & Time -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="form-label">Appointment Date</label>
            <input v-model="form.appointment_date" type="date" class="input-field" required />
          </div>
          <div>
            <label class="form-label">Appointment Time</label>
            <input v-model="form.appointment_time" type="time" class="input-field" required />
          </div>
        </div>

        <!-- Reason -->
        <div>
          <label class="form-label">Reason for Visit</label>
          <textarea
            v-model="form.reason"
            placeholder="Describe your symptoms or reason for consultation"
            rows="4"
            class="input-field"
            required
          ></textarea>
        </div>

        <!-- Buttons -->
        <div class="flex gap-4">
          <button type="submit" class="btn-primary flex-1">
            {{ loading ? 'Booking...' : 'Book Appointment' }}
          </button>
          <router-link to="/patient" class="btn-secondary flex-1 text-center">
            Cancel
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { ref } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Appointment',
  setup() {
    const router = useRouter()
    const form = ref({
      doctor_id: '',
      appointment_date: '',
      appointment_time: '',
      reason: '',
    })
    const loading = ref(false)

    const handleBookAppointment = async () => {
      loading.value = true
      try {
        await api.post('/appointment/book', form.value)
        alert('Appointment booked successfully!')
        router.push('/patient')
      } catch (error) {
        alert('Failed to book appointment: ' + error.response?.data?.message || error.message)
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      handleBookAppointment,
    }
  },
})
</script>
