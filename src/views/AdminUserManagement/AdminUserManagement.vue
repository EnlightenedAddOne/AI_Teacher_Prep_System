<template>
  <div class="user-list-card">
    <!-- 卡片头部 -->
    <div class="user-list-card-header">
      <span class="header-title">用户列表</span>
      <el-button type="primary" @click="openCreateUserDrawer" class="create-user-btn">
        创建用户
      </el-button>
    </div>

    <!-- 卡片主体 -->
    <div class="user-list-card-body">
      <!-- 用户表格 -->
      <div class="user-table-container">
        <el-table
          :data="currentPageUsers"
          style="width: 100%"
          :row-class-name="getRowClassName"
        >
          <el-table-column prop="id" label="ID" width="60"></el-table-column>
          <el-table-column prop="username" label="用户名"></el-table-column>
          <el-table-column prop="password" label="密码"></el-table-column>
          <el-table-column prop="role" label="角色"></el-table-column>
          <el-table-column label="操作" width="260">
            <template #default="scope">
              <!-- 编辑按钮 -->
              <el-button
                class="edit-btn"
                type="primary"
                size="small"
                @click="openEditUserDrawer(scope.row)"
              >
                编辑
              </el-button>
              <!-- 删除按钮 -->
              <el-button
                class="delete-btn"
                type="danger"
                size="small"
                @click="handleDeleteUser(scope.row.username)"
              >
                删除
              </el-button>
              <!-- 分配教师按钮 -->
              <el-button
                v-if="scope.row.role === 'STUDENT'"
                class="assign-btn"
                type="success"
                size="small"
                @click="openAssignTeacherDialog(scope.row)"
              >
                分配教师
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页组件 -->
      <div class="pagination-block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="users.length"
        ></el-pagination>
      </div>
    </div>
  </div>

  <!-- 创建用户抽屉 -->
  <el-drawer
    v-model="createUserDrawerVisible"
    title="创建用户"
    direction="rtl"
    size="40%"
    :before-close="handleCloseDrawer"
    @open="adjustTableContentWidth"
    @close="resetTableContentWidth"
  >
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
    <div class="drawer-footer">
      <el-button @click="createUserDrawerVisible = false">取消</el-button>
      <el-button type="primary" @click="handleCreateUser">确认</el-button>
    </div>
  </el-drawer>

  <!-- 编辑用户抽屉 -->
  <el-drawer
    v-model="editUserDrawerVisible"
    title="编辑用户"
    direction="rtl"
    size="40%"
    :before-close="handleCloseDrawer"
    @open="adjustTableContentWidth"
    @close="resetTableContentWidth"
  >
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
    <div class="drawer-footer">
      <el-button @click="editUserDrawerVisible = false">取消</el-button>
      <el-button type="primary" @click="handleEditUser">确认</el-button>
    </div>
  </el-drawer>

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
</template>

<script lang="ts">
import { ref, onMounted, computed } from "vue";
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
    const createUserDrawerVisible = ref(false); // 创建用户抽屉的显示状态
    const editUserDrawerVisible = ref(false); // 编辑用户抽屉的显示状态
    const assignTeacherDialogVisible = ref(false);
    const createUserForm = ref<User>({ username: "", password: "", role: "" });
    const editUserForm = ref<User>({ username: "", password: "", role: "" });
    const assignTeacherForm = ref<{ studentUsername: string; teacherUsername: string }>({ studentUsername: "", teacherUsername: "" });
    const teachers = ref<User[]>([]);

    // 分页相关
    const currentPage = ref(1);
    const pageSize = ref(5);
    const currentPageUsers = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = start + pageSize.value;
      return users.value.slice(start, end);
    });

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

    // 根据角色动态设置行类名
    const getRowClassName = ({ row }: { row: User }) => {
      return "custom-row";
    };

    // 打开创建用户抽屉
    const openCreateUserDrawer = () => {
      createUserForm.value = { username: "", password: "", role: "" };
      createUserDrawerVisible.value = true;
    };

    // 打开编辑用户抽屉
    const openEditUserDrawer = (user: User) => {
      editUserForm.value = { ...user };
      editUserDrawerVisible.value = true;
    };

    // 关闭抽屉时的回调
    const handleCloseDrawer = () => {
      createUserDrawerVisible.value = false;
      editUserDrawerVisible.value = false;
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
        createUserDrawerVisible.value = false;
        await fetchUsers();
      } catch (error) {
        console.error("用户创建失败：", error);
        ElMessage.error("用户创建失败");
      }
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
        editUserDrawerVisible.value = false;
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

    // 动态调整表格内容宽度
    const adjustTableContentWidth = () => {
      const tableContainer = document.querySelector(".user-table-container");
      if (tableContainer) {
        tableContainer.style.width = "calc(100% - 40%)"; // 假设抽屉宽度为 40%
      }
    };

    // 重置表格内容宽度
    const resetTableContentWidth = () => {
      const tableContainer = document.querySelector(".user-table-container");
      if (tableContainer) {
        tableContainer.style.width = "100%";
      }
    };

    // 分页事件处理
    const handleSizeChange = (newSize: number) => {
      pageSize.value = newSize;
    };

    const handleCurrentChange = (newPage: number) => {
      currentPage.value = newPage;
    };

    onMounted(() => {
      console.log("进入管理员界面");
      fetchUsers();
    });

    return {
      users,
      createUserDrawerVisible,
      editUserDrawerVisible,
      assignTeacherDialogVisible,
      createUserForm,
      editUserForm,
      assignTeacherForm,
      teachers,
      fetchUsers,
      openCreateUserDrawer,
      handleCreateUser,
      openEditUserDrawer,
      handleEditUser,
      handleDeleteUser,
      openAssignTeacherDialog,
      handleAssignTeacher,
      currentPage,
      pageSize,
      currentPageUsers,
      handleSizeChange,
      handleCurrentChange,
      getRowClassName,
      handleCloseDrawer,
      adjustTableContentWidth,
      resetTableContentWidth,
    };
  },
};
</script>

<style scoped>
/* 动画效果 */
.user-list-card {
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  max-height: 600px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  animation: slideInFromLeft 0.5s ease-in-out; /* 从左侧快速划入动画 */
}

@keyframes slideInFromLeft {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.user-list-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 10px;
  border-bottom: 1px solid #ccc; /* 添加底部边框 */
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #000; /* 文字颜色为黑色 */
  margin-left: 20px; /* 将标题向右移动 */
}

.create-user-btn {
  margin-right: 60px; /* 将按钮向左移动 */
}

.user-list-card-body {
  padding: 20px;
  overflow-y: auto;
  max-height: 500px;
}

.user-table-container {
  max-height: 400px;
  overflow-y: auto;
  transition: width 0.3s ease; /* 添加宽度过渡动画 */
}

/* 隐藏滚动条但保留滚动功能 */
.user-list-card-body::-webkit-scrollbar,
.user-table-container::-webkit-scrollbar {
  width: 0;
}

.pagination-block {
  margin-top: 20px;
  text-align: right; /* 分页插件移动到右侧 */
}

/* 表格行距 */
.el-table .custom-row {
  line-height: 100px;
}

/* 按钮样式调整 */
.edit-btn {
  background-color: #e6f7ff; /* 浅蓝色背景 */
  border: 1px solid #d0e6ff; /* 深色边框 */
  color: #000; /* 深色文字 */
}

.delete-btn {
  background-color: #ffe4e1; /* 浅粉色背景 */
  border: 1px solid #f7d0d0; /* 深色边框 */
  color: #000; /* 深色文字 */
}

.assign-btn {
  background-color: #e6ffec; /* 浅绿色背景 */
  border: 1px solid #d0f7e6; /* 深色边框 */
  color: #000; /* 深色文字 */
}

/* 抽屉底部按钮样式 */
.drawer-footer {
  text-align: right;
  margin-top: 20px;
}
</style>
