<script setup>
import { ref } from 'vue'

// 模拟表格数据
const tableData = ref([
  {
    date: '2025-01-01',
    name: '课程主题1',
    address: '科目1'
  },
  {
    date: '2025-01-02',
    name: '课程主题2',
    address: '科目2'
  }
  // 更多数据...
])

// 查看和删除函数
const handleView = row => {
  console.log('查看:', row)
}
const handleDelete = row => {
  console.log('删除:', row)
}
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <h1>备课历史</h1>
    </template>
    <!--表格-->
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="date" label="日期" width="200" align="center" />
      <el-table-column prop="name" label="课程主题" width="300" align="center" />
      <el-table-column prop="address" label="科目" width="200" align="center" />
      <el-table-column label="操作" width="auto" align="center">
        <template #default="scope">
          <el-button size="mini" type="success" @click="handleView(scope.row)">查看</el-button>
          <el-button size="mini" type="warning" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<style scoped>
.box-card {
  margin-top: 5px;
  margin-right: 20px;
  width: auto;
}

.el-table .cell {
  text-align: center;
}

.el-button--success {
  background-color: #1da8e9;
  border-color: #1da8e9;
}
.el-button--warning {
  background-color: #f8aa34;
  border-color: #f8aa34;
}
</style>