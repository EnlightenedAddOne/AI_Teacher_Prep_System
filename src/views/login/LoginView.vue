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
    // 假设登录接口返回一个 token 和用户角色(等待后端接口调整)
    //const { token, role } = response;
    const token = response; // 逻辑测试语句
    const role = "TEACHER"; // 逻辑测试语句

    // 检查角色是否正确存储
    console.log("登录成功，角色为：", role);
    // 将 token 和角色存储到 localStorage 中
    localStorage.setItem("token", token);
    localStorage.setItem("role", role);

     // 检查角色是否正确存储到 localStorage
     const storedRole = localStorage.getItem("role");
     console.log("存储的角色为：", storedRole);

    // 将当前登录的用户名存储到 localStorage 中
    localStorage.setItem("currentUsername", form.username); // 存储用户名

    // 检查角色是否正确存储到 localStorage
    const storedName = localStorage.getItem("currentUsername");
    console.log("存储的名字为：", storedName);

    // 登录成功，跳转到主页
    router.push("/IndexView");
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
// 生成星星的随机位置
const randomPosition = () => {
  const top = Math.random() * 100;
  const left = Math.random() * 100;
  return {
    top: `${top}%`,
    left: `${left}%`,
  };
};
const formRef = ref<FormInstance>();
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
        <h2 class="login-title">登录</h2>
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
  background: linear-gradient(135deg, #a2d2ff, #c9f1df, #e6f7ff, #f5f5f5);
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
  width: 53%;
  padding: 40px;
}

.introduction {
  flex: 1;
  text-align: left;
  margin-right: 100px;
}

.system-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

.description {
  font-size: 1rem;
  color: #333;
  line-height: 1.6;
}

.login {
  flex: 1;
  margin-left: 40px;
  padding: 30px;
  background-color: rgba(255, 255, 255, 0);
  border: 1px solid rgba(73, 73, 73, 0.2);
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  width: 300px;
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

.login .el-form {
  margin-top: 20px;
}

.login .el-form .el-form-item {
  margin-top: 20px;
}

.glass-input {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  padding: 10px;
  color: #000;
  font-weight: bold;
  caret-color: #000;
}

.black-button {
  width: 100%;
  margin-top: 10px;
  background-color: #000;
  border: 1px solid #000;
  border-radius: 10px;
  color: #fff;
  font-weight: bold;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  &:hover {
    background-color: #333;
    border-color: #333;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  }
}

.el-form-item__label {
  color: #000;
}

::v-deep(.el-input__inner) {
  background-color: transparent !important;
  color: #000 !important;
  caret-color: #000;
}

::v-deep(.el-input__placeholder) {
  color: transparent;
}
</style>
