<template>
  <div class="home-container">
    <!-- 顶部标题 -->
    <div class="header">
      <h1>AI辅助教师备课系统</h1>
      <p>让备课更高效，教学更智能</p>
    </div>

    <!-- 使用教程 -->
    <div class="video-container">
      <video
        controls
        :src="videoUrl"
        @loadedmetadata="onLoadedMetadata"
        @error="onVideoError"
      ></video>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  setup() {
    // 确保视频路径正确
    const videoUrl = ref('src/video/demo.mp4'); // 替换为你的视频文件路径

    // 视频加载完成时的回调
    const onLoadedMetadata = () => {
      console.log('视频加载完成');
    };

    // 视频加载失败时的回调
    const onVideoError = (event: Event) => {
      console.error('视频加载失败', event);
      alert('视频加载失败，请检查视频路径和文件是否正确！');
    };

    return {
      videoUrl,
      onLoadedMetadata,
      onVideoError,
    };
  },
});
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

.video-container {
  margin-bottom: 40px;
  width: 100%;
  max-width: 800px; /* 视频容器的宽度 */
  position: relative; /* 设置为相对定位 */
  overflow: hidden; /* 隐藏超出容器的部分 */
  transition: transform 0.3s ease; /* 添加过渡动画 */
}

.video-container video {
  width: 100%;
  height: auto;
  border-radius: 5px; /* 视频也应用圆角 */
  display: block; /* 防止视频有默认的内边距 */
  transition: transform 0.3s ease; /* 添加过渡动画 */
}

.video-container:hover {
  transform: scale(1.05); /* 鼠标悬停时放大 */
}
</style>
