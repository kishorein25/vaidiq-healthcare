import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/Register.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../pages/admin/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' },
  },
  {
    path: '/doctor',
    name: 'DoctorDashboard',
    component: () => import('../pages/doctor/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'doctor' },
  },
  {
    path: '/patient',
    name: 'PatientDashboard',
    component: () => import('../pages/patient/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'patient' },
  },
  {
    path: '/appointment',
    name: 'Appointment',
    component: () => import('../pages/Appointment.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/queue',
    name: 'Queue',
    component: () => import('../pages/Queue.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const requiredRole = to.meta.role

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (requiredRole && authStore.user?.role !== requiredRole) {
    next('/login')
  } else if (!requiresAuth && authStore.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
    next(`/${authStore.user?.role}`)
  } else {
    next()
  }
})

export default router
