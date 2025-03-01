<template>
  <div class="exercises-section">
    <!-- 新增的动画文本 -->
    <div class="intro-text" v-if="!isGenerating && !exercisesResponse">
      <h2>智能练习题器</h2>
      <p>一键生成高质量练习题，助力教学与学习。</p>
    </div>

    <!-- 功能入口 -->
    <div v-if="!isGenerating && !exercisesResponse" class="feature-box" @click="showExercisesForm = true">
      <el-icon><Edit /></el-icon>
      <div class="feature-content">
        <h1>练习题生成</h1>
        <p>自动生成练习题，帮助学生巩固知识。</p>
      </div>
    </div>

    <!-- 练习题生成需求表单 -->
    <el-dialog
      v-model="showExercisesForm"
      title="练习题生成需求"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      class="exercises-dialog"
      width="50%"
    >
      <el-form
        ref="exercisesForm"
        :model="exercisesRequest"
        label-width="120px"
        class="form-content"
      >
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
            <el-input-number v-model="exercisesRequest.exercise_config.choice.count" :min="0" class="config-input"></el-input-number>
            <span class="label">选择题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.choice.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>填空题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.fill.count" :min="0" class="config-input"></el-input-number>
            <span class="label">填空题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.fill.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>判断题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.judge.count" :min="0" class="config-input"></el-input-number>
            <span class="label">判断题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.judge.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>简答题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.short_answer.count" :min="0" class="config-input"></el-input-number>
            <span class="label">简答题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.short_answer.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>应用题题数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.application.count" :min="0" class="config-input"></el-input-number>
            <span class="label">应用题分数：</span>
            <el-input-number v-model="exercisesRequest.exercise_config.application.score" :min="0" class="config-input"></el-input-number>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showExercisesForm = false">取消</el-button>
        <el-button type="primary" @click="handleGenerateExercises">生成练习题</el-button>
      </template>
    </el-dialog>

    <!-- 练习题生成结果展示 -->
    <div v-if="exercisesResponse || isGenerating" class="result-container">
      <!-- 返回按钮 -->
      <el-card class="box-card back-card">
        <el-button class="back-button" type="text" @click="resetState">&lt;&lt; 返回</el-button>
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
            <el-button class="download-button" type="success" @click="downloadPdf('exercises.pdf')">下载练习题 PDF</el-button>
            <el-button class="download-button" type="success" @click="downloadPdf('answers_and_explanations.pdf')">下载答案解析 PDF</el-button>
          </div>

          <!-- 提示信息 -->
          <div v-else>
            <p>请填写上方表格生成练习题。</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { generateExercises, downloadPdf as apiDownloadPdf } from '@/api/examService';
import type { ExerciseRequest, ExerciseResponse } from '@/types/exam';
import { Loading, Edit } from '@element-plus/icons-vue';
import { marked } from 'marked';

const showExercisesForm = ref(false); // 控制表单弹窗的显示
const exercisesRequest = ref<ExerciseRequest>({
  subject: '',
  topic: '',
  degree: '',
  exercise_config: {
    choice: { count: 0, score: 0, enabled: true },
    fill: { count: 0, score: 0, enabled: true },
    judge: { count: 0, score: 0, enabled: true },
    short_answer: { count: 0, score: 0, enabled: true },
    application: { count: 0, score: 0, enabled: true }
  }
});
const exercisesResponse = ref<ExerciseResponse | null>(null);
const isLoading = ref(false);
const isGenerating = ref(false);

const handleGenerateExercises = async () => {
  showExercisesForm.value = false; // 关闭表单弹窗
  isGenerating.value = true; // 设置标志变量，表示正在生成

  try {
    isLoading.value = true;
    exercisesResponse.value = await generateExercises(exercisesRequest.value);
  } catch (error) {
    console.error('生成练习题失败:', error);
    alert('生成练习题失败，请检查输入是否正确');
    resetState(); // 如果失败，重置状态
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

const formatMarkdown = (response: ExerciseResponse) => {
  if (response) {
    return marked(response.exercises);
  }
  return '';
};

const resetState = () => {
  showExercisesForm.value = false;
  exercisesResponse.value = null;
  isGenerating.value = false;
};
</script>

<style scoped>
.exercises-section {
  padding: 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 新增的动画文本样式 */
.intro-text {
  text-align: center;
  margin-bottom: 20px;
  animation: fadeIn 2s ease forwards;
}

.intro-text h2 {
  font-size: 2em;
  color: #409eff;
}

.intro-text p {
  font-size: 1.2em;
  color: #666;
}

/* 功能入口样式 */
.feature-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 500px;
  height: 500px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin: auto;
  padding: 20px;
}

.feature-box:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.feature-box .el-icon {
  font-size: 7em;
  color: #409eff;
  margin-bottom: 20px;
}

.feature-box h3 {
  font-size: 1.5em;
  color: #333;
  margin: 0 0 10px 0;
}

.feature-box p {
  font-size: 1.1em;
  color: #666;
  margin: 0;
  text-align: center;
  line-height: 1.5;
}

/* 动画定义 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 返回按钮和结果卡片的宽度固定为 800px */
.box-card {
  width: 800px; /* 固定宽度 */
  margin: 20px auto;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  padding: 10px 20px;
}

.result-content {
  display: flex;
  flex-direction: column;
  align-items: center;
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

.preview-container {
  border: 1px solid #ddd;
  padding: 10px;
  margin-top: 20px;
  max-height: 300px;
  overflow-y: auto;
  width: calc(100% - 20px);
}

.download-button {
  margin-top: 10px;
}

.back-card {
  position: sticky;
  top: 20px;
  width: 800px; /* 固定宽度 */
  margin: 0 auto 20px;
}

.back-button {
  font-size: 16px;
  color: #1677ff;
  text-decoration: none;
  cursor: pointer;
}

h1{
  font-size: 37px;
  text-align: center;
}
</style>
