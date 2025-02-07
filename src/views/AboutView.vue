<script lang="ts">
import axios from 'axios';

interface Exam {
  exam_id: number;
  exam_name: string;
  subject_name: string;
  total_score: number;
  time_limit: number;
  questions: Question[];
}

interface Question {
  id: number;
  content: string;
  score: number;
  options: Option[];
}

interface Option {
  key: string;
  value: string;
  correct: boolean;
}

export default {
  data() {
    return {
      exams: [] as Exam[],
      examDetail: null as Exam | null,
      showExamDetail: true,
      newExamName: '',
      newExamSubject: '',
      newExamTimeLimit: 90,
      newExamTotalScore: 100
    };
  },
  methods: {
    async fetchExams(): Promise<void> {
      try {
        const response = await axios.get<Exam[]>('http://localhost:5000/exam');
        if (Array.isArray(response.data)) {
          this.exams = response.data;
        } else {
          console.error('Invalid data format:', response.data);
          this.exams = [];
        }
      } catch (error) {
        console.error('加载试卷失败:', error);
        alert('加载试卷失败');
      }
    },
    async fetchExamDetail(examId: number): Promise<void> {
      try {
        const response = await axios.get<Exam>(`http://localhost:5000/exam/${examId}`);
        this.examDetail = response.data;
        this.showExamDetail = true;
      } catch (error) {
        console.error('加载试卷详情失败:', error);
        this.examDetail = null;
        alert('内容已删除');
      }
    },
    async deleteExam(examId: number): Promise<void> {
      try {
        const response = await axios.delete(`http://localhost:5000/exam/${examId}`);
        if (response.status === 200) {
          alert('试卷删除成功');
          this.fetchExams(); // 刷新试卷列表
          if (this.examDetail && this.examDetail.exam_id === examId) {
            this.examDetail = null;
          }
        }
      } catch (error) {
        console.error('删除试卷失败:', error);
        alert('删除试卷失败');
      }
    },
    async importExam(): Promise<void> {
      if (!this.newExamName || !this.newExamSubject) {
        alert('试卷名称和科目名称不能为空');
        return;
      }
      try {
        const jsonData = {
          exam_name: this.newExamName,
          subject_name: this.newExamSubject,
          total_score: this.newExamTotalScore,
          time_limit: this.newExamTimeLimit,
          questions: [
            {
              subject: this.newExamSubject,
              type: 'single_choice',
              content: '示例题目',
              explanation: '示例解析',
              degree: '中等',
              topic: '示例专题',
              number: '1',
              score: 10,
              options: [
                { key: 'A', value: '选项A', correct: true },
                { key: 'B', value: '选项B', correct: false }
              ],
              knowledge_points: ['示例知识点']
            }
          ]
        };
        console.log('Sending data:', jsonData); // 打印发送的数据
        const response = await axios.post('http://localhost:5000/exam', jsonData);
        console.log('Response:', response.data); // 打印后端返回的响应
        if (response.status === 200) {
          alert('试卷导入成功');
          this.fetchExams(); // 刷新试卷列表
        }
      } catch (error) {
        console.error('导入试卷失败:', error);
        alert('导入试卷失败');
      }
    },
    toggleExamDetail(): void {
      this.showExamDetail = !this.showExamDetail;
    }
  }
};
</script>

<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>教育应用</h1>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>试卷列表</span>
              <el-button type="primary" @click="fetchExams">加载试卷</el-button>
            </div>
          </template>
          <el-table :data="exams" style="width: 100%">
            <el-table-column prop="exam_id" label="ID" width="180" />
            <el-table-column prop="exam_name" label="试卷名称" />
            <el-table-column prop="subject_name" label="科目" />
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button link @click="fetchExamDetail(scope.row.exam_id)">查看</el-button>
                <el-button link @click="deleteExam(scope.row.exam_id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <el-card v-if="examDetail" class="mt-4">
          <template #header>
            <div class="card-header">
              <span>试卷详情</span>
              <el-button link @click="toggleExamDetail">收起</el-button>
            </div>
          </template>
          <div v-if="showExamDetail">
            <h3 v-if="examDetail">{{ examDetail.exam_name }}</h3>
            <p v-if="examDetail">总分: {{ examDetail.total_score }}</p>
            <p v-if="examDetail">时间限制: {{ examDetail.time_limit }} 分钟</p>
            <el-table v-if="examDetail" :data="examDetail.questions" style="width: 100%">
              <el-table-column prop="id" label="ID" width="180" />
              <el-table-column prop="content" label="题目" />
              <el-table-column prop="score" label="分数" />
            </el-table>
            <p v-else>内容已删除</p>
          </div>
        </el-card>

        <el-card class="mt-4">
          <template #header>
            <div class="card-header">
              <span>新增试卷</span>
            </div>
          </template>
          <el-form>
            <el-form-item label="试卷名称">
              <el-input v-model="newExamName" placeholder="试卷名称" />
            </el-form-item>
            <el-form-item label="科目名称">
              <el-input v-model="newExamSubject" placeholder="科目名称" />
            </el-form-item>
            <el-form-item label="考试时间（分钟）">
              <el-input v-model.number="newExamTimeLimit" placeholder="考试时间" type="number" />
            </el-form-item>
            <el-form-item label="总分">
              <el-input v-model.number="newExamTotalScore" placeholder="总分" type="number" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="importExam">导入试卷</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mt-4 {
  margin-top: 20px;
}
</style>
