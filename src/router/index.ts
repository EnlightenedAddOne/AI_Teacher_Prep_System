import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import IndexView from '@/views/IndexView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/TestPage',
      name: 'TestPage',
      component: () => import('@/views/TestPage.vue'),
      meta: { title: '测试页' }
    },
    {
      path: '/TestLogin',
      name: 'TestLogin',
      component: () => import('@/views/TestLogin.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/LoginView.vue'),
      meta: { title: '登录页' }
    },
    {
      path: '/',
      name: '',
      component: AppLayout,
      children: [
        {
          path: "",
          component: IndexView,
          meta: { title: '首页' }

        },
        {
          path: '/TeachingAuto',
          name: 'TeachingAuto',
          component: () => import('@/views/TeachingAuto/TeachingAuto.vue'),
          meta: { title: '智能备课助手' }
        },
        {
          path: '/Record',
          name: 'Record',
          component: () => import('@/views/Record/Record.vue'),
          meta: { title: '历史记录'}
        },
        {
          path: '/Test',
          name: 'Test',
          component: () => import('@/views/Test/Test.vue'),
          meta: { title: '智能习题生成器' }
        },
        {
          path: '/OnlineTest',
          name: 'OnlineTest',
          component: () => import('@/views/OnlineTest/OnlineTest.vue'),
          meta: { title: '在线测试生成器' }
        },
        {
          path: '/StudentAnalysis',
          name: 'StudentAnalysis',
          component: () => import('@/views/StudentAnalysis/StudentAnalysis.vue'),
          meta: { title: '智能学情分析' }
        },
        {
          path: '/Self',
          name: 'Self',
          component: () => import('@/views/Self/Self.vue'),
          meta: { title: '个人中心' }
        }
      ]
    }
  ]
})
export default router
