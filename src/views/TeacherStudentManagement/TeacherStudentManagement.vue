<template>
  <div>
    <!-- 学生表格 -->
    <el-table :data="students" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="password" label="密码"></el-table-column>
      <el-table-column prop="role" label="角色"></el-table-column>
      <el-table-column prop="createdBy" label="创建者">
        <template #default="scope">
          {{ scope.row.createdBy || "" }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button type="text" @click="handleDeleteStudent(scope.row.username)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建学生对话框 -->
    <el-dialog v-model="createStudentDialogVisible" title="创建学生">
      <el-form :model="createStudentForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="createStudentForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="createStudentForm.password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createStudentDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateStudent">创建</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 创建学生按钮 -->
    <el-button type="primary" @click="createStudentDialogVisible = true">创建学生</el-button>
  </div>
</template>


<script lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { createStudent, deleteStudent, getStudents } from "@/api/user";

interface Student {
  id?: number; // 可选字段
  username: string;
  password: string;
  role?: string; // 学生角色，默认为 STUDENT
  createdBy?: string; // 创建者
}

export default {
  setup() {
    const students = ref<Student[]>([]);
    const createStudentDialogVisible = ref(false);
    const createStudentForm = ref<Student>({ username: "", password: "" });

    // 获取学生列表
    const fetchStudents = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      ElMessage.error("未登录，请先登录");
      return;
    }

    try {
      const data = await getStudents(token);
      // 过滤出角色为 STUDENT 的用户
      students.value = data.filter((student: Student) => student.role === "STUDENT");
    } catch (error) {
      console.error("获取学生列表失败:", error);
      ElMessage.error("获取学生列表失败");
    }
  };

    // 创建学生
    const handleCreateStudent = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        ElMessage.error("未登录，请先登录");
        return;
      }

      const studentData = {
        username: createStudentForm.value.username,
        password: createStudentForm.value.password,
        role: "STUDENT", // 默认角色为 STUDENT
        createdBy: localStorage.getItem("currentUsername") || "Unknown",
      };

      try {
        await createStudent(token, studentData);
        ElMessage.success("学生创建成功");
        createStudentDialogVisible.value = false;
        await fetchStudents();
      } catch (error) {
        console.error("创建学生失败:", error);
        ElMessage.error("创建学生失败");
      }
    };

    // 删除学生
    const handleDeleteStudent = async (username: string) => {
      const token = localStorage.getItem("token");
      if (!token) {
        ElMessage.error("未登录，请先登录");
        return;
      }

      try {
        await deleteStudent(token, username);
        ElMessage.success("学生删除成功");
        await fetchStudents();
      } catch (error) {
        console.error("删除学生失败:", error);
        ElMessage.error("删除学生失败");
      }
    };

    onMounted(() => {
      console.log("进入教师管理界面");
      fetchStudents();
    });

    return {
      students,
      createStudentDialogVisible,
      createStudentForm,
      fetchStudents,
      handleCreateStudent,
      handleDeleteStudent,
    };
  },
};
</script>
