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
        <el-form
          ref="teachingDesignForm"
          :model="teachingDesignRequest"
          label-width="120px"
          class="form-content"
          :rules="rules"
        >
          <el-form-item label="科目" prop="subject">
            <el-input
              v-model="teachingDesignRequest.subject"
              placeholder="请输入科目"
            ></el-input>
          </el-form-item>
          <el-form-item label="主题" prop="topic">
            <el-input
              v-model="teachingDesignRequest.topic"
              placeholder="请输入主题"
            ></el-input>
          </el-form-item>
          <el-form-item label="教学目标" prop="goals">
            <el-input
              v-model="teachingDesignRequest.goals"
              type="textarea"
              placeholder="请输入教学目标"
            ></el-input>
          </el-form-item>
          <el-form-item label="时长" prop="duration">
            <el-input
              v-model="teachingDesignRequest.duration"
              placeholder="请输入时长"
            ></el-input>
          </el-form-item>
          <el-form-item label="年级" prop="grade">
            <el-input
              v-model="teachingDesignRequest.grade"
              placeholder="请输入年级"
            ></el-input>
          </el-form-item>
          <el-form-item label="是否包含图片">
            <el-switch
              v-model="teachingDesignRequest.with_images"
              @change="handleWithImagesChange"
            />
          </el-form-item>
          <el-form-item
            label="图片数量"
            v-if="teachingDesignRequest.with_images"
          >
            <el-select v-model="teachingDesignRequest.image_count">
              <el-option
                v-for="n in 20"
                :key="n"
                :label="n.toString()"
                :value="n"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="是否生成 PPT 视频">
            <el-switch
              v-model="teachingDesignRequest.ppt_turn_video"
              @change="handlePptVideoChange"
            />
          </el-form-item>
          <el-form-item label="是否推荐资源">
            <el-switch
              v-model="teachingDesignRequest.resource_recommendation.require_books"
              @change="handleBooksChange"
            />
          </el-form-item>
          <el-form-item
            label="推荐书籍数量"
            v-if="teachingDesignRequest.resource_recommendation.require_books"
          >
            <el-select
              v-model="teachingDesignRequest.resource_recommendation.book_count"
            >
              <el-option
                v-for="n in 5"
                :key="n"
                :label="n.toString()"
                :value="n"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="是否推荐论文">
            <el-switch
              v-model="teachingDesignRequest.resource_recommendation.require_papers"
              @change="handlePapersChange"
            />
          </el-form-item>
          <el-form-item
            label="推荐论文数量"
            v-if="teachingDesignRequest.resource_recommendation.require_papers"
          >
            <el-select
              v-model="teachingDesignRequest.resource_recommendation.paper_count"
            >
              <el-option
                v-for="n in 5"
                :key="n"
                :label="n.toString()"
                :value="n"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="是否推荐视频">
            <el-switch
              v-model="teachingDesignRequest.resource_recommendation.require_videos"
              @change="handleVideosChange"
            />
          </el-form-item>
          <el-form-item
            label="推荐视频数量"
            v-if="teachingDesignRequest.resource_recommendation.require_videos"
          >
            <el-select
              v-model="teachingDesignRequest.resource_recommendation.video_count"
            >
              <el-option
                v-for="n in 5"
                :key="n"
                :label="n.toString()"
                :value="n"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="handleGenerateTeachingDesign"
            >
              生成教学设计
            </el-button>
            <el-button
              type="danger"
              @click="handleCancelGeneration"
            >
              取消生成
            </el-button>
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
          <div
            v-else-if="!teachingDesignResponse"
            class="empty-state"
          >
            <p>请填写左侧表格并生成教案。</p>
          </div>

          <!-- 生成结果展示 -->
          <div v-else>
            <!-- 浏览框 -->
            <div class="preview-container">
              <div v-html="formatMarkdown(teachingDesignResponse)"></div>
            </div>
            <!-- 下载按钮 -->
            <el-button
              class="download-button"
              type="success"
              @click="downloadPdf('teaching_design.pdf')"
            >
              下载 PDF
            </el-button>
            <!-- 图片展示 -->
            <div
              v-if="teachingDesignResponse.images"
              class="image-container"
            >
            <h3>教学设计图片</h3>
                <ul>
                  <li
                    v-for="image in teachingDesignResponse.images"
                    :key="image.md5"
                  >
                    <!-- 图片展示 -->
                    <img
                      :src="extractImageUrl(image.url)"
                      :alt="image.title"
                      class="design-image"
                    />
                    <!-- 点击链接 -->
                    <a :href="extractImageUrl(image.url)" target="_blank">
                      查看图片 {{ image.title }}
                    </a>
                    <el-button
                    type="success"
                    @click="downloadImage(image.url)"
                    class="download-image-button"
                    >
                      下载图片
                    </el-button>
                  </li>
                </ul>
            </div>
            <!-- PPT 视频展示 -->
            <div
              v-if="teachingDesignResponse.ppt_video_path"
              class="video-container"
            >
              <h3>PPT 视频</h3>
              <video
                :src="teachingDesignResponse.ppt_video_path"
                controls
              ></video>
            </div>
            <!-- 推荐资源展示 -->
            <div
              v-if="teachingDesignResponse.books"
              class="resource-container"
            >
              <h3>推荐书籍</h3>
              <ul>
                <li
                  v-for="book in teachingDesignResponse.books"
                  :key="book.title"
                >
                  {{ book.title }} - {{ book.authors.join(', ') }}
                </li>
              </ul>
            </div>
            <div
              v-if="teachingDesignResponse.papers"
              class="resource-container"
            >
              <h3>推荐论文</h3>
              <ul>
                <li
                  v-for="paper in teachingDesignResponse.papers"
                  :key="paper.title"
                >
                  {{ paper.title }} - {{ paper.authors.join(', ') }}
                </li>
              </ul>
            </div>
            <div
              v-if="teachingDesignResponse.videos"
              class="resource-container"
            >
              <h3>推荐视频</h3>
              <ul>
                <li
                  v-for="video in teachingDesignResponse.videos"
                  :key="video.title"
                >
                  <a :href="video.url" target="_blank">
                    {{ video.title }}
                  </a>
                </li>
              </ul>
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
import { Loading } from '@element-plus/icons-vue';
import { marked } from 'marked';
import type { FormInstance } from 'element-plus';

const active = ref(0);
const teachingDesignRequest = ref<TeachingDesignRequest>({
  subject: '',
  topic: '',
  goals: '',
  duration: '',
  grade: '',
  with_images: false,
  image_count: 0,
  ppt_turn_video: false,
  resource_recommendation: {
    require_books: false,
    book_count: 0,
    require_papers: false,
    paper_count: 0,
    require_videos: false,
    video_count: 0
  }
});

const teachingDesignResponse = ref<TeachingDesignResponse | null>(null);
const isLoading = ref(false);
const rules = {
  subject: [{ required: true, message: '请输入科目', trigger: 'blur' }],
  topic: [{ required: true, message: '请输入主题', trigger: 'blur' }],
  goals: [{ required: true, message: '请输入教学目标', trigger: 'blur' }],
  duration: [{ required: true, message: '请输入时长', trigger: 'blur' }],
  grade: [{ required: true, message: '请输入年级', trigger: 'blur' }]
};

const teachingDesignForm = ref<FormInstance | null>(null);

const extractImageUrl = (url: string) => {
  const match = url.match(/<url[^>]*>([^<]+)<\/url>/);
  return match ? match[1] : url; // 如果匹配成功，返回提取的 URL，否则返回原始 URL
};

const handleWithImagesChange = () => {
  if (!teachingDesignRequest.value.with_images) {
    teachingDesignRequest.value.image_count = 0;
  }
};

const handlePptVideoChange = () => {
  if (!teachingDesignRequest.value.ppt_turn_video) {

  }
};

const handleBooksChange = () => {
  if (!teachingDesignRequest.value.resource_recommendation.require_books) {
    teachingDesignRequest.value.resource_recommendation.book_count = 0;
  }
};

const handlePapersChange = () => {
  if (!teachingDesignRequest.value.resource_recommendation.require_papers) {
    teachingDesignRequest.value.resource_recommendation.paper_count = 0;
  }
};

const handleVideosChange = () => {
  if (!teachingDesignRequest.value.resource_recommendation.require_videos) {
    teachingDesignRequest.value.resource_recommendation.video_count = 0;
  }
};

const handleGenerateTeachingDesign = async () => {
  if (teachingDesignForm.value) {
    const isValid = await teachingDesignForm.value.validate();
    if (!isValid) {
      alert('请填写完整信息');
      return;
    }
  }

  active.value = 1;
  isLoading.value = true;
  try {
    teachingDesignResponse.value = await generateTeachingDesign(teachingDesignRequest.value);
    active.value = 2;
  } catch (error) {
    console.error('生成教学设计失败:', error);
    alert('生成教学设计失败，请检查输入是否正确');
  } finally {
    isLoading.value = false;
  }
};

const handleCancelGeneration = () => {
  active.value = 0;
  teachingDesignRequest.value = {
    subject: '',
    topic: '',
    goals: '',
    duration: '',
    grade: '',
    with_images: false,
    image_count: 0,
    ppt_turn_video: false,
    resource_recommendation: {
      require_books: false,
      book_count: 0,
      require_papers: false,
      paper_count: 0,
      require_videos: false,
      video_count: 0
    }
  };
  teachingDesignResponse.value = null;
  isLoading.value = false;
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
  active.value = 3;
  alert('教案已保存！');
};

const formatMarkdown = (response: TeachingDesignResponse) => {
  if (response) {
    return marked(response.content);
  }
  return '';
};

const downloadImage = (url: string) => {
  const link = document.createElement('a');
  link.href = url;
  link.download = url.split('/').pop() || 'image'; // 设置下载文件名
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
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

.download-button {
  margin-top: 10px;
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

.preview-container {
  border: 1px solid #ddd;
  padding: 0;
  margin-top: 10px;
  max-height: 300px;
  overflow-y: auto;
  width: calc(100% - 20px);
}

.preview-container div {
  white-space: pre-wrap;
}

.video-container video {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.resource-container {
  margin-top: 20px;
}

.design-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.download-image-button {
  margin-left: 10px;
}
</style>
