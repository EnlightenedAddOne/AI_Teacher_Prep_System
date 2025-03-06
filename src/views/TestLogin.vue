<script lang="ts" setup>
import { ref, computed } from "vue";
import type { OnlineTestRequest, OnlineTestResponse, GradingResult } from "@/types/exam";
import { Loading, Edit } from "@element-plus/icons-vue";

const showOnlineTestForm = ref(false);
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
const isTimerStarted = ref(false);

const studentAnswers = ref<Record<number, string>>({});
const studentId = ref("");
const showResult = ref(false);
const gradingResult = ref<GradingResult | null>(null);

// 模拟后端返回的在线测试数据
const mockOnlineTestResponse: OnlineTestResponse = {
  exam_id: 2,
  questions: [
    {
      number: "一",
      type: "选择题",
      score: 2,
      id: 1,
      content: "已知函数f(x) = ax^2 + bx + c，若其图像通过点(1, 3)和(-1, 5)，则a + b + c的值为：",
      options: [
        { key: "A", value: "3" },
        { key: "B", value: "4" },
        { key: "C", value: "5" },
        { key: "D", value: "6" },
      ],
      correct_answer: "B",
      explanation: "根据题目条件，代入点(1, 3)和(-1, 5)可以得到两个方程：a + b + c = 3 和 a - b + c = 5。解这两个方程可得a + b + c = 4。",
      knowledge_points: ["方程求解"],
      subject: "数学",
      topic: "函数",
      degree: "困难",
    },
    {
      number: "二",
      type: "填空题",
      score: 3,
      id: 6,
      content: "设函数f(x) = x^2 + 2x + 1，则f(-1) = ________。",
      options: null,
      correct_answer: "0",
      explanation: "直接代入x = -1计算，f(-1) = (-1)^2 + 2*(-1) + 1 = 0。",
      knowledge_points: ["函数求值"],
      subject: "数学",
      topic: "函数",
      degree: "困难",
    },
    {
      number: "三",
      type: "判断题",
      score: 1,
      id: 9,
      content: "函数f(x) = x^2在其定义域内是单调递增的。",
      options: [
        { key: "A", value: "√" },
        { key: "B", value: "×" },
      ],
      correct_answer: "B",
      explanation: "二次函数f(x) = x^2在x < 0时是单调递减的，在x > 0时是单调递增的。",
      knowledge_points: ["二次函数"],
      subject: "数学",
      topic: "函数",
      degree: "困难",
    },
    {
      number: "四",
      type: "简答题",
      score: 5,
      id: 13,
      content: "解释为什么函数f(x) = e^x在其定义域内是严格递增的。",
      options: null,
      correct_answer: "因为e^x的导数为e^x，而e^x总是大于0，所以e^x在其定义域内始终是严格递增的。",
      explanation: "指数函数e^x的导数为e^x，且e^x > 0对于所有x成立，因此e^x在其定义域内是严格递增的。",
      knowledge_points: ["单调性"],
      subject: "数学",
      topic: "函数",
      degree: "困难",
    },
    {
      number: "五",
      type: "应用计算题",
      score: 10,
      id: 15,
      content: "给定函数f(x) = x^3 - 3x^2 + 2x，求其在区间[-1, 2]上的最大值和最小值。",
      options: null,
      correct_answer: "最大值为f(2) = 2，最小值为f(1) = 0。",
      explanation: "首先求导f'(x) = 3x^2 - 6x + 2，令f'(x) = 0解得驻点x = 1 ± √(2/3)。然后计算端点值f(-1) = -6，f(2) = 2，以及驻点值f(1 - √(2/3)) ≈ 0.385，f(1 + √(2/3)) ≈ 0.385。比较这些值，最大值为f(2) = 2，最小值为f(1) = 0。",
      knowledge_points: ["多项式函数"],
      subject: "数学",
      topic: "函数",
      degree: "困难",
    },
  ],
  test_info: {
    total_score: 53,
    time_limit: 45,
  },
};

// 模拟后端返回的批改结果数据
const mockGradingResult: GradingResult = {
  record_id: 21,
  student_id: "1",
  exam_id: 2,
  status: "pending_manual",
  score_summary: {
    objective_score: 11.0,
    objective_total: 14.0,
    subjective_score: 36.5,
    subjective_total: 39.0,
    total_score: 47.5,
    total_possible: 53.0,
  },
  question_details: [
    {
      exam_question_id: 17,
      question_type: "single_choice",
      content: "设函数f(x) = x^3 - 3x + 1，则f(x)在区间[-2, 2]上的最大值为：",
      assigned_score: 2.0,
      student_answer: "D",
      correct_answer: "B",
      explanation: "求导f'(x) = 3x^2 - 3，令f'(x) = 0得驻点x = ±1。计算端点和驻点处的函数值，f(-2) = -1, f(2) = 3, f(1) = -1, f(-1) = 3，因此最大值为f(2)=5。",
      final_score: 0.0,
      status: "graded",
    },
    {
      exam_question_id: 18,
      question_type: "single_choice",
      content: "已知f(x)是一个偶函数，且满足f(x+2) = f(x)，则下列选项正确的是：",
      assigned_score: 2.0,
      student_answer: "A",
      correct_answer: "A",
      explanation: "由f(x+2) = f(x)可知f(x)是以2为周期的周期函数，同时f(x)是偶函数，进一步说明其具有对称性。",
      final_score: 2.0,
      status: "graded",
    },
    {
      exam_question_id: 19,
      question_type: "single_choice",
      content: "若函数f(x) = ax^2 + bx + c (a≠0)的图像关于直线x=1对称，则b的值为：",
      assigned_score: 2.0,
      student_answer: "A",
      correct_answer: "A",
      explanation: "二次函数的对称轴为x = -b/(2a)，由题目条件x=1可得-b/(2a) = 1，解得b = -2a。",
      final_score: 2.0,
      status: "graded",
    },
    {
      exam_question_id: 20,
      question_type: "single_choice",
      content: "设f(x) = |x| + |x-1|，则f(x)的最小值为：",
      assigned_score: 2.0,
      student_answer: "B",
      correct_answer: "B",
      explanation: "分段讨论f(x)，当x≤0时f(x) = -2x+1，当0<x<1时f(x) = 1，当x≥1时f(x) = 2x-1，最小值出现在x=0或x=1，f(x) = 1。",
      final_score: 2.0,
      status: "graded",
    },
    {
      exam_question_id: 21,
      question_type: "single_choice",
      content: "设f(x)是定义在R上的奇函数，且f(x+2) = -f(x)，则f(x)的周期为：",
      assigned_score: 2.0,
      student_answer: "B",
      correct_answer: "B",
      explanation: "由f(x+2) = -f(x)，再代入f(x+4) = -f(x+2) = f(x)，可得f(x)的周期为4。",
      final_score: 2.0,
      status: "graded",
    },
    {
      exam_question_id: 22,
      question_type: "fill_blank",
      content: "设函数f(x) = e^x / (e^x + 1)，则f(x)的反函数f^-1(x)为__________。",
      assigned_score: 3.0,
      student_answer: "ln(x/(1-x))",
      correct_answer: "ln(x / (1-x))",
      explanation: "令y = f(x)，即y = e^x / (e^x + 1)，解出x = ln(y / (1-y))，故f^-1(x) = ln(x / (1-x))。",
      final_score: 3.0,
      status: "graded",
    },
    {
      exam_question_id: 23,
      question_type: "fill_blank",
      content: "已知f(x) = sin(x) + cos(x)，则f(x)的最大值为__________。",
      assigned_score: 3.0,
      student_answer: "√2",
      correct_answer: "√2",
      explanation: "利用辅助角公式，f(x) = √2sin(x + π/4)，最大值为√2。",
      final_score: 3.0,
      status: "graded",
    },
    {
      exam_question_id: 24,
      question_type: "fill_blank",
      content: "设f(x) = x^3 - 6x^2 + 9x + 1，则f(x)的拐点坐标为__________。",
      assigned_score: 3.0,
      student_answer: "(2,3)",
      correct_answer: "(2, 3)",
      explanation: "求二阶导数f''(x) = 6x - 12，令f''(x) = 0得x = 2，代入f(x)得拐点为(2, 3)。",
      final_score: 3.0,
      status: "graded",
    },
    {
      exam_question_id: 25,
      question_type: "judgment",
      content: "若f(x)是定义在R上的偶函数，则f(x)的导数f'(x)也是偶函数。",
      assigned_score: 1.0,
      student_answer: "A",
      correct_answer: "B",
      explanation: "偶函数的导数是奇函数，而非偶函数。",
      final_score: 0.0,
      status: "graded",
    },
    {
      exam_question_id: 26,
      question_type: "judgment",
      content: "若f(x)是定义在R上的单调递增函数，则f(x)必然是连续函数。",
      assigned_score: 1.0,
      student_answer: "B",
      correct_answer: "B",
      explanation: "单调递增函数未必连续，例如分段函数可能不连续。",
      final_score: 1.0,
      status: "graded",
    },
    {
      exam_question_id: 27,
      question_type: "judgment",
      content: "若f(x)是周期函数，则f(x)的导数f'(x)也是周期函数。",
      assigned_score: 1.0,
      student_answer: "A",
      correct_answer: "A",
      explanation: "周期函数的导数仍是周期函数，且周期相同。",
      final_score: 1.0,
      status: "graded",
    },
    {
      exam_question_id: 28,
      question_type: "judgment",
      content: "若f(x)是定义在R上的奇函数，则f(x)的积分F(x)也是奇函数。",
      assigned_score: 1.0,
      student_answer: "B",
      correct_answer: "B",
      explanation: "奇函数的积分是偶函数，而非奇函数。",
      final_score: 1.0,
      status: "graded",
    },
    {
      exam_question_id: 29,
      question_type: "short_answer",
      content: "证明：若f(x)是定义在R上的偶函数，则f'(x)是奇函数。",
      assigned_score: 5.0,
      student_answer: "设f(x)是偶函数，则f(-x) = f(x)。对等式两边求导数，得到：f'(-x)·(-1) = f'(x)，即f'(-x) = -f'(x)。这表明f'(x)是奇函数，因为奇函数的定义就是g(-x) = -g(x)。因此，偶函数的导数是奇函数。",
      correct_answer: "设f(x)是偶函数，则f(-x) = f(x)。两边求导得-f'(-x) = f'(x)，即f'(-x) = -f'(x)，故f'(x)是奇函数。",
      explanation: "设f(x)是偶函数，则f(-x) = f(x)。两边求导得-f'(-x) = f'(x)，即f'(-x) = -f'(x)，故f'(x)是奇函数。",
      final_score: 5.0,
      status: "graded",
    },
    {
      exam_question_id: 30,
      question_type: "short_answer",
      content: "已知f(x) = x^3 - 3x^2 + 2x，求f(x)的所有零点及其对应的重数。",
      assigned_score: 5.0,
      student_answer: "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。",
      correct_answer: "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。",
      explanation: "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。",
      final_score: 5.0,
      status: "graded",
    },
    {
      exam_question_id: 31,
      question_type: "application",
      content: "已知函数f(x) = x^3 - 6x^2 + 9x + C，其中C为常数，若f(x)在x=1处取得极小值，求C的值以及f(x)的极值点和极值。",
      assigned_score: 10.0,
      student_answer: "求导得f'(x) = 3x^2 - 12x + 9，令f'(x) = 0，得3(x^2 - 4x + 3) = 0，解得x = 1或x = 3。计算二阶导数f''(x) = 6x - 12，当x = 1时，f''(1) = -6 < 0，所以x = 1是极大值点；当x = 3时，f''(3) = 6 > 0，所以x = 3是极小值点。由于题目要求f(x)在x = 1处取得极小值，所以C的值应使得f''(1) > 0。但是f''(x) = 6x - 12只与x有关，与C无关。如果假设x = 1是极小值点，则C = -4，此时f(1) = 0，f(3) = 4。",
      correct_answer: "求导f'(x) = 3x^2 - 12x + 9，令f'(x) = 0得x = 1或x = 3。由f''(x) = 6x - 12可知x=1为极小值点，代入f(1) = C+4，由于f(1)为极小值，故C=-4，极值点为x=1，极小值为0；极值点为x=3，极大值为4。",
      explanation: "求导f'(x) = 3x^2 - 12x + 9，令f'(x) = 0得x = 1或x = 3。由f''(x) = 6x - 12可知x=1为极小值点，代入f(1) = C+4，由于f(1)为极小值，故C=-4，极值点为x=1，极小值为0；极值点为x=3，极大值为4。",
      final_score: 7.5,
      status: "graded",
    },
    {
      exam_question_id: 32,
      question_type: "application",
      content: "已知f(x) = e^x - x^2，求证f(x)在区间(0, +∞)上单调递增，并求f(x)的最小值。",
      assigned_score: 10.0,
      student_answer: "求导得f'(x) = e^x - 2x。对于任意x > 0，我们有e^x > 1 + x（泰勒展开的性质）。当x > 0时，1 + x > 2x仅在0 < x < 1时成立。但即使在0 < x < 1区间，我们仍有e^x > 1 + x > 2x，所以f'(x) = e^x - 2x > 0。当x ≥ 1时，e^x增长速度远大于2x，所以f'(x) > 0仍然成立。因此，在整个区间(0, +∞)上，f'(x) > 0，函数f(x)单调递增。函数的最小值出现在区间的左端点x = 0处，f(0) = e^0 - 0^2 = 1。",
      correct_answer: "求导f'(x) = e^x - 2x，在(0, +∞)上，e^x增长速度大于2x，故f'(x) > 0，f(x)单调递增。f(x)的最小值出现在x=0，f(0) = 1。",
      explanation: "求导f'(x) = e^x - 2x，在(0, +∞)上，e^x增长速度大于2x，故f'(x) > 0，f(x)单调递增。f(x)的最小值出现在x=0，f(0) = 1。",
      final_score: 10.0,
      status: "graded",
    },
  ],
};

// 模拟数据赋值
onlineTestResponse.value = mockOnlineTestResponse;
gradingResult.value = mockGradingResult;
showResult.value = true;

// 定义方法
const handleGenerateOnlineTest = () => {
  console.log("生成在线测试");
  // 在这里实现生成在线测试的逻辑
};

const resetState = () => {
  console.log("重置状态");
  // 在这里实现重置状态的逻辑
};

const submitAnswers = () => {
  console.log("提交答案");
  // 在这里实现提交答案的逻辑
};

const startTimerAndShowQuestions = () => {
  console.log("开始倒计时");
  // 在这里实现倒计时逻辑
};

const remainingTime = ref(0); // 剩余时间
const formattedTime = computed(() => {
  const minutes = Math.floor(remainingTime.value / 60);
  const seconds = remainingTime.value % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
});
</script>


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
      <el-card class="box-card back-card" style="margin-bottom: 20px;">
        <el-button class="back-button" type="text" @click="resetState">&lt;&lt; 返回</el-button>
      </el-card>

      <!-- 倒计时器 -->
      <el-card class="box-card timer-card" style="margin-bottom: 20px;">
        <template #header>
          <div class="card-header">
            <span>倒计时</span>
          </div>
        </template>
        <div class="timer-content">
          <div v-if="!isTimerStarted && onlineTestResponse">
            <p>题目已经生成，请点击下方开始按钮开始答题。</p>
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
      <el-card class="box-card result-card" style="margin-bottom: 20px;">
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
                  <p>题目类型：{{ question.type }}</p> <!-- 调试信息 -->
                </div>
                <div class="question-options" v-if="question.options">
                  <template v-if="question.type === '选择题' || question.type === '判断题'">
                    <el-radio-group v-model="studentAnswers[question.id]">
                      <div
                        v-for="option in question.options"
                        :key="option.key"
                        class="option-item"
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
      <el-card class="box-card back-card" style="margin-bottom: 20px;">
        <el-button class="back-button" type="text" @click="resetState">&lt;&lt; 返回</el-button>
      </el-card>

      <!-- 批改结果展示 -->
      <el-card class="box-card result-card" style="margin-bottom: 20px;">
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
      <el-card class="box-card result-card" style="margin-bottom: 20px;">
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
            <p><strong>题目 ID：</strong>{{ detail.exam_question_id }}</p>
            <p><strong>题目类型：</strong>{{ detail.question_type }}</p>
            <p><strong>题目内容：</strong>{{ detail.content }}</p>
            <p><strong>学生答案：</strong>{{ detail.student_answer }}</p>
            <p><strong>正确答案：</strong>{{ detail.correct_answer }}</p>
            <p><strong>解析：</strong>{{ detail.explanation }}</p>
            <p><strong>得分：</strong>{{ detail.final_score }} / {{ detail.assigned_score }}</p>
            <p><strong>状态：</strong>{{ detail.status }}</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

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
  margin-bottom: 20px; /* 添加间距 */
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  margin-bottom: 20px; /* 添加间距 */
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
  height: 150px; /* 增加高度 */
  justify-content: center; /* 水平居中 */
  height: 100px;
  padding: 20px;
}

.loading-icon {
  animation: spin 1s infinite linear;
  font-size: 48px;
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
  border: 1px solid #ddd; /* 添加边框 */
  padding: 10px; /* 增加内边距 */
  margin-bottom: 20px; /* 增加间距 */
  background-color: #f9f9f9; /* 添加背景色 */
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
  margin-bottom: 16px; /* 增加间距 */
}
</style>
