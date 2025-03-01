import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import IndexView from '@/views/IndexView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/TestPage',
      name: 'TestPage',
      component: () => import('@/views/TestPage.vue')
    },
    {
      path: '/TestLogin',
      name: 'TestLogin',
      component: () => import('@/views/TestLogin.vue')
    },
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
          path: '/Test',
          name: 'Test',
          component: () => import('@/views/Test/Test.vue')
        },
        {
          path: '/OnlineTest',
          name: 'OnlineTest',
          component: () => import('@/views/OnlineTest/OnlineTest.vue')
        },
        {
          path: '/StudentAnalysis',
          name: 'StudentAnalysis',
          component: () => import('@/views/StudentAnalysis/StudentAnalysis.vue')
        },
        {
          path: '/Self',
          name: 'Self',
          component: () => import('@/views/Self/Self.vue')
        }
      ]
    }
  ]
})
export default router
