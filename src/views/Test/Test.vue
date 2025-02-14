<template>
  <div class="exercises-section">
    <el-card class="box-card request-card">
      <template #header>
        <div class="card-header">
          <span>练习题生成需求</span>
        </div>
      </template>
      <el-form ref="exercisesForm" :model="exercisesRequest" label-width="120px" class="form-content">
        <el-form-item label="科目">
          <el-input v-model="exercisesRequest.subject" placeholder="请输入科目"></el-input>
        </el-form-item>
        <el-form-item label="主题">
          <el-input v-model="exercisesRequest.topic" placeholder="请输入主题"></el-input>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="exercisesRequest.degree">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="练习题配置">
          <el-form-item label="题型">
            <el-select v-model="exercisesRequest.exercise_config.type">
              <el-option label="选择题" value="choice" />
              <el-option label="填空题" value="fill" />
              <el-option label="判断题" value="judge" />
              <el-option label="简答题" value="short_answer" />
              <el-option label="应用计算题" value="application" />
            </el-select>
          </el-form-item>
          <el-form-item label="题目数量">
            <el-input-number v-model="exercisesRequest.exercise_config.count" :min="1" />
          </el-form-item>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleGenerateExercises">生成练习题</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="box-card result-card">
      <template #header>
        <div class="card-header">
          <span>练习题生成结果</span>
        </div>
      </template>
      <div class="result-content">
        <!-- 加载动画 -->
        <div v-if="isLoading" class="loading-container">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <p>正在生成练习题，请稍候...</p>
        </div>

        <!-- 下载按钮 -->
        <div v-else-if="exercisesResponse">
          <el-button type="success" @click="downloadPdf('exercises.pdf')">下载练习题 PDF</el-button>
          <el-button type="success" @click="downloadPdf('answers_and_explanations.pdf')">下载答案解析 PDF</el-button>
        </div>

        <!-- 提示信息 -->
        <div v-else>
          <p>请填写左侧表格并生成练习题。</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { generateExercises, downloadPdf as apiDownloadPdf } from '@/api/examService';
import type { ExerciseRequest, ExerciseResponse } from '@/types/exam';
import { Loading } from '@element-plus/icons-vue'; // 引入加载图标

const exercisesRequest = ref<ExerciseRequest>({
  subject: '',
  topic: '',
  degree: '',
  exercise_config: {
    type: 'choice',
    count: 1
  }
});

const exercisesResponse = ref<ExerciseResponse | null>(null);
const isLoading = ref(false);

const handleGenerateExercises = async () => {
  isLoading.value = true;
  try {
    exercisesResponse.value = await generateExercises(exercisesRequest.value);
  } catch (error) {
    console.error('生成练习题失败:', error);
  } finally {
    isLoading.value = false;
  }
};

const downloadPdf = async (filename: string) => {
  try {
    const blob = await apiDownloadPdf(filename);
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error('下载 PDF 失败:', error);
  }
};
</script>

<style scoped>
.exercises-section {
  padding: 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

.box-card {
  margin-bottom: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  color: #6a806b;
  border-bottom: 2px solid #ddd;
  padding: 10px 20px;
}

.form-content {
  padding: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100px;
  padding: 20px;
}

.loading-icon {
  animation: spin 1s infinite linear;
  font-size: 32px;
  margin-bottom: 8px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.result-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  margin-top: 0px;
}
</style>
