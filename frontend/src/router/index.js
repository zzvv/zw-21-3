import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user.js'

const routes = [
  { path: '/login', component: () => import('../views/Login.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'teachers', component: () => import('../views/Teachers.vue') },
      { path: 'students', component: () => import('../views/Students.vue') },
      { path: 'courses', component: () => import('../views/Courses.vue') },
      { path: 'classrooms', component: () => import('../views/Classrooms.vue') },
      { path: 'schedules', component: () => import('../views/Schedules.vue') },
      { path: 'enrollments', component: () => import('../views/Enrollments.vue') },
      { path: 'lesson-records', component: () => import('../views/LessonRecords.vue') },
      { path: 'exams', component: () => import('../views/Exams.vue') },
      { path: 'instruments', component: () => import('../views/Instruments.vue') },
      { path: 'users', component: () => import('../views/Users.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const store = useUserStore()
  if (!to.meta.public && !store.isLoggedIn) {
    return '/login'
  }
})

export default router
