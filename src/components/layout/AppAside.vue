<script setup lang="ts">
import { ref } from 'vue'
import { isCollapse } from './IsCollapse'
</script>

<template>
  <!--侧边栏-->
  <el-aside>
    <!--菜单-->
    <el-menu router unique-opened :collapse="isCollapse">
      <a href="/" class="logo">
        <h1>AI辅助教师备课系统</h1>
      </a>
      <el-menu-item index="/TeachingAuto">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpSetting />
          </el-icon>
          <span>教学自动化生成</span>
        </div>
      </el-menu-item>

      <el-menu-item index="/Record">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpSetting />
          </el-icon>
          <span>备课记录</span>
        </div>
      </el-menu-item>

      <el-menu-item index="/StudentAnalysis">
        <div class="icon-text-wrapper">
          <el-icon>
            <IEpSetting />
          </el-icon>
          <span>学情分析</span>
        </div>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>


<style lang="scss" scoped>
.el-aside {
  background-color: #70c3c3;
  height: 100vh;
  width: auto;
}
.logo {
  display: flex;
  justify-content: center;
  text-decoration: none;
  color: black;
  height: 60px;
  align-items: center;
  img {
    width: 32px;
    height: 32px;
  }
}
.el-menu {
  background-color: #70c3c3;
  border-right: none;
  width: 250px;
  &.el-menu--collapse {
    background-color: #70c3c3;
    width: 60px;
    & h1 {
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