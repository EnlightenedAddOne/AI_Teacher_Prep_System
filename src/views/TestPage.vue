<script lang="ts" setup>
import { ref } from 'vue';
import { generateTeachingDesign, downloadPdf as apiDownloadPdf } from '@/api/examService';
import type { TeachingDesignRequest, TeachingDesignResponse } from '@/types/exam';

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
  isLoading.value = true;
  try {
    teachingDesignResponse.value = await generateTeachingDesign(teachingDesignRequest.value);
  } catch (error) {
    console.error('生成教学设计失败:', error);
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

<template>
  <div class="teaching-design-section">
    <!-- 教学设计表单 -->
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>教案生成需求</span>
        </div>
      </template>
      <el-form ref="teachingDesignForm" :model="teachingDesignRequest" label-width="120px">
        <el-form-item label="科目">
          <el-input v-model="teachingDesignRequest.subject" placeholder="请输入科目"></el-input>
        </el-form-item>
        <el-form-item label="主题">
          <el-input v-model="teachingDesignRequest.topic" placeholder="请输入主题"></el-input>
        </el-form-item>
        <el-form-item label="教学目标">
          <el-input v-model="teachingDesignRequest.goals" placeholder="请输入教学目标"></el-input>
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
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 加载中提示 -->
    <el-card class="box-card" v-if="isLoading">
      <template #header>
        <div class="card-header">
          <span>生成中...</span>
        </div>
      </template>
      <div class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>
    </el-card>

    <!-- 教学设计结果 -->
    <el-card class="box-card" v-if="teachingDesignResponse">
      <template #header>
        <div class="card-header">
          <span>教案生成结果</span>
        </div>
      </template>
      <div class="result-content">
        <el-button type="success" @click="downloadPdf('teaching_design.pdf')">下载 PDF</el-button>
        <div v-if="teachingDesignResponse.image_path" class="image-container">
          <h3>教学设计图片</h3>
          <img :src="teachingDesignResponse.image_path" alt="教学设计图片" class="design-image">
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.teaching-design-section {
  padding: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.result-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-container {
  margin-top: 20px;
}

.design-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
