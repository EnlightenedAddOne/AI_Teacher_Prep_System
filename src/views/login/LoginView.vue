<script setup lang="ts">
import { reactive, ref } from "vue";
import type { FormRules, FormInstance } from "element-plus";
import { login } from "@/api/user";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

const router = useRouter();

// 表单的响应式数据
const form = reactive({
  username: "", // 用户名
  password: "" // 密码
});

// 登录事件处理
const onSubmit = async () => {
  // 表单校验（失败执行 catch）
  await formRef.value?.validate().catch((err) => {
    ElMessage.error("用户名或密码错误");
    throw err;
  });

  try {
    // 调用登录接口
    const response = await login(form.username, form.password);
    // 假设登录接口返回一个 token
    const token = response.token;

    // 将 token 存储到 localStorage 中
    localStorage.setItem("token", token);

    // 登录成功，跳转到主页
    router.push("/");
  } catch (error) {
    // 显式忽略 error 变量
    void error;
    // 登录失败，提示错误信息
    ElMessage.error("登录失败请检查用户名和密码");
    console.log("登录失败");
  }
};

// 定义表单校验规则
const rules = reactive<FormRules>({
  username: [
    { required: true, message: "请输入用户名" },
  ],
  password: [
    { required: true, message: "请输入密码" }
  ]
});

const formRef = ref<FormInstance>();

// 随机生成星星位置
const randomPosition = () => {
  const top = Math.random() * 100; // 0-100%
  const left = Math.random() * 100; // 0-100%
  return {
    top: `${top}%`,
    left: `${left}%`
  };
};

// 确保 randomPosition 函数在模板中可用
defineExpose({ randomPosition });
</script>

<template>
  <div class="login-container">
    <div class="background">
      <div class="star" v-for="n in 100" :key="n" :style="randomPosition()"></div>
    </div>
    <div class="content">
      <div class="introduction">
        <h1 class="system-title">AI辅助教师备课系统</h1>
        <p class="description">
          欢迎使用AI辅助教师备课系统！<br>
          本系统利用先进的人工智能技术，为教师提供智能化的备课支持。<br>
          您可以通过AI生成教学大纲、教案、课件，<br>
          并获取丰富的教学资源和案例，<br>
          让备课更高效、更轻松！
        </p>
      </div>
      <div class="login">
        <h2 class="login-title">登录</h2> <!-- 登录标题 -->
        <el-form
          :model="form"
          label-width="auto"
          :rules="rules"
          style="max-width: 400px"
          size="large"
          ref="formRef"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              class="glass-input"
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              class="glass-input"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="onSubmit" class="black-button">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>

.login-container {
  position: relative;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #a2d2ff, #c9f1df, #e6f7ff, #f5f5f5); /* 蓝绿灰白渐变 */
  z-index: -1;
  animation: gradient 15s infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  animation: twinkle 2s infinite alternate;
}

@keyframes twinkle {
  from {
    opacity: 0.7;
    transform: scale(1);
  }
  to {
    opacity: 1;
    transform: scale(1.2);
  }
}

.content {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 53%; /* 宽度调整 */
  padding: 40px; /* 增加内边距 */
}

.introduction {
  flex: 1;
  text-align: left;
  margin-right: 100px;
}

.system-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000; /* 系统标题文字为黑色 */
  margin-bottom: 20px;
}

.description {
  font-size: 1rem;
  color: #333; /* 描述文字颜色 */
  line-height: 1.6;
}

.login {
  flex: 1;
  margin-left: 40px;
  padding: 30px; /* 增加内边距 */
  background-color: rgba(255, 255, 255, 0); /* 完全透明 */
  border: 1px solid rgba(73, 73, 73, 0.2); /* 深色边框 */
  border-radius: 15px; /* 圆角调整 */
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  width: 300px; /* 设置一个固定宽度 */
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  color: #000; /* 登录标题文字为黑色 */
  margin-bottom: 20px;
}

.login .el-form {
  margin-top: 20px;
}

.login .el-form .el-form-item {
  margin-top: 20px;
}

.glass-input {
  background-color: transparent; /* 输入框背景透明 */
  border: 1px solid rgba(255, 255, 255, 0.5); /* 输入框边框透明 */
  border-radius: 10px; /* 输入框圆角 */
  padding: 10px; /* 输入框内边距 */
  color: #000; /* 输入框文字颜色改为黑色 */
  font-weight: bold; /* 输入框文字加粗 */
  caret-color: #000; /* 输入光标颜色改为黑色 */
}

.black-button {
  width: 100%;
  margin-top: 10px;
  background-color: #000; /* 按钮背景为黑色 */
  border: 1px solid #000; /* 按钮边框为黑色 */
  border-radius: 10px; /* 按钮圆角 */
  color: #fff; /* 按钮文字颜色为白色 */
  font-weight: bold; /* 按钮文字加粗 */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* 按钮阴影 */
  transition: all 0.3s ease; /* 添加过渡效果 */
  &:hover {
    background-color: #333; /* 鼠标悬停时的背景颜色 */
    border-color: #333; /* 鼠标悬停时的边框颜色 */
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.5); /* 鼠标悬停时的阴影效果 */
  }
}

/* 修改表单标签和占位符的颜色 */
.el-form-item__label {
  color: #000; /* 标签文字颜色改为黑色 */
}

::v-deep(.el-input__inner) {
  background-color: transparent !important; /* 输入框背景完全透明 */
  color: #000 !important; /* 输入框文字颜色为黑色 */
  caret-color: #000; /* 输入光标颜色为黑色 */
}

::v-deep(.el-input__placeholder) {
  color: transparent;
}
</style>
