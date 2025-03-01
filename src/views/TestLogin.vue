<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { login, createUser, updateUser, deleteUser } from "@/api/user";

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

    // 修改用户表单数据
    const updateForm = reactive({
      username: "",
      password: "",
      role: "",
    });
    const updateError = ref<string | null>(null);
    const updateSuccess = ref<string | null>(null);

    // 删除用户表单数据
    const deleteForm = reactive({
      username: "",
    });
    const deleteError = ref<string | null>(null);
    const deleteSuccess = ref<string | null>(null);

    // 处理登录
    const handleLogin = async () => {
      loginError.value = null;
      console.log("尝试登录，用户名:", loginForm.username, "密码:", loginForm.password);
      const tokenValue = await login(loginForm.username, loginForm.password);
      console.log("登录返回的 token:", tokenValue);
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

      console.log("检查 token 状态:", token.value);
      // 检查是否已登录
      if (!token.value) {
        console.log("未登录，无法创建用户");
        createError.value = "请先登录后再创建用户！";
        return;
      }

      console.log("调用创建用户接口，数据:", createForm);
      // 调用创建用户接口
      const success = await createUser(token.value, createForm.username, createForm.password, createForm.role);
      console.log("创建用户接口返回结果:", success);
      if (success) {
        createSuccess.value = "用户创建成功";
      } else {
        createError.value = "用户创建失败";
      }
    };

    // 处理修改用户
    const handleUpdateUser = async () => {
      updateError.value = null;
      updateSuccess.value = null;

      console.log("检查 token 状态:", token.value);
      // 检查是否已登录
      if (!token.value) {
        console.log("未登录，无法修改用户");
        updateError.value = "请先登录后再修改用户！";
        return;
      }

      console.log("调用修改用户接口，数据:", updateForm);
      // 调用修改用户接口
      const success = await updateUser(token.value, updateForm.username, updateForm.password, updateForm.role);
      console.log("修改用户接口返回结果:", success);
      if (success) {
        updateSuccess.value = "用户信息更新成功";
      } else {
        updateError.value = "用户信息更新失败";
      }
    };

    // 处理删除用户
    const handleDeleteUser = async () => {
      deleteError.value = null;
      deleteSuccess.value = null;

      console.log("检查 token 状态:", token.value);
      // 检查是否已登录
      if (!token.value) {
        console.log("未登录，无法删除用户");
        deleteError.value = "请先登录后再删除用户！";
        return;
      }

      console.log("调用删除用户接口，用户名:", deleteForm.username);
      // 调用删除用户接口
      const success = await deleteUser(token.value, deleteForm.username);
      console.log("删除用户接口返回结果:", success);
      if (success) {
        deleteSuccess.value = "用户删除成功";
      } else {
        deleteError.value = "用户删除失败";
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
      updateForm,
      updateError,
      updateSuccess,
      deleteForm,
      deleteError,
      deleteSuccess,
      handleLogin,
      handleCreateUser,
      handleUpdateUser,
      handleDeleteUser,
    };
  },
});
</script>
