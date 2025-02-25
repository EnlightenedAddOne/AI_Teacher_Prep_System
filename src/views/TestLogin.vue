<template>
  <div>
    <!-- 切换按钮 -->
    <div>
      <button @click="currentForm = 'login'" :class="{ active: currentForm === 'login' }">登录</button>
      <button @click="currentForm = 'create'" :class="{ active: currentForm === 'create' }">创建用户</button>
    </div>

    <!-- 登录表单 -->
    <div v-if="currentForm === 'login'">
      <h2>登录</h2>
      <input v-model="loginForm.username" placeholder="用户名" />
      <input v-model="loginForm.password" type="password" placeholder="密码" />
      <button @click="handleLogin">登录</button>
      <p v-if="loginError" style="color: red">{{ loginError }}</p>
    </div>

    <!-- 创建用户表单 -->
    <div v-if="currentForm === 'create'">
      <h2>创建用户</h2>
      <input v-model="createForm.username" placeholder="用户名" />
      <input v-model="createForm.password" type="password" placeholder="密码" />
      <input v-model="createForm.role" placeholder="角色" />
      <button @click="handleCreateUser">创建用户</button>
      <p v-if="createError" style="color: red">{{ createError }}</p>
      <p v-if="createSuccess" style="color: green">{{ createSuccess }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { login, createUser } from "@/api/user";

export default defineComponent({
  name: "UserManagement",
  setup() {
    // 当前显示的表单
    const currentForm = ref("login"); // 默认显示登录表单

    // 登录表单数据
    const loginForm = reactive({
      username: "",
      password: "",
    });
    const loginError = ref<string | null>(null);
    const token = ref<string | null>(null);

    // 创建用户表单数据
    const createForm = reactive({
      username: "",
      password: "",
      role: "",
    });
    const createError = ref<string | null>(null);
    const createSuccess = ref<string | null>(null);

    // 处理登录
    const handleLogin = async () => {
      loginError.value = null;
      const tokenValue = await login(loginForm.username, loginForm.password);
      if (tokenValue) {
        token.value = tokenValue;
        createSuccess.value = "登录成功！"; // 提示登录成功
      } else {
        loginError.value = "登录失败，请检查用户名和密码";
      }
    };

    // 处理创建用户
    const handleCreateUser = async () => {
      createError.value = null;
      createSuccess.value = null;

      // 检查是否已登录
      if (!token.value) {
        createError.value = "请先登录后再创建用户！";
        return;
      }

      // 调用创建用户接口
      const success = await createUser(token.value, createForm.username, createForm.password, createForm.role);
      if (success) {
        createSuccess.value = "用户创建成功";
      } else {
        createError.value = "用户创建失败";
      }
    };

    return {
      currentForm,
      loginForm,
      loginError,
      token,
      createForm,
      createError,
      createSuccess,
      handleLogin,
      handleCreateUser,
    };
  },
});
</script>

<style scoped>
/* 添加一些简单的样式 */
input {
  margin: 5px;
  padding: 5px;
}
button {
  margin: 5px;
  padding: 5px;
}

/* 激活状态的按钮样式 */
button.active {
  font-weight: bold;
  background-color: #007bff;
  color: white;
}
</style>
