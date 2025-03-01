<template>
  <div class="teaching-design-section">
    <!-- 功能区 -->
    <div v-if="!isGenerating && !teachingDesignResponse" class="features-section">
      <div class="feature-container">
        <!-- 功能区标题 -->
        <div class="features-title">
          <h2>智能备课助手</h2>
          <p>一键生成教案和多媒体教学材料</p>
        </div>

        <!-- 两个入口文件组成的容器 -->
        <div class="entry-container">
          <!-- 教案生成功能入口 -->
          <div
            class="feature-box"
            @click="showTeachingDesignDialog = true; currentMode = 'teaching-design'"
          >
            <div class="feature-content-container">
              <div class="icons-container">
                <el-icon><Document /></el-icon>
              </div>
              <div class="feature-content">
                <h1>教案生成</h1>
                <p>根据教学大纲和课程内容，快速生成高质量教案。</p>
              </div>
            </div>
          </div>
          <!-- 教案及多媒体材料生成功能入口 -->
          <div
            class="feature-box"
            @click="showTeachingDesignDialog = true; currentMode = 'multimedia'"
          >
            <div class="feature-content-container">
              <div class="icons-container">
                <el-icon><Document /></el-icon>
                <el-icon><VideoCamera /></el-icon>
              </div>
              <div class="feature-content">
                <h1>教案和多媒体材料生成</h1>
                <p>生成教案和与课程相关的多媒体教学材料，丰富教学内容。</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 教案生成需求弹框 -->
    <el-dialog
      v-model="showTeachingDesignDialog"
      :title="currentMode === 'teaching-design' ? '教案生成需求' : '教案及多媒体材料生成需求'"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      class="teaching-design-dialog"
      width="50%"
    >
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

        <!-- 多媒体相关选项仅在当前模式为 'multimedia' 时显示 -->
        <template v-if="currentMode === 'multimedia'">
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
          <!-- 是否生成 PPT 视频 -->
        <el-form-item label="是否生成 PPT 视频">
          <el-switch
            v-model="teachingDesignRequest.ppt_turn_video"
            @change="handlePptVideoChange"
          />
        </el-form-item>

        <!-- PPT 视频声线选择（仅在选择生成 PPT 视频时显示） -->
        <el-form-item
          label="PPT 视频声线"
          v-if="teachingDesignRequest.ppt_turn_video"
        >
          <el-select v-model="teachingDesignRequest.voice_type">
            <el-option
              v-for="option in voiceOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
          <el-form-item label="是否推荐书籍">
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
        </template>
      </el-form>
      <template #footer>
        <el-button @click="showTeachingDesignDialog = false">取消</el-button>
        <el-button type="primary" @click="handleGenerateTeachingDesign">
          生成教学设计
        </el-button>
      </template>
    </el-dialog>

    <!-- 教案生成结果展示 -->
    <div v-if="teachingDesignResponse || isGenerating" class="result-container">
      <div class="result-card-container">
        <!-- 返回按钮所在的独立卡片 -->
        <el-card class="box-card back-card">
          <el-button class="back-button" type="text" @click="resetState">&lt;&lt; 返回</el-button>
        </el-card>

        <!-- 教案生成结果卡片 -->
        <el-card class="box-card result-card">
          <template #header>
            <div class="card-header">
              <span>教案生成结果</span>
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
             <!-- 教案PDF -->
             <h3>教案PDF</h3> <!-- 文字提示 -->
             <div class="preview-container">
                  <div v-html="formatMarkdown(teachingDesignResponse?.content)"></div> <!-- 浏览框 -->
             </div>
              <!-- 下载按钮 -->
              <el-button class="download-button" type="success" @click="downloadPdf('teaching_design.pdf')">下载 PDF</el-button>

              <!-- 推荐图片 -->
              <div v-if="teachingDesignResponse?.images" class="carousel-container">
                <h3>推荐图片</h3>
                <el-carousel :autoplay="false" indicator-position="none" arrow="always">
                  <el-carousel-item v-for="image in teachingDesignResponse.images" :key="image.md5">
                    <div class="carousel-item">
                      <img :src="image.url" :alt="image.title" class="design-image" />
                      <a :href="image.url" target="_blank" class="image-link">
                        查看图片 {{ image.title }}
                      </a>
                    </div>
                  </el-carousel-item>
                </el-carousel>
              </div>

              <!-- PPT 视频展示 -->
              <div
                v-if="teachingDesignResponse?.ppt_video_path"
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
                v-if="teachingDesignResponse?.books"
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
                v-if="teachingDesignResponse?.papers"
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
                v-if="teachingDesignResponse?.videos"
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
</div>

</template>

<script lang="ts" setup>
import { ref } from "vue";
import { generateTeachingDesign, downloadPdf as apiDownloadPdf } from "@/api/examService";
import type { TeachingDesignRequest, TeachingDesignResponse } from "@/types/exam";
import { Loading, Document, VideoCamera } from "@element-plus/icons-vue";
import { marked } from "marked";
import type { FormInstance } from "element-plus";

const showTeachingDesignDialog = ref(false); // 控制教案生成需求弹框的显示
const currentMode = ref("teaching-design"); // 当前模式：教案生成或教案及多媒体生成
const teachingDesignRequest = ref<TeachingDesignRequest>({
  subject: "",
  topic: "",
  goals: "",
  duration: "",
  grade: "",
  with_images: false,
  image_count: 0,
  ppt_turn_video: false,
  voice_type: "年轻男声", // 默认值
  resource_recommendation: {
    require_books: false,
    book_count: 0,
    require_papers: false,
    paper_count: 0,
    require_videos: false,
    video_count: 0,
  },
});
const teachingDesignResponse = ref<TeachingDesignResponse | null>(null);
const isLoading = ref(false);
const isGenerating = ref(false); // 新增标志变量，用于控制生成按钮点击后的显示逻辑
const rules = {
  subject: [{ required: true, message: "请输入科目", trigger: "blur" }],
  topic: [{ required: true, message: "请输入主题", trigger: "blur" }],
  goals: [{ required: true, message: "请输入教学目标", trigger: "blur" }],
  duration: [{ required: true, message: "请输入时长", trigger: "blur" }],
  grade: [{ required: true, message: "请输入年级", trigger: "blur" }],
};

const voiceOptions = [
  { label: "年轻男声", value: "年轻男声" },
  { label: "温暖女声", value: "温暖女声" },
  { label: "播音男声", value: "播音男声" },
  { label: "甜美女声", value: "甜美女声" },
  { label: "活泼女声", value: "活泼女声" },
];
const teachingDesignForm = ref<FormInstance | null>(null);

const handleWithImagesChange = () => {
  teachingDesignRequest.value.image_count = teachingDesignRequest.value.with_images ? 1 : 0;
};

const handlePptVideoChange = () => {
  if (!teachingDesignRequest.value.ppt_turn_video) {
    // 无需设置默认值，因为已经初始化为false
  }
};



const handleBooksChange = () => {
  teachingDesignRequest.value.resource_recommendation.book_count = teachingDesignRequest.value.resource_recommendation.require_books ? 1 : 0;
};

const handlePapersChange = () => {
  teachingDesignRequest.value.resource_recommendation.paper_count = teachingDesignRequest.value.resource_recommendation.require_papers ? 1 : 0;
};

const handleVideosChange = () => {
  teachingDesignRequest.value.resource_recommendation.video_count = teachingDesignRequest.value.resource_recommendation.require_videos ? 1 : 0;
};

const handleGenerateTeachingDesign = async () => {
  if (teachingDesignForm.value) {
    const isValid = await teachingDesignForm.value.validate();
    if (!isValid) {
      alert("请填写完整信息");
      return;
    }
  }

  showTeachingDesignDialog.value = false; // 关闭弹窗
  isGenerating.value = true; // 设置标志变量，表示正在生成

  try {
    isLoading.value = true;
    teachingDesignResponse.value = await generateTeachingDesign(teachingDesignRequest.value);
  } catch (error) {
    console.error("生成教学设计失败:", error);
    alert("生成教学设计失败，请检查输入是否正确");
    resetState(); // 如果失败，重置状态
  } finally {
    isLoading.value = false;
  }
};

const downloadPdf = async (filename: string) => {
  try {
    const blob = await apiDownloadPdf(filename);
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error("下载 PDF 失败:", error);
  }
};

const formatMarkdown = (content: string | undefined) => {
  if (content) {
    return marked(content);
  }
  return "";
};

const resetState = () => {
  showTeachingDesignDialog.value = false;
  teachingDesignResponse.value = null;
  isGenerating.value = false; // 重置标志变量
};
</script>

<style scoped>
/* 整体页面容器，设置内边距、字体、颜色和居中对齐 */
.teaching-design-section {
  padding: 50px; /* 页面上下左右内边距为20px */
  font-family: "Arial", sans-serif; /* 设置字体为Arial */
  color: #333; /* 设置文字颜色为深灰色 */
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
}

/* 功能区容器，宽度占满屏幕，内容居中 */
.features-section {
  width: 100%; /* 宽度占满屏幕 */
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
}

/* 功能区标题 */
.features-title {
  text-align: center; /* 文本居中对齐 */
  margin-bottom: 20px; /* 与下方入口的间距 */
}

.features-title h2 {
  font-size: 30px; /* 标题字体大小 */
  color: #409eff; /* 标题颜色为蓝色 */
  animation: fadeIn 2s ease forwards; /* 添加淡入动画 */
}

.features-title p {
  font-size: 16px; /* 描述字体大小 */
  color: #666; /* 描述颜色为浅灰色 */
  animation: fadeIn 2s ease forwards; /* 添加淡入动画 */
}

/* 功能区标题动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px); /* 从上方进入 */
  }
  to {
    opacity: 1;
    transform: translateY(0); /* 定位到原位置 */
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  padding: 10px 20px;
}

/* 包裹两个入口文件的容器，宽度占满屏幕 */
.entry-container {
  width: 100%; /* 宽度占满父容器 */
  display: flex; /* 使用flex布局 */
  justify-content: space-between; /* 两个入口左右排列，间距均匀分布 */
  padding: 0 20px; /* 根据需要添加左右内边距，确保内容不紧贴边缘 */
}

/* 单个入口的样式 */
.feature-box {
  width: 520px; /* 宽度设置为500px */
  height: 520px; /* 高度设置为500px */
  background-color: #f9f9f9; /* 背景颜色为浅灰色 */
  border: 1px solid #ddd; /* 边框为淡灰色 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 鼠标悬停时的动画效果 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
  display: flex; /* 使用flex布局 */
  align-items: center; /* 垂直居中对齐 */
  justify-content: center; /* 水平居中对齐 */
}

/* 鼠标悬停时的样式 */
.feature-box:hover {
  transform: scale(1.05); /* 放大1.05倍 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 增加阴影效果 */
}

/* 入口内容的容器 */
.feature-content-container {
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
  justify-content: center; /* 垂直居中对齐 */
  text-align: center; /* 文字居中对齐 */
}

/* 图标容器 */
.icons-container {
  display: flex; /* 使用flex布局 */
  flex-wrap: wrap; /* 允许换行 */
  justify-content: center; /* 水平居中对齐 */
  gap: 10px; /* 图标之间的间距 */
}

/* 入口图标样式 */
.feature-content-container .el-icon {
  font-size: 7em; /* 图标大小 */
  color: #409eff; /* 图标颜色为蓝色 */
}

/* 入口内容区域 */
.feature-content h3 {
  font-size: 2em; /* 标题字体大小 */
  color: #333; /* 标题颜色为深灰色 */
  margin: 0 0 10px 0; /* 标题与描述的间距 */
}

.feature-content p {
  font-size: 1em; /* 描述字体大小 */
  color: #666; /* 描述颜色为浅灰色 */
  margin: 0; /* 清除默认的段落间距 */
}

/* 结果展示容器，宽度占满屏幕，内容居中 */
.result-container {
  width: 85%; /* 宽度占满屏幕 */
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
}

/* 包裹返回按钮和结果卡片的容器，宽度占满屏幕，左右内边距为10px */
.result-card-container {
  width: 100%; /* 宽度占满屏幕 */
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
  padding: 0 10px; /* 距离左右边界10px */
}

/* 卡片样式，宽度占满屏幕减去20px（左右内边距），居中显示 */
.box-card {
  width: calc(100% - 20px); /* 宽度占满屏幕减去20px */
  margin: 20px auto; /* 上下外边距为20px，左右自动居中 */
  background-color: rgba(255, 255, 255, 0.8); /* 背景颜色为半透明白色 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  backdrop-filter: blur(10px); /* 添加背景模糊效果 */
}

/* 返回按钮样式 */
.back-button {
  font-size: 16px; /* 字体大小 */
  color: #1677ff; /* 字体颜色为蓝色 */
  text-decoration: none; /* 去掉下划线 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
}

/* 结果卡片样式，宽度占满屏幕减去20px（左右内边距） */
.result-card {
  width: calc(100% - 20px); /* 宽度占满屏幕减去20px */
}

/* 加载动画容器 */
.loading-container {
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
  justify-content: center; /* 垂直居中对齐 */
  height: 100px; /* 容器高度 */
  padding: 20px; /* 内边距 */
}

/* 加载图标样式 */
.loading-icon {
  animation: spin 1s infinite linear; /* 旋转动画 */
  font-size: 32px; /* 图标大小 */
  margin-bottom: 8px; /* 图标与文字的间距 */
}

/* 定义旋转动画 */
@keyframes spin {
  from { transform: rotate(0deg); } /* 从0度开始 */
  to { transform: rotate(360deg); } /* 旋转360度 */
}

/* 结果内容区域 */
.result-content {
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
  padding: 20px; /* 内边距 */
}

/* 图片轮播容器 */
.carousel-container {
  margin-top: 20px; /* 与上一个元素的间距 */
  width: 100%; /* 宽度占满容器 */
}

/* 单个轮播项 */
.carousel-item {
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
}

/* 图片样式 */
.design-image {
  max-width: 100%; /* 图片宽度不超过容器 */
  height: auto; /* 图片高度自适应 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  margin-bottom: 10px; /* 图片与文字的间距 */
}

/* 图片链接样式 */
.image-link {
  color: #1677ff; /* 字体颜色为蓝色 */
  text-decoration: none; /* 去掉下划线 */
  font-size: 14px; /* 字体大小 */
}

/* 下载按钮样式 */
.download-button {
  margin-top: 10px; /* 与上一个元素的间距 */
}

/* 预览容器 */
.preview-container {
  border: 1px solid #ddd; /* 边框为淡灰色 */
  padding: 0; /* 清除内边距 */
  margin-top: 10px; /* 与上一个元素的间距 */
  max-height: 300px; /* 最大高度 */
  overflow-y: auto; /* 超出部分显示滚动条 */
  width: calc(100% - 20px); /* 宽度占满容器减去20px */
}

/* 预览内容样式 */
.preview-container div {
  white-space: pre-wrap; /* 保留换行符和空格 */
}

/* 视频容器 */
.video-container video {
  max-width: 100%; /* 视频宽度不超过容器 */
  height: auto; /* 视频高度自适应 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  margin-top: 10px; /* 与上一个元素的间距 */
}

/* 资源容器 */
.resource-container {
  margin-top: 20px; /* 与上一个元素的间距 */
}

.preview-container {
  border: 1px solid #ddd; /* 边框为淡灰色 */
  padding: 10px; /* 内边距 */
  margin-top: 10px; /* 与标题的间距 */
  max-height: 300px; /* 最大高度 */
  overflow-y: auto; /* 超出部分显示滚动条 */
  width: calc(100% - 20px); /* 宽度占满容器减去20px */
  background-color: #fff; /* 背景颜色 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

h3 {
  margin: 20px 0 10px; /* 标题的上下间距 */
  text-align: left; /* 标题居中对齐 */
  font-size: 20px;
}

h1{
  font-size: 37px;
}
</style>
