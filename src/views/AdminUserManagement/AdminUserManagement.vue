<template>
  <div>
    <!-- 用户表格 -->
    <el-table :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="password" label="密码"></el-table-column>
      <el-table-column prop="role" label="角色"></el-table-column>
      <el-table-column prop="createdBy" label="创建者">
        <template #default="scope">
          {{ scope.row.createdBy || "" }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="260">
        <template #default="scope">
          <el-button type="text" @click="openEditUserDialog(scope.row)">编辑</el-button>
          <el-button type="text" @click="handleDeleteUser(scope.row.username)">删除</el-button>
          <el-button
            type="text"
            v-if="scope.row.role === 'STUDENT'"
            @click="openAssignTeacherDialog(scope.row)"
          >
            分配教师
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建用户对话框 -->
    <el-dialog v-model="createUserDialogVisible" title="创建用户">
      <el-form :model="createUserForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="createUserForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="createUserForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="createUserForm.role">
            <el-option label="教师" value="TEACHER"></el-option>
            <el-option label="学生" value="STUDENT"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="创建者" v-if="createUserForm.role === 'STUDENT'">
          <el-select v-model="createUserForm.createdBy">
            <el-option
              v-for="teacher in teachers"
              :key="teacher.username"
              :label="teacher.username"
              :value="teacher.username"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createUserDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateUser">确认</el-button>
      </template>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog v-model="editUserDialogVisible" title="编辑用户">
      <el-form :model="editUserForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="editUserForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="editUserForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editUserForm.role">
            <el-option label="管理员" value="ADMIN"></el-option>
            <el-option label="教师" value="TEACHER"></el-option>
            <el-option label="学生" value="STUDENT"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editUserDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEditUser">确认</el-button>
      </template>
    </el-dialog>

    <!-- 分配教师对话框 -->
    <el-dialog v-model="assignTeacherDialogVisible" title="分配教师">
      <el-form :model="assignTeacherForm" label-width="100px">
        <el-form-item label="学生">
          <el-input v-model="assignTeacherForm.studentUsername" disabled></el-input>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="assignTeacherForm.teacherUsername">
            <el-option
              v-for="teacher in teachers"
              :key="teacher.username"
              :label="teacher.username"
              :value="teacher.username"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignTeacherDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssignTeacher">确认</el-button>
      </template>
    </el-dialog>

    <!-- 创建用户按钮 -->
    <el-button type="primary" @click="openCreateUserDialog">创建用户</el-button>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import {
  createUser,
  deleteUser,
  updateUser,
  getAllUsers,
  assignStudentToTeacher
} from "@/api/user";

interface User {
  id?: number;
  username: string;
  password: string;
  role: string;
  createdBy?: string;
}

export default {
  setup() {
    const users = ref<User[]>([]);
    const createUserDialogVisible = ref(false);
    const editUserDialogVisible = ref(false);
    const assignTeacherDialogVisible = ref(false);
    const createUserForm = ref<User>({ username: "", password: "", role: "" });
    const editUserForm = ref<User>({ username: "", password: "", role: "" });
    const assignTeacherForm = ref<{ studentUsername: string; teacherUsername: string }>({ studentUsername: "", teacherUsername: "" });
    const teachers = ref<User[]>([]);

    // 获取用户列表
    const fetchUsers = async () => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token) {
        ElMessage.error("未登录，请先登录");
        return;
      }

      if (role !== "ADMIN") {
        ElMessage.error("您没有权限访问此页面");
        return;
      }

      try {
        const response = await getAllUsers(token);
        users.value = response;
        teachers.value = response.filter(user => user.role === "TEACHER");
        console.log("获取到的用户列表：", users.value);
      } catch (error) {
        console.error("获取用户列表失败：", error);
        ElMessage.error("获取用户列表失败");
      }
    };

    // 打开创建用户对话框
    const openCreateUserDialog = () => {
      createUserForm.value = { username: "", password: "", role: "" };
      createUserDialogVisible.value = true;
    };

    // 创建用户
    const handleCreateUser = async () => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token || role !== "ADMIN") {
        ElMessage.error("您没有权限创建用户");
        return;
      }

      if (createUserForm.value.role === "ADMIN") {
        ElMessage.error("管理员不能创建管理员账号");
        return;
      }

      try {
        await createUser(token, createUserForm.value);
        ElMessage.success("用户创建成功");
        createUserDialogVisible.value = false;
        await fetchUsers();
      } catch (error) {
        console.error("用户创建失败：", error);
        ElMessage.error("用户创建失败");
      }
    };

    // 打开编辑用户对话框
    const openEditUserDialog = (user: User) => {
      editUserForm.value = { ...user };
      editUserDialogVisible.value = true;
    };

    // 编辑用户
    const handleEditUser = async () => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token || role !== "ADMIN") {
        ElMessage.error("您没有权限编辑用户");
        return;
      }

      try {
        await updateUser(token, editUserForm.value);
        ElMessage.success("用户更新成功");
        editUserDialogVisible.value = false;
        await fetchUsers();
      } catch (error) {
        console.error("用户更新失败：", error);
        ElMessage.error("用户更新失败");
      }
    };

    // 删除用户
    const handleDeleteUser = async (username: string) => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token || role !== "ADMIN") {
        ElMessage.error("您没有权限删除用户");
        return;
      }

      try {
        await deleteUser(token, username);
        ElMessage.success("用户删除成功");
        await fetchUsers();
      } catch (error) {
        console.error("用户删除失败：", error);
        ElMessage.error("用户删除失败");
      }
    };

    // 打开分配教师对话框
    const openAssignTeacherDialog = (student: User) => {
      assignTeacherForm.value = { studentUsername: student.username, teacherUsername: "" };
      assignTeacherDialogVisible.value = true;
    };

    // 分配教师
    const handleAssignTeacher = async () => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token || role !== "ADMIN") {
        ElMessage.error("您没有权限分配教师");
        return;
      }

      try {
        await assignStudentToTeacher(token, assignTeacherForm.value.studentUsername, assignTeacherForm.value.teacherUsername);
        ElMessage.success("分配成功");
        assignTeacherDialogVisible.value = false;
        await fetchUsers();
      } catch (error) {
        console.error("分配失败：", error);
        ElMessage.error("分配失败");
      }
    };

    onMounted(() => {
      console.log("进入管理员界面");
      fetchUsers();
    });

    return {
      users,
      createUserDialogVisible,
      editUserDialogVisible,
      assignTeacherDialogVisible,
      createUserForm,
      editUserForm,
      assignTeacherForm,
      teachers,
      fetchUsers,
      openCreateUserDialog,
      handleCreateUser,
      openEditUserDialog,
      handleEditUser,
      handleDeleteUser,
      openAssignTeacherDialog,
      handleAssignTeacher,
    };
  },
};
</script>
