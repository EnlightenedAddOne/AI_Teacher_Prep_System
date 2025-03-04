import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/components/layout/AppLayout.vue';
import IndexView from '@/views/IndexView.vue';
import { ElMessage } from 'element-plus';

// 扩展 RouteMeta 类型，添加 roles 属性
declare module 'vue-router' {
  interface RouteMeta {
    title?: string;       // 路由标题
    requiresAuth?: boolean; // 是否需要认证
    roles?: string[];     // 允许访问的角色数组
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/TestPage',
      name: 'TestPage',
      component: () => import('@/views/TestPage.vue'),
      meta: { title: '测试页' },
    },
    {
      path: '/TestLogin',
      name: 'TestLogin',
      component: () => import('@/views/TestLogin.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/LoginView.vue'),
      meta: { title: '登录页' },
    },
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: AppLayout,
      children: [
        {
          path: '/IndexView',
          name: 'IndexView',
          component: () => import('@/views/IndexView.vue'),
          meta: { title: '首页' },
        },
        {
          path: '/TeachingAuto',
          name: 'TeachingAuto',
          component: () => import('@/views/TeachingAuto/TeachingAuto.vue'),
          meta: { title: '智能备课助手' },
        },
        {
          path: '/Record',
          name: 'Record',
          component: () => import('@/views/Record/Record.vue'),
          meta: { title: '历史记录' },
        },
        {
          path: '/Test',
          name: 'Test',
          component: () => import('@/views/Test/Test.vue'),
          meta: { title: '智能习题生成器' },
        },
        {
          path: '/OnlineTest',
          name: 'OnlineTest',
          component: () => import('@/views/OnlineTest/OnlineTest.vue'),
          meta: { title: '在线测试生成器' },
        },
        {
          path: '/UserManagement',
          name: 'UserManagement',
          component: () => import('@/views/UserManagement/UserManagement.vue'),
          meta: { title: '用户管理', requiresAuth: true, roles: ['ADMIN', 'TEACHER'] },
        },
        {
          path: '/StudentAnalysis',
          name: 'StudentAnalysis',
          component: () => import('@/views/StudentAnalysis/StudentAnalysis.vue'),
          meta: { title: '智能学情分析' },
        },
        {
          path: '/Self',
          name: 'Self',
          component: () => import('@/views/Self/Self.vue'),
          meta: { title: '个人中心' },
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('role');

  // 打印 token 和 userRole 的值
  console.log("当前 Token：", token);
  console.log("当前用户角色：", userRole);

  // 检查是否需要认证
  if (to.meta.requiresAuth && !token) {
    // 如果需要认证但没有 token，跳转到登录页
    next('/login');
  } else if (to.meta.roles && Array.isArray(to.meta.roles) && userRole && !to.meta.roles.includes(userRole)) {
    // 如果用户角色不符合要求，提示无权限并跳转到首页
    ElMessage.error('您没有权限访问该页面');
    next({ name: 'IndexView' });
  } else {
    next();
  }
});
export default router;
