<script setup lang="ts">
import { ref } from 'vue';
import { isCollapse } from './IsCollapse';
</script>

<template>
  <el-aside>
    <el-menu router unique-opened :collapse="isCollapse">
      <a href="/IndexView" class="logo">
        <h1>AI辅助教师备课系统</h1>
      </a>

      <el-menu-item index="/TeachingAuto">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpDocument />
          </el-icon>
          <span>智能备课助手</span>
        </div>
      </el-menu-item>

      <el-menu-item index="/Test">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpEditPen />
          </el-icon>
          <span>智能习题生成器</span>
        </div>
      </el-menu-item>

      <el-menu-item index="/OnlineTest">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpList />
          </el-icon>
          <span>在线测生成器</span>
        </div>
      </el-menu-item>

      <el-menu-item index="/UserManagement">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpUser />
          </el-icon>
          <span>用户管理</span>
        </div>
      </el-menu-item>

      <el-menu-item index="/StudentAnalysis">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpDataAnalysis />
          </el-icon>
          <span>智能学情分析</span>
        </div>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style lang="scss" scoped>
.el-aside {
  background-color: #2c3e50; /* 深蓝色背景 */
  height: 100vh;
  width: auto;
  color: #fff; /* 白色文字 */
  transition: width 0.3s ease;
}

.logo {
  display: flex;
  justify-content: center;
  text-decoration: none;
  color: #fff; /* 白色文字 */
  height: 60px;
  align-items: center;
  img {
    width: 32px;
    height: 32px;
  }
}

.el-menu {
  background-color: #2c3e50; /* 深蓝色背景 */
  border-right: none;
  width: 250px;
  transition: width 0.3s ease;

  &.el-menu--collapse {
    width: 60px;
    h1 {
      display: none;
    }
  }
}

.el-menu-item {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 60px;
  padding: 0 20px;
  gap: 10px;
  color: #fff; /* 白色文字 */
  &:hover {
    background-color: #42b983; /* 悬停时浅蓝色背景 */
  }
}

.icon-text-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
  .el-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    margin: 0;
    padding: 0;
  }
  span {
    line-height: 60px;
    margin: 0;
    padding: 0;
  }
}
</style>
