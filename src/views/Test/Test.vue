<script setup lang="ts">
import { reactive } from 'vue'

const formInline = reactive({
  subject: '', // 学科名称
  grade: '', // 学生年级
  topic: '', // 课程主题
  multipleChoiceCount: '', // 选择题题数
  multipleChoiceScore: '', // 选择题分值
  fillInTheBlankCount: '', // 填空题题数
  fillInTheBlankScore: '', // 填空题分值
  trueFalseCount: '', // 判断题题数
  trueFalseScore: '', // 判断题分值
  problemSolvingCount: '', // 解答题题数
  problemSolvingScore: '', // 解答题分值
  type: [] // 添加 type 属性
});

const generateResources = () => {
  console.log('生成练习题');
  console.log(formInline);
  // 在这里实现生成练习题的逻辑
};
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <h1>练习题生成设置</h1>
    </template>

    <el-form :model="formInline" class="demo-form-inline" label-position="top">
      <!-- 学科名称和学生年级 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="学科名称">
            <el-input v-model="formInline.subject" placeholder="学科名称" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="学生年级">
            <el-input v-model="formInline.grade" placeholder="学生年级" clearable />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 课程主题 -->
      <el-form-item label="课程主题">
        <el-input v-model="formInline.topic" placeholder="课程主题" clearable />
      </el-form-item>

      <!-- 选择题设置 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="选择题题数">
            <el-input v-model="formInline.multipleChoiceCount" placeholder="选择题题数" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="选择题分值">
            <el-input v-model="formInline.multipleChoiceScore" placeholder="选择题分值" clearable />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 填空题设置 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="填空题题数">
            <el-input v-model="formInline.fillInTheBlankCount" placeholder="填空题题数" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="填空题分值">
            <el-input v-model="formInline.fillInTheBlankScore" placeholder="填空题分值" clearable />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 判断题设置 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="判断题题数">
            <el-input v-model="formInline.trueFalseCount" placeholder="判断题题数" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="判断题分值">
            <el-input v-model="formInline.trueFalseScore" placeholder="判断题分值" clearable />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 解答题设置 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="解答题题数">
            <el-input v-model="formInline.problemSolvingCount" placeholder="解答题题数" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="解答题分值">
            <el-input v-model="formInline.problemSolvingScore" placeholder="解答题分值" clearable />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 生成按钮 -->
      <el-form-item class="button-center">
        <el-button
          type="primary"
          @click="generateResources"
          class="custom-button"
        >生成</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<style lang="scss" scoped>
.box-card {
  margin-top: 5px;
  margin-right: 20px;
  width: auto;
}

.demo-form-inline {
  .el-form-item {
    margin-bottom: 16px; // 调整间距
  }
}

.custom-button {
  &.el-button--primary {
    background-color: #1da8e9;
    border-color: #1da8e9;
  }
}

.button-center {
  text-align: center;
}
</style>
