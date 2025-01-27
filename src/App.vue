<script setup lang="ts">
import { RouterView } from 'vue-router'

//这是试验接口start
import request from './utils/request'
request({
  method: 'GET', //请求类型
  url: '/users', //请求地址 实际请求地址要加上之前的baseURL
  //请求参数（无）
}).then((res) => {
  console.log(res)
})
//试验接口end
</script>

<template>
  <!--占位符，用于显示当前路由匹配的组件-->
  <RouterView />
</template>

<style scoped></style>
