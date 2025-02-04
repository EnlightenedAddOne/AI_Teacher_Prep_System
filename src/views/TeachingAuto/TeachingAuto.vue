<script lang="ts" setup>
import { reactive, computed, watch } from 'vue'

const formInline = reactive({
  subject: '', // 学科名称
  grade: '', // 学生年级
  topic: '', // 课程主题
  design: '', // 教学设计设置
  time: '', // 课程时长
  type: [], // 第一组复选框的选中值（生成资源类型）
  mediaType: [], // 第二组复选框的选中值（多媒体资源生成选择）
  desc: '', // 附加要求
})

const resourceTypes = [
  { label: '教案', value: '教案' },
  { label: '多媒体材料', value: '多媒体材料' }
]

const mediaTypes = [
  { label: '图片', value: '图片' },
  { label: '视频', value: '视频' },
  { label: 'PPT', value: 'PPT' }
]

</script>

<template>
  <el-card class="box-card">
    <template #header>
      <h1>教学资源生成设置</h1>
    </template>
    <el-form :inline="false" :model="formInline" class="demo-form-inline" label-position="top">
      <!-- 第一行：学科名称和学生年级并列 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="学科名称">
            <el-input v-model="formInline.subject" placeholder="学科名称" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="学生年级">
            <el-input v-model="formInline.grade" placeholder="学生年级" clearable />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 第二行：课程主题 -->
      <el-form-item label="课程主题">
        <el-input v-model="formInline.topic" placeholder="课程主题" clearable />
      </el-form-item>

      <!-- 第三行：生成资源类型 -->
      <el-form-item label="生成资源类型">
        <el-checkbox-group v-model="formInline.type">
          <div v-for="item in resourceTypes" :key="item.value">
            <el-checkbox :value="item.value" :label="item.label" />
            <!-- 动态生成相关表单项 -->
            <div v-if="formInline.type.includes(item.value)">
              <el-form-item v-if="item.value === '教案'" label="课程时长">
                <el-input v-model="formInline.time" placeholder="课程时长" clearable />
              </el-form-item>
              <el-form-item v-if="item.value === '多媒体材料'" label="多媒体资源生成选择">
                <el-checkbox-group v-model="formInline.mediaType">
                  <el-checkbox
                    v-for="media in mediaTypes"
                    :key="media.value"
                    :value="media.value"
                    :label="media.label"
                  ></el-checkbox>
                </el-checkbox-group>
              </el-form-item>

            </div>
          </div>
        </el-checkbox-group>
      </el-form-item>

      <!-- 第十四行：附加要求 -->
      <el-form-item label="附加要求">
        <el-input v-model="formInline.desc" type="textarea" />
      </el-form-item>

      <!-- 第十五行：生成按钮 -->
      <el-form-item class="button-center">
        <el-button
          type="primary"
          :disabled="formInline.type.length === 0"
          @click="generateResources"
          class="custom-button"
        >生成</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<style lang="scss" scoped>
.box-card {
  margin-top: 5px;
  margin-right: 20px;
  width: auto;
}

.demo-form-inline {
  .el-form-item {
    margin-bottom: 16px; // 调整间距
  }
}

.custom-button {
  &.el-button--primary {
    background-color: #1da8e9;
    border-color: #1da8e9;
  }
}
</style>
