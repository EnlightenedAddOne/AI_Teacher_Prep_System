<script setup lang="ts">
import { ref } from 'vue'
import { isCollapse } from './IsCollapse'
import { LoginInfo, logout } from '@/api/users'
import { useRouter } from 'vue-router'
const router = useRouter()

const toself = async () => {
  router.push('/Self');
}

//退出事件处理
const handleLogout = async () => {
  //1.询问用户确认退出
  await ElMessageBox.confirm('确认要退出吗？', ' ', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  }).catch(() => {
    return new Promise(() => {})
  })
  //2.执行退出
  //await logout().catch(() => {})
  //3.清空token
  //
  //4.跳转到login
  router.push('/login')
}
</script>

<template>
  <!--头部-->
  <el-header>
    <!--图标-->
    <el-icon @click="isCollapse=!isCollapse">
      <IEpExpand v-show="isCollapse" />
      <IEpFold v-show="!isCollapse" />
    </el-icon>

    <!--下拉菜单-->
    <el-dropdown>
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
</style>
