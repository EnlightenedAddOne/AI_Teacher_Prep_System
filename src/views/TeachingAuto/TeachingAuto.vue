<template>
  <div class="teaching-design-section">
    <!-- 进度条 -->
    <el-card class="progress-card">
      <el-steps :active="active" finish-status="success" align-center>
        <el-step title="填写教案生成需求" />
        <el-step title="生成教案" />
        <el-step title="保存教案" />
      </el-steps>
    </el-card>

    <!-- 教案生成需求和结果 -->
    <div class="content-container">
      <!-- 教案生成需求 -->
      <el-card class="box-card request-card">
        <template #header>
          <div class="card-header">
            <span>教案生成需求</span>
          </div>
        </template>
        <el-form ref="teachingDesignForm" :model="teachingDesignRequest" label-width="120px" class="form-content">
          <el-form-item label="科目">
            <el-input v-model="teachingDesignRequest.subject" placeholder="请输入科目"></el-input>
          </el-form-item>
          <el-form-item label="主题">
            <el-input v-model="teachingDesignRequest.topic" placeholder="请输入主题"></el-input>
          </el-form-item>
          <el-form-item label="教学目标">
            <el-input v-model="teachingDesignRequest.goals" type="textarea" placeholder="请输入教学目标"></el-input>
          </el-form-item>
          <el-form-item label="时长">
            <el-input v-model="teachingDesignRequest.duration" placeholder="请输入时长"></el-input>
          </el-form-item>
          <el-form-item label="年级">
            <el-input v-model="teachingDesignRequest.grade" placeholder="请输入年级"></el-input>
          </el-form-item>
          <el-form-item label="是否包含图片">
            <el-switch v-model="teachingDesignRequest.with_images" />
          </el-form-item>
          <el-form-item label="图片数量" v-if="teachingDesignRequest.with_images">
            <el-select v-model="teachingDesignRequest.image_count">
              <el-option v-for="n in 10" :key="n" :label="n.toString()" :value="n" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleGenerateTeachingDesign">生成教学设计</el-button>
            <el-button type="danger" @click="handleCancelGeneration">取消生成</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 教案生成结果 -->
      <el-card class="box-card result-card">
        <template #header>
          <div class="card-header">
            <span>教案生成结果</span>
            <el-button
              v-if="teachingDesignResponse"
              type="primary"
              @click="saveTeachingDesign"
              style="float: right;"
            >
              保存教案
            </el-button>
          </div>
        </template>
        <div class="result-content">
          <!-- 加载动画 -->
          <div v-if="isLoading" class="loading-container">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <p>正在火速生成教案，请稍候...</p>
          </div>

          <!-- 生成结果为空时的提示 -->
          <div v-else-if="!teachingDesignResponse" class="empty-state">
            <p>请填写左侧表格并生成教案。</p>
          </div>

          <!-- 生成结果展示 -->
          <div v-else>
            <el-button type="success" @click="downloadPdf('teaching_design.pdf')">下载 PDF</el-button>
            <div v-if="teachingDesignResponse.image_path" class="image-container">
              <h3>教学设计图片</h3>
              <img :src="teachingDesignResponse.image_path" alt="教学设计图片" class="design-image">
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { generateTeachingDesign, downloadPdf as apiDownloadPdf } from '@/api/examService';
import type { TeachingDesignRequest, TeachingDesignResponse } from '@/types/exam';
import { Loading } from '@element-plus/icons-vue'; // 引入加载图标

const active = ref(0); // 当前步骤
const teachingDesignRequest = ref<TeachingDesignRequest>({
  subject: '',
  topic: '',
  goals: '',
  duration: '',
  grade: '',
  with_images: false,
  image_count: 5
});

const teachingDesignResponse = ref<TeachingDesignResponse | null>(null);
const isLoading = ref(false);

const handleGenerateTeachingDesign = async () => {
  active.value = 1; // 更新进度条到步骤2
  isLoading.value = true; // 开始加载提示
  try {
    teachingDesignResponse.value = await generateTeachingDesign(teachingDesignRequest.value);
    active.value = 2; // 更新进度条到步骤3
  } catch (error) {
    console.error('生成教学设计失败:', error);
  } finally {
    isLoading.value = false; // 结束加载提示
  }
};

const handleCancelGeneration = () => {
  active.value = 0; // 重置进度条
  teachingDesignRequest.value = { // 重置请求数据
    subject: '',
    topic: '',
    goals: '',
    duration: '',
    grade: '',
    with_images: false,
    image_count: 5
  };
  teachingDesignResponse.value = null; // 清空教案生成结果
  isLoading.value = false; // 关闭加载状态
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

const saveTeachingDesign = () => {
  active.value = 3; // 更新进度条到步骤3
  // 这里要记得补充保存教案的逻辑
  alert('教案已保存！');
};
</script>

<style scoped>
.teaching-design-section {
  padding: 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

.progress-card {
  margin-bottom: 20px;
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

.image-container {
  margin-top: 20px;
  text-align: center;
}

.design-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  margin-top: 0px;
}

.content-container {
  display: flex;
  gap: 20px;
}

.request-card {
  flex: 1;
}

.result-card {
  flex: 1;
}

.empty-state {
  text-align: center;
  color: #999;
  font-size: 16px;
}
</style>
