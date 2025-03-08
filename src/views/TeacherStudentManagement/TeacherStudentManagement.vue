<template>
  <div class="user-list-card">
    <!-- 卡片头部 -->
    <div class="user-list-card-header">
      <span class="header-title">学生列表</span>
      <el-button type="primary" @click="createStudentDialogVisible = true" class="create-user-btn">
        创建学生
      </el-button>
    </div>

    <!-- 卡片主体 -->
    <div class="user-list-card-body">
      <!-- 学生表格 -->
      <div class="user-table-container">
        <el-table
          :data="currentPageStudents"
          style="width: 100%"
          :row-class-name="getRowClassName"
        >
          <el-table-column prop="id" label="ID" width="60"></el-table-column>
          <el-table-column prop="username" label="用户名"></el-table-column>
          <el-table-column prop="password" label="密码"></el-table-column>
          <el-table-column prop="role" label="角色"></el-table-column>
          <el-table-column prop="createdBy" label="创建者"></el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button
                type="text"
                @click="handleDeleteStudent(scope.row.username)"
              >
                删除
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
          :total="students.length"
        ></el-pagination>
      </div>
    </div>
  </div>

  <!-- 创建学生抽屉 -->
  <el-drawer
    v-model="createStudentDialogVisible"
    title="创建学生"
    direction="rtl"
    size="40%"
    :before-close="handleCloseDrawer"
  >
    <el-form :model="createStudentForm" label-width="100px">
      <el-form-item label="用户名">
        <el-input v-model="createStudentForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="createStudentForm.password" type="password"></el-input>
      </el-form-item>
    </el-form>
    <div class="drawer-footer">
      <el-button @click="createStudentDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleCreateStudent">创建</el-button>
    </div>
  </el-drawer>
</template>

<style scoped>
.user-list-card {
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  max-height: 600px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  animation: slideInFromLeft 0.5s ease-in-out;
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
  border-bottom: 1px solid #ccc;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #000;
  margin-left: 20px;
}

.create-user-btn {
  margin-right: 60px;
}

.user-list-card-body {
  padding: 20px;
  overflow-y: auto;
  max-height: 500px;
}

.user-table-container {
  max-height: 400px;
  overflow-y: auto;
  transition: width 0.3s ease;
}

.user-list-card-body::-webkit-scrollbar,
.user-table-container::-webkit-scrollbar {
  width: 0;
}

.pagination-block {
  margin-top: 20px;
  text-align: right;
}

.el-table .custom-row {
  line-height: 100px;
}

.drawer-footer {
  text-align: right;
  margin-top: 20px;
}
</style>


<script lang="ts">
import { ref, onMounted, computed } from "vue";
import { ElMessage } from "element-plus";
import { createStudent, deleteStudent, getStudents } from "@/api/user";

interface Student {
  id?: number;
  username: string;
  password: string;
  role?: string;
  createdBy?: string;
}

export default {
  setup() {
    const students = ref<Student[]>([]);
    const createStudentDialogVisible = ref(false);
    const createStudentForm = ref<Student>({ username: "", password: "" });

    // 分页相关
    const currentPage = ref(1);
    const pageSize = ref(5);
    const currentPageStudents = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = start + pageSize.value;
      return students.value.slice(start, end);
    });

    // 获取学生列表
    const fetchStudents = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        ElMessage.error("未登录，请先登录");
        return;
      }

      try {
        const data = await getStudents(token);
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
        role: "STUDENT",
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

    // 分页事件处理
    const handleSizeChange = (newSize: number) => {
      pageSize.value = newSize;
    };

    const handleCurrentChange = (newPage: number) => {
      currentPage.value = newPage;
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
      currentPage,
      pageSize,
      currentPageStudents,
      handleSizeChange,
      handleCurrentChange,
    };
  },
};
</script>
