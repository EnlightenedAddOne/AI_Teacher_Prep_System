<template>
  <div class="online-test-section">
    <!-- 动画文本 -->
    <div class="intro-text" v-if="!isGenerating && !onlineTestResponse && !showResult">
      <h2>在线测试生成器</h2>
      <p>快速生成在线测试，助力学习与评估。</p>
    </div>

    <!-- 功能入口 -->
    <div v-if="!isGenerating && !onlineTestResponse && !showResult" class="feature-box" @click="showOnlineTestForm = true">
      <el-icon><Edit /></el-icon>
      <div class="feature-content">
        <h1>在线测试生成</h1>
        <p>自动生成在线测试，帮助学生进行自我评估。</p>
      </div>
    </div>

    <!-- 1. 在线测试生成需求表单 -->
    <el-dialog
      v-model="showOnlineTestForm"
      title="在线测试生成需求"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      class="online-test-dialog"
      width="50%"
    >
      <el-form
        ref="onlineTestForm"
        :model="onlineTestRequest"
        label-width="120px"
        class="form-content"
      >
        <el-form-item label="科目">
          <el-input v-model="onlineTestRequest.subject" placeholder="请输入科目"></el-input>
        </el-form-item>
        <el-form-item label="主题">
          <el-input v-model="onlineTestRequest.topic" placeholder="请输入主题"></el-input>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="onlineTestRequest.degree">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间限制（分钟）">
          <el-input-number v-model="onlineTestRequest.time_limit" :min="1" class="config-input"></el-input-number>
        </el-form-item>
        <el-form-item label="题型配置">
          <div class="config-item">
            <span>选择题题数：</span>
            <el-input-number v-model="onlineTestRequest.questions.choice.count" :min="0" class="config-input"></el-input-number>
            <span class="label">选择题分数：</span>
            <el-input-number v-model="onlineTestRequest.questions.choice.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>填空题题数：</span>
            <el-input-number v-model="onlineTestRequest.questions.fill.count" :min="0" class="config-input"></el-input-number>
            <span class="label">填空题分数：</span>
            <el-input-number v-model="onlineTestRequest.questions.fill.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>判断题题数：</span>
            <el-input-number v-model="onlineTestRequest.questions.judge.count" :min="0" class="config-input"></el-input-number>
            <span class="label">判断题分数：</span>
            <el-input-number v-model="onlineTestRequest.questions.judge.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>简答题题数：</span>
            <el-input-number v-model="onlineTestRequest.questions.short_answer.count" :min="0" class="config-input"></el-input-number>
            <span class="label">简答题分数：</span>
            <el-input-number v-model="onlineTestRequest.questions.short_answer.score" :min="0" class="config-input"></el-input-number>
          </div>
          <div class="config-item">
            <span>应用计算题题数：</span>
            <el-input-number v-model="onlineTestRequest.questions.application.count" :min="0" class="config-input"></el-input-number>
            <span class="label">应用计算题分数：</span>
            <el-input-number v-model="onlineTestRequest.questions.application.score" :min="0" class="config-input"></el-input-number>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showOnlineTestForm = false">取消</el-button>
        <el-button type="primary" @click="handleGenerateOnlineTest">生成在线测试</el-button>
      </template>
    </el-dialog>

    <!-- 2. 在线测试测试界面 -->
    <div v-if="onlineTestResponse || isGenerating" class="result-container">
      <!-- 返回按钮 -->
      <el-card class="box-card back-card">
        <el-button class="back-button" type="text" @click="resetState">&lt;&lt; 返回</el-button>
      </el-card>

      <!-- 倒计时器 -->
      <el-card class="box-card timer-card">
        <template #header>
          <div class="card-header">
            <span>倒计时</span>
          </div>
        </template>
        <div class="timer-content">
          <div v-if="!isTimerStarted && onlineTestResponse">
            <p>题目已经生成，请点击开始按钮开始答题。</p>
          </div>
          <div v-else>
            <span>剩余时间：</span>
            <span>{{ formattedTime }}</span>
          </div>
          <div class="timer-controls">
            <el-button
              type="primary"
              @click="startTimerAndShowQuestions"
              :disabled="isTimerStarted || remainingTime <= 0"
            >
              开始答题
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- 在线测试 -->
      <el-card class="box-card result-card">
        <template #header>
          <div class="card-header">
            <span>在线测试</span>
          </div>
        </template>
        <div class="result-content">
          <!-- 加载动画 -->
          <div v-if="isLoading" class="loading-container">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <p>正在生成在线测试，请稍候...</p>
          </div>

          <!-- 生成结果展示 -->
          <div v-else-if="onlineTestResponse" class="result-display">
            <!-- 用户输入 ID -->
            <div class="student-id-content">
              <p class="student-id-prompt">请输入你的ID：</p>
              <el-input v-model="studentId" placeholder="请输入您的 ID"></el-input>
            </div>

            <div class="test-container">
              <div
                v-for="question in onlineTestResponse.questions"
                :key="question.id"
                class="question-container"
              >
                <div class="question-header">
                  <h3>{{ question.number }}、{{ question.type }}</h3>
                </div>
                <div class="question-content">
                  <p>{{ question.id }}（{{ question.score }}分）：{{ question.content }}</p>
                </div>
                <div class="question-options" v-if="question.options">
                  <template v-if="question.type === '选择题' || question.type === '判断题'">
                    <el-radio-group v-model="studentAnswers[question.id]">
                      <div
                        v-for="option in question.options"
                        :key="option.key"
                        class="option-item"
                        style="margin-bottom: 16px;"
                      >
                        <el-radio-button :label="option.key">{{ option.key }} {{ option.value }}</el-radio-button>
                      </div>
                    </el-radio-group>
                  </template>
                  <template v-else-if="question.type === '填空题'">
                    <el-input
                      v-model="studentAnswers[question.id]"
                      placeholder="请输入答案"
                    ></el-input>
                  </template>
                  <template v-else-if="question.type === '简答题' || question.type === '应用计算题'">
                    <el-input
                      type="textarea"
                      v-model="studentAnswers[question.id]"
                      placeholder="请输入答案"
                    ></el-input>
                  </template>
                </div>
              </div>
              <el-button type="primary" @click="submitAnswers">提交答案</el-button>
            </div>
          </div>

          <!-- 提示信息 -->
          <div v-else>
            <p>在线测试生成失败，请检查输入是否正确。</p>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 3. 提交答案后的结果展示 -->
    <div v-if="showResult" class="result-container">
      <el-card class="box-card back-card">
        <el-button class="back-button" type="text" @click="resetState">&lt;&lt; 返回</el-button>
      </el-card>

      <!-- 批改结果展示 -->
      <el-card class="box-card result-card">
        <template #header>
          <div class="card-header">
            <span>批改结果</span>
          </div>
        </template>
        <div class="result-content">
          <div v-if="gradingResult">
            <p><strong>学生 ID：</strong>{{ gradingResult.student_id }}</p>
            <p><strong>试卷 ID：</strong>{{ gradingResult.exam_id }}</p>
            <p><strong>总分：</strong>{{ gradingResult.score_summary.total_score }} / {{ gradingResult.score_summary.total_possible }}</p>
            <p><strong>客观题得分：</strong>{{ gradingResult.score_summary.objective_score }} / {{ gradingResult.score_summary.objective_total }}</p>
            <p><strong>主观题得分：</strong>{{ gradingResult.score_summary.subjective_score }} / {{ gradingResult.score_summary.subjective_total }}</p>
            <p><strong>状态：</strong>{{ gradingResult.status }}</p>
          </div>
        </div>
      </el-card>

      <!-- 详细批改结果 -->
      <el-card class="box-card result-card">
        <template #header>
          <div class="card-header">
            <span>题目详细批改</span>
          </div>
        </template>
        <div class="result-content">
          <div
            v-for="detail in gradingResult?.question_details"
            :key="detail.exam_question_id"
            class="question-result"
          >
            <div class="detail-item">
              <span class="label">题目 ID：</span>
              <span>{{ detail.exam_question_id }}</span>
            </div>
            <div class="detail-item">
              <span class="label">题目类型：</span>
              <span>{{ detail.question_type }}</span>
            </div>
            <div class="detail-item">
              <span class="label">题目内容：</span>
              <span>{{ detail.content }}</span>
            </div>
            <div class="detail-item">
              <span class="label">学生答案：</span>
              <span>{{ detail.student_answer }}</span>
            </div>
            <div class="detail-item">
              <span class="label">正确答案：</span>
              <span>{{ detail.correct_answer }}</span>
            </div>
            <div class="detail-item">
              <span class="label">解析：</span>
              <span>{{ detail.explanation }}</span>
            </div>
            <div class="detail-item">
              <span class="label">得分：</span>
              <span>{{ detail.final_score }} / {{ detail.assigned_score }}</span>
            </div>
            <div class="detail-item">
              <span class="label">状态：</span>
              <span>{{ detail.status }}</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { generateOnlineTest, gradeStudentAnswers } from "@/api/examService";
import type { OnlineTestRequest, OnlineTestResponse, GradingResult } from "@/types/exam";
import { Loading, Edit } from "@element-plus/icons-vue";

const showOnlineTestForm = ref(false); // 控制表单弹窗的显示
const onlineTestRequest = ref<OnlineTestRequest>({
  subject: "",
  topic: "",
  degree: "",
  time_limit: 60,
  questions: {
    choice: { count: 0, score: 0 },
    fill: { count: 0, score: 0 },
    judge: { count: 0, score: 0 },
    short_answer: { count: 0, score: 0 },
    application: { count: 0, score: 0 },
  },
});
const onlineTestResponse = ref<OnlineTestResponse | null>(null);
const isLoading = ref(false);
const isGenerating = ref(false);
const isTimerStarted = ref(false); // 标记倒计时是否已开始

const studentAnswers = ref<Record<number, string>>({});
const studentId = ref(""); // 用户输入的 ID
const showResult = ref(false); // 控制提交答案后结果的显示
const gradingResult = ref<GradingResult | null>(null); // 使用新类型

// 倒计时相关逻辑
const timeLimitInSeconds = ref(0); // 倒计时的初始时间（秒）
const remainingTime = ref(0); // 剩余时间
const intervalId = ref<number | undefined>(undefined); // 定时器 ID，类型为 number 或 undefined

const formattedTime = computed(() => {
  const hours = Math.floor(remainingTime.value / 3600);
  const minutes = Math.floor((remainingTime.value % 3600) / 60);
  const seconds = remainingTime.value % 60;
  return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
});

const startTimerAndShowQuestions = () => {
  if (!onlineTestResponse.value) {
    alert("请先生成在线测试！");
    return;
  }
  isTimerStarted.value = true; // 标记倒计时已开始
  startTimer(); // 开始倒计时
};

const startTimer = () => {
  if (intervalId.value) return; // 如果已经在运行，不再重复启动
  intervalId.value = window.setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--;
    } else {
      clearInterval(intervalId.value);
      intervalId.value = undefined;
      alert("时间到，已自动提交。");
      submitAnswers(); // 自动提交答案
    }
  }, 1000);
};

const stopTimer = () => {
  if (intervalId.value) {
    clearInterval(intervalId.value); // 清除定时器
    intervalId.value = undefined; // 将定时器 ID 设置为 undefined
  }
};

const handleGenerateOnlineTest = async () => {
  showOnlineTestForm.value = false; // 关闭表单弹窗
  isGenerating.value = true; // 设置标志变量，表示正在生成

  try {
    isLoading.value = true;
    const result = await generateOnlineTest(onlineTestRequest.value);
    if (result) {
      onlineTestResponse.value = result; // 如果后端返回成功，显示结果
      timeLimitInSeconds.value = result.test_info.time_limit * 60; // 设置倒计时时间
      remainingTime.value = timeLimitInSeconds.value; // 初始化剩余时间
      isTimerStarted.value = false; // 重置倒计时状态
    } else {
      onlineTestResponse.value = null; // 如果后端返回失败，显示失败提示
    }
  } catch (error) {
    console.error("生成在线测试失败:", error);
    onlineTestResponse.value = null; // 如果请求失败，显示失败提示
  } finally {
    isLoading.value = false;
    isGenerating.value = false; // 重置生成状态
  }
};

const submitAnswers = () => {
  const answers = onlineTestResponse.value?.questions.map((question) => ({
    exam_question_id: question.id,
    question_type: question.type,
    answer_data: {
      selected_option: question.type === "选择题" || question.type === "判断题" ? studentAnswers.value[question.id] : undefined,
      filled_answers: question.type === "填空题" ? [studentAnswers.value[question.id]] : undefined,
      content: question.type === "简答题" || question.type === "应用计算题" ? studentAnswers.value[question.id] : undefined,
    },
  }));

  if (answers && onlineTestResponse.value) {
    const gradingRequest = {
      exam_id: onlineTestResponse.value.exam_id,
      student_id: studentId.value,
      answers: answers,
    };

    gradeStudentAnswers(gradingRequest)
      .then((response) => {
        console.log("评分结果:", response);
        gradingResult.value = response; // 确保 response 的结构与 GradingResult 类型一致
        showResult.value = true; // 显示批改结果
      })
      .catch((error) => {
        console.error("提交答案失败:", error);
        alert("提交答案失败，请稍后再试");
      });
  }
};

const resetState = () => {
  showOnlineTestForm.value = false;
  onlineTestResponse.value = null;
  isGenerating.value = false;
  studentAnswers.value = {};
  studentId.value = ""; // 清空用户输入的 ID
  showResult.value = false; // 隐藏批改结果
  gradingResult.value = null; // 清空批改结果
  stopTimer(); // 停止倒计时器
};
</script>

<style scoped>
.online-test-section {
  padding: 20px;
  font-family: "Arial", sans-serif;
  color: #333;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.intro-text {
  text-align: center;
  margin-bottom: 20px;
}

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

.feature-box h1 {
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

.box-card {
  width: 800px;
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
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.question-result {
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.question-result:last-child {
  border-bottom: none;
}

.back-button {
  font-size: 16px;
  color: #1677ff;
  text-decoration: none;
  cursor: pointer;
}

.option-item {
  margin-bottom: 16px; /* 增加选项间距 */
}

.student-id-prompt {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.detail-item .label {
  font-weight: bold;
  margin-right: 8px;
  white-space: nowrap;
}
</style>
