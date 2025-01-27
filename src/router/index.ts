import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import IndexView from '@/views/IndexView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/LoginView.vue')
    },
    {
      path: '/',
      name: '',
      component: AppLayout,
      children: [
        {
          path: "",
          component: IndexView

        },
        {
          path: '/TeachingAuto',
          name: 'TeachingAuto',
          component: () => import('@/views/TeachingAuto/TeachingAuto.vue')
        },
        {
          path: '/Record',
          name: 'Record',
          component: () => import('@/views/Record/Record.vue')
        },
        {
          path: '/StudentAnalysis',
          name: 'StudentAnalysis',
          component: () => import('@/views/StudentAnalysis/StudentAnalysis.vue')
        },
      ]
    }
  ]
})
export default router
