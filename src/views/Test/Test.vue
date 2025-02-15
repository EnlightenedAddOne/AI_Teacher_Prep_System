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
        <el-form-item label="题型配置">
          <div class="config-item">
            <span>选择题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.choice_count" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>选择题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.choice_score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>填空题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.fill_count" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>填空题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.fill_score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>应用题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.application_count" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>应用题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.application_score" :min="0" class="config-input"></el-input-number>
          </div>
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

        <!-- 生成结果展示 -->
        <div v-else-if="exercisesResponse" class="result-display">
          <div class="preview-container">
            <div v-html="formatMarkdown(exercisesResponse)"></div>
          </div>
          <!-- 按钮移动到外部 -->
          <div class="download-buttons">
            <el-button type="success" @click="downloadPdf('exercises.pdf')">下载练习题 PDF</el-button>
            <el-button type="success" @click="downloadPdf('answers_and_explanations.pdf')">下载答案解析 PDF</el-button>
          </div>
        </div>

        <!-- 提示信息 -->
        <div v-else>
          <p>请填写上方表格生成练习题。</p>
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
import { marked } from 'marked'; // 引入marked库用于Markdown渲染

const exercisesRequest = ref<ExerciseRequest>({
  subject: '',
  topic: '',
  degree: '',
  exercise_config: {
     choice_count: 0,
    choice_score: 0,
    fill_count: 0,
    fill_score: 0,
    application_count: 0,
    application_score: 0
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

// 格式化Markdown文本
const formatMarkdown = (response: ExerciseResponse) => {
  if (response) {
    return marked(response.exercises);
  }
  return '';
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
  background-color: #f9f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  padding: 10px 20px;
}

.form-content {
  padding: 20px;
}

.config-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.config-input {
  margin-left: 10px;
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

.result-display {
  width: calc(100% - 70px); /* 距离左右边界各35px */
  margin: 0 35px 40px; /* 上下间距调整 */
}

.preview-container {
  border: 1px solid #ddd;
  padding: 10px;
  margin-top: 20px;
  max-height: 300px; /* 固定高度 */
  overflow-y: auto; /* 可滚动 */
}

.download-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 距离浏览框下边沿20px */
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  margin-top: 0px;
}
</style>
