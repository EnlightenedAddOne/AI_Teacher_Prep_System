// 教学设计请求和响应类型
export interface TeachingDesignRequest {
  subject: string; // 科目
  topic: string; // 主题
  goals: string; // 教学目标
  duration: string; // 时长
  grade: string; // 年级
  with_images?: boolean; // 是否包含图片
  image_count?: number; // 图片数量

}

export interface TeachingDesignResponse {
  content: string; // 教学设计内容
  teach_pdf_url: string; // 教学设计 PDF 链接
  image_path?: string; // 图片路径（可选属性）
}

// 练习题请求和响应类型
export interface ExerciseRequest {
  subject: string; // 科目
  topic: string; // 主题
  degree: string; // 难度
  exercise_config: ExerciseConfig; // 练习题配置
}

// 练习题配置接口
export interface ExerciseConfig {
  type: string; // 练习题类型（如选择题、填空题等）
  count: number; // 题目数量
  [key: string]: unknown; // 允许扩展其他配置项
}

export interface ExerciseResponse {
  exercises: string; // 练习题内容
  answers_and_explanations: string; // 答案解析内容
  exercises_pdf_url: string; // 练习题 PDF 链接
  answers_pdf_url: string; // 答案解析 PDF 链接
}

// 在线测试请求和响应类型
export interface OnlineTestRequest {
  subject: string; // 科目
  topic: string; // 主题
  degree: string; // 难度
  time_limit: number; // 时间限制
  questions: number; // 题目数量
}

export interface OnlineTestResponse {
  exam_id: number; // 试卷 ID
  questions: Array<{
    question: string; // 题目
    options: string[]; // 选项
    answer: string; // 答案
    explanation: string; // 解析
  }>;
  test_info: {
    subject: string; // 科目
    topic: string; // 主题
    time_limit: number; // 时间限制
  };
}
