<template>
  <div class="home-container">
    <!-- 顶部标题 -->
    <div class="header">
      <h1>AI辅助教师备课系统</h1>
      <p>让备课更高效，教学更智能</p>
    </div>

    <!-- 使用教程视频区域 -->
    <div class="tutorial-section">
      <h2>使用教程</h2>
      <div class="video-container">
        <iframe
          width="580"
          height="315"
          src="https://www.bilibili.com/video/BV1JhezeREdZ/?spm_id_from=333.1387.homepage.video_card.click"
          title="妙手回春啊大夫"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>

    <!-- 功能介绍区域 -->
    <div class="features-section">
      <h2>系统功能</h2>
      <div class="feature-list">
        <div class="feature-item">
          <el-icon><Document /></el-icon>
          <div class="feature-content">
            <h3>教案生成</h3>
            <p>根据教学大纲和课程内容，快速生成高质量教案。</p>
          </div>
        </div>
        <div class="feature-item">
          <el-icon><VideoCamera /></el-icon>
          <div class="feature-content">
            <h3>多媒体材料生成</h3>
            <p>生成与课程相关的多媒体教学材料，丰富教学内容。</p>
          </div>
        </div>
        <div class="feature-item">
          <el-icon><Edit /></el-icon>
          <div class="feature-content">
            <h3>练习题生成</h3>
            <p>自动生成练习题，帮助学生巩固知识。</p>
          </div>
        </div>
        <div class="feature-item">
          <el-icon><DataAnalysis /></el-icon>
          <div class="feature-content">
            <h3>智能学情分析</h3>
            <p>通过数据分析，提供学生学习情况的智能分析。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 联系我们区域 -->
    <div class="contact-section">
      <h2>联系我们</h2>
      <div class="contact-info">
        <p>如有任何问题或建议，请通过以下方式联系我们：</p>
        <ul>
          <li><strong>邮箱：</strong>support@teacherai.com</li>
          <li><strong>电话：</strong>10101010101</li>
          <li><strong>微信：</strong>teacher_ai_support</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { Document, VideoCamera, Edit, DataAnalysis } from '@element-plus/icons-vue';

export default {
  components: {
    Document,
    VideoCamera,
    Edit,
    DataAnalysis,
  },
};
</script>

<style scoped>
.home-container {
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.header {
  margin-bottom: 40px;
  text-align: center;
  width: 100%;
}

.header h1 {
  font-size: 2.5em;
  color: #333;
}

.header p {
  font-size: 1.2em;
  color: #666;
}

.tutorial-section,
.features-section,
.contact-section {
  margin-bottom: 40px;
  width: 100%;
  text-align: center;
}

.tutorial-section h2,
.features-section h2,
.contact-section h2 {
  font-size: 1.8em;
  color: #333;
  margin-bottom: 20px;
}

.video-container {
  margin: 0 auto;
  position: relative;
  width: 100%; /* 容器宽度占满父容器 */
  max-width: 600px; /* 最大宽度限制 */
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  overflow: hidden; /* 防止内容溢出 */
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

/* 确保功能模块整体居中 */
.features-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feature-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  max-width: 1200px; /* 设置最大宽度，避免在大屏幕上过于分散 */
  margin: 0 auto; /* 确保功能列表水平居中 */
}

.feature-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  width: calc(50% - 20px); /* 每个功能模块占一半宽度，减去左右间距 */
  margin-left: 10px;
  margin-right: 10px;
}

.feature-item .el-icon {
  font-size: 2em;
  color: #409eff;
  margin-right: 15px;
}

.feature-content {
  text-align: left; /* 功能模块内容左对齐 */
}

.feature-content h3 {
  font-size: 1.2em;
  color: #333;
}

.feature-content p {
  font-size: 1em;
  color: #666;
}

.contact-info {
  max-width: 600px;
  margin: 0 auto;
  text-align: left;
}

.contact-info p {
  font-size: 1em;
  color: #666;
}

.contact-info ul {
  list-style: none;
  padding: 0;
}

.contact-info ul li {
  margin-bottom: 10px;
  font-size: 1em;
  color: #333;
}
</style>
