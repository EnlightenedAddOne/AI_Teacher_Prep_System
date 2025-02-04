<script setup lang="ts">
import { reactive, ref } from "vue";
import type { FormRules, FormInstance } from "element-plus";
import { login } from "@/api/users";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

const router = useRouter();

// 表单的响应式数据
const form = reactive({
  phone: '19983259304', // 默认可以登录的账号
  password: 'potato'
});

// 登录事件处理
const onSubmit = async () => {
  // 表单校验（失败执行catch）
  await formRef.value?.validate().catch((err) => {
    ElMessage.error("手机号或密码错误");
    throw err;
  });

  // 直接跳转到主页
  router.push("/");
};

// 定义表单校验规则
const rules = reactive<FormRules>({
  phone: [
    { required: true, message: "请输入电话号码" },
    { pattern: /^\d{11}$/, message: "请正确输入11位电话号码" }
  ],
  password: [
    { required: true, message: "请输入密码" },
    { min: 6, max: 18, message: "密码长度需要6-18位" }
  ]
});

const formRef = ref<FormInstance>();

// 随机生成星星位置
const randomPosition = () => {
  const top = Math.random() * 100; // 0-100%
  const left = Math.random() * 100; // 0-100%
  return {
    top: `${top}%`,
    left: `${left}%`,
  };
};
</script>

<template>
  <div class="login-container">
    <div class="background">
      <div class="star" v-for="n in 100" :key="n" :style="randomPosition()"></div>
    </div>
    <div class="login">
      <h1 class="title">AI辅助教师备课系统</h1>
      <el-form
        :model="form"
        label-width="auto"
        :rules="rules"
        style="max-width: 600px"
        size="large"
        ref="formRef"
      >
        <h2>登录</h2>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
        </el-form-item>
      </el-form>
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

.login {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 300px;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #345;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Pacifico', cursive; /* 使用艺术字体 */
}

.login .el-form {
  margin-top: 20px;
}

.login .el-form .el-form-item {
  margin-top: 20px;
}

.login .el-form .el-form-item .el-button {
  width: 100%;
  margin-top: 10px;
}
</style>
