<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { isCollapse } from './IsCollapse'

const router = useRouter()
const route = useRoute()

// 面包屑列表
const breadcrumbList = ref([] as { path: string; name: string }[])

// 生成面包屑路径
const generateBreadcrumb = () => {
  const matched = route.matched.filter(record => record.meta && record.meta.title)
  breadcrumbList.value = matched.map(record => ({
    path: record.path,
    name: record.meta.title as string
  }))
}

// 监听路由变化，动态更新面包屑
watch(route, generateBreadcrumb, { immediate: true })

// 其他功能
const toself = async () => {
  router.push('/Self')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确认要退出吗？', '', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    });

    // 清理缓存
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("currentUsername");

    // 执行退出操作
    router.push('/login');
  } catch (error) {
    void error;
  }
};
</script>

<template>
  <!-- 头部 -->
  <el-header>
    <!-- 收起侧边栏的图标 -->
    <el-icon @click="isCollapse = !isCollapse">
      <IEpExpand v-show="isCollapse" />
      <IEpFold v-show="!isCollapse" />
    </el-icon>

    <!-- 面包屑组件 -->
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item v-for="item in breadcrumbList" :key="item.path" :to="item.path">
        {{ item.name }}
      </el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 下拉菜单 -->
    <el-dropdown class="dropdown">
      <span class="el-dropdown-link">
        <el-avatar
          :size="32"
          :src="'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'"
        />
        <el-icon class="el-icon--right">
          <IEpArrow-down />
        </el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="toself">个人中心</el-dropdown-item>
          <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </el-header>
</template>

<style scoped>
.el-header {
  display: flex;
  align-items: center;
  background-color: #bcc3c3;
  opacity: 0.6;
}

.el-header .el-icon {
  margin-right: 16px;
}

.el-dropdown {
  margin-left: auto;
  outline: none;
}

.el-dropdown .el-dropdown-link {
  display: flex;
  justify-content: center;
  align-items: center;
  outline: none;
}

.breadcrumb {
  margin-left: 16px;
  flex: 1;
  font-size: 16px; /* 字体放大 */
}
</style>
