<template>
  <el-card class="user-card">
    <div class="user-info">
      <el-avatar :size="100" :src="userInfo.avatar" />
      <div class="user-details">
        <div class="user-name">{{ userInfo.name }}</div>
        <div class="user-phone">{{ userInfo.phone }}</div>
      </div>
    </div>
    <div class="password-section">
      <el-form ref="passwordForm" :model="passwordForm" :rules="rules" label-width="100px">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input
            v-model="passwordForm.currentPassword"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请确认新密码"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitPasswordChange">修改密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>
</template>

<script>
// import axios from 'axios';
// import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      userInfo: {
        avatar: 'https://via.placeholder.com/100', // 示例头像
        name: 'Mrs. Black',
        phone: '19983259304',
      },
      passwordForm: {
        currentPassword: 'potato', // 默认密码
        newPassword: '',
        confirmPassword: '',
      },
      rules: {
        currentPassword: [
          { required: true, message: '请输入当前密码', trigger: 'blur' },
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
        ],
        confirmPassword: [
          { required: true, message: '请确认新密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.passwordForm.newPassword) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
      },
    };
  },
  // mounted() {
  //   this.fetchUserInfo();
  // },
  methods: {
    // async fetchUserInfo() {
    //   try {
    //     const response = await axios.get('/api/user/info');
    //     this.userInfo = response.data;
    //   } catch (error) {
    //     console.error('获取用户信息失败', error);
    //     ElMessage.error('获取用户信息失败');
    //   }
    // },
    submitPasswordChange() {
      this.$refs.passwordForm.validate((valid) => {
        if (valid) {
          console.log('密码修改成功');
          // 清空表单
          this.passwordForm = {
            currentPassword: 'potato', // 保留默认密码
            newPassword: '',
            confirmPassword: '',
          };
        }
      });
    },
  },
};
</script>

<style scoped>
.user-card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-right: 20px; /* 添加右边距 */
}
.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.user-avatar {
  margin-right: 20px; /* 增加头像与信息的间距 */
}
.user-details {
  display: flex;
  flex-direction: column;
}
.user-details .user-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px; /* 增加姓名与电话的间距 */
}
.user-details .user-phone {
  font-size: 14px;
  color: #666;
}
.password-section {
  margin-top: 20px;
}
</style>
