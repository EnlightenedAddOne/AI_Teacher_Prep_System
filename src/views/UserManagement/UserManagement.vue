<template>
  <div class="user-management">
    <el-tabs v-model="activeTab" type="card">
      <!-- 管理员用户管理 -->
      <el-tab-pane label="用户管理" name="userManagement" v-if="userRole === 'ADMIN'">
        <AdminUserManagement />
      </el-tab-pane>
      <!-- 教师学生管理 -->
      <el-tab-pane label="学生管理" name="studentManagement" v-if="userRole === 'TEACHER'">
        <TeacherStudentManagement />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AdminUserManagement from "@/views/AdminUserManagement/AdminUserManagement.vue";
import TeacherStudentManagement from "@/views/TeacherStudentManagement/TeacherStudentManagement.vue";

const activeTab = ref("userManagement");
const userRole = ref(""); // 当前用户角色

// 获取当前用户角色
onMounted(() => {
  const role = localStorage.getItem("role");
  console.log("进入用户管理界面当前用户角色：", role);
  if (role) {
    userRole.value = role;
  }
});
</script>

<style scoped>
.user-management {
  padding: 20px;
}
</style>
