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
  multipleChoiceCount: '0', // 选择题题数，默认值为0
  multipleChoiceScore: '0', // 选择题分值，默认值为0
  fillInTheBlankCount: '0', // 填空题题数，默认值为0
  fillInTheBlankScore: '0', // 填空题分值，默认值为0
  trueFalseCount: '0', // 判断题题数，默认值为0
  trueFalseScore: '0', // 判断题分值，默认值为0
  problemSolvingCount: '0', // 解答题题数，默认值为0
  problemSolvingScore: '0', // 解答题分值，默认值为0
  practiceCount: '0', // 练习题题数，默认值为0
  practiceScore: '0', // 练习题分值，默认值为0
  totalScore: '0' // 总分，默认值为0
})

const resourceTypes = [
  { label: '教案', value: '教案' },
  { label: '多媒体材料', value: '多媒体材料' },
  { label: '练习题', value: '练习题' }
]

const mediaTypes = [
  { label: '图片', value: '图片' },
  { label: '视频', value: '视频' },
  { label: 'PPT', value: 'PPT' }
]

// 计算总分
const calculateTotalScore = computed(() => {
  const mcScore =
    parseInt(formInline.multipleChoiceCount) * parseInt(formInline.multipleChoiceScore)
  const fibScore =
    parseInt(formInline.fillInTheBlankCount) * parseInt(formInline.fillInTheBlankScore)
  const tfScore = parseInt(formInline.trueFalseCount) * parseInt(formInline.trueFalseScore)
  const psScore =
    parseInt(formInline.problemSolvingCount) * parseInt(formInline.problemSolvingScore)
  const practiceScore = parseInt(formInline.practiceCount) * parseInt(formInline.practiceScore)

  return mcScore + fibScore + tfScore + psScore + practiceScore
})

// 监听相关字段的变化，自动更新总分
watch(
  [
    formInline.multipleChoiceCount,
    formInline.multipleChoiceScore,
    formInline.fillInTheBlankCount,
    formInline.fillInTheBlankScore,
    formInline.trueFalseCount,
    formInline.trueFalseScore,
    formInline.problemSolvingCount,
    formInline.problemSolvingScore,
    formInline.practiceCount,
    formInline.practiceScore
  ],
  () => {
    formInline.totalScore = calculateTotalScore.value.toString()
  }
)
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
              <el-row :gutter="20" v-if="item.value === '练习题'">
                <el-col :span="12">
                  <el-form-item label="选择题题数">
                    <el-input
                      v-model="formInline.multipleChoiceCount"
                      placeholder="选择题题数"
                      clearable
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="选择题分值">
                    <el-input
                      v-model="formInline.multipleChoiceScore"
                      placeholder="选择题分值"
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20" v-if="item.value === '练习题'">
                <el-col :span="12">
                  <el-form-item label="填空题题数">
                    <el-input
                      v-model="formInline.fillInTheBlankCount"
                      placeholder="填空题题数"
                      clearable
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="填空题分值">
                    <el-input
                      v-model="formInline.fillInTheBlankScore"
                      placeholder="填空题分值"
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20" v-if="item.value === '练习题'">
                <el-col :span="12">
                  <el-form-item label="判断题题数">
                    <el-input v-model="formInline.trueFalseCount" placeholder="判断题题数" clearable />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="判断题分值">
                    <el-input v-model="formInline.trueFalseScore" placeholder="判断题分值" clearable />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20" v-if="item.value === '练习题'">
                <el-col :span="12">
                  <el-form-item label="解答题题数">
                    <el-input
                      v-model="formInline.problemSolvingCount"
                      placeholder="解答题题数"
                      clearable
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="解答题分值">
                    <el-input
                      v-model="formInline.problemSolvingScore"
                      placeholder="解答题分值"
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item v-if="item.value === '练习题'" label="总分">
                <el-input v-model="formInline.totalScore" placeholder="总分" clearable disabled />
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