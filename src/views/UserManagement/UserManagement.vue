<template>
  <div class="user-management">
    <!-- 动态渲染组件 -->
    <component :is="currentComponent" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AdminUserManagement from "@/views/AdminUserManagement/AdminUserManagement.vue";
import TeacherStudentManagement from "@/views/TeacherStudentManagement/TeacherStudentManagement.vue";

const userRole = ref(""); // 当前用户角色
const currentComponent = ref(null); // 当前要渲染的组件

// 获取当前用户角色
onMounted(() => {
  const role = localStorage.getItem("role");
  console.log("进入用户管理界面当前用户角色：", role);
  if (role) {
    userRole.value = role;
    // 根据角色设置当前组件
    if (role === "ADMIN") {
      currentComponent.value = AdminUserManagement;
    } else if (role === "TEACHER") {
      currentComponent.value = TeacherStudentManagement;
    }
  }
});
</script>

<style scoped>
.user-management {
  padding: 20px;
}
</style>
