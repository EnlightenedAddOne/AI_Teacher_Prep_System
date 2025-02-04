<script setup lang="ts">
import AppAside from './AppAside.vue'
import Appheader from './AppHeader.vue'
</script>

<template>
  <div class="common-layout">
    <el-container>
      <AppAside />
      <el-container class="header-and-main">
        <AppHeader />
        <!--主体-->
        <el-main>
          <el-scrollbar>
            <RouterView />
          </el-scrollbar>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.header-and-main {
  flex-direction: column;
  height: 100vh;
}
.el-main {
  background-color: rgb(225, 245, 245);
  padding-right: 0;
}
</style>
