<script setup lang="ts">
import { reactive,ref } from "vue";
import type { FormRules } from "element-plus";
import {login} from "@/api/users"
import {useRouter} from "vue-router"
const router = useRouter()
//表单的响应式数据
const form = reactive({
  //默认可以登录的账号
  phone: '19983259304',
  password: 'potato'
})
//登录事件处理
const onSubmit = async() => {
  //表单校验（失败执行catch）
  await formRef.value?.validate().catch((err)=>{
    ElMessage.error("手机号或密码错误")
    throw err
  })
  //（表单校验成功）正式发送登录请求
  //const data=login(form).then((res)=>{
    //...(根据接口文档判断是否登录成功比如通过定义的success参数)
    /*如果登录失败
    if(){
    ElMessage.error(手机号或密码有误)
    throw new Error(登录信息有误)
    }
    return res.data
    */
  //})
  router.push("/");
}
//定义表单校验规则
const rules = reactive<FormRules>({
  phone: [{required:true,message:"请输入电话号码"},
          {pattern:/^\d{11}$/,message:"请正确输入11位电话号码"}],
  password: [{required:true,message:"请输入密码"},
          {min:6,max:18,message:"密码长度需要6-18位"}]
})


const formRef = ref<FormInstance>()
</script>

<template>
  <div class="login">
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
        <el-input v-model="form.password" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style lang="scss" scoped>
.login {
  background-color: #70c3c3;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login .el-form {
  padding: 30px;
  height: 280px;
  width: 260px;
  background-color: #fff;
}
.login .el-form .el-form-item {
  margin-top: 20px;
}
.login .el-form .el-form-item .el-button {
  width: 100%;
  margin-top: 10px;
}
</style>