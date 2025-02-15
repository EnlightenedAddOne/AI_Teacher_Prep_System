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
  choice: {
    enabled: boolean; // 是否启用选择题
    count: number; // 选择题数量
    score: number; // 选择题分数
  };
  fill: {
    enabled: boolean; // 是否启用填空题
    count: number; // 填空题数量
    score: number; // 填空题分数
  };
  judge: {
    enabled: boolean; // 是否启用判断题
    count: number; // 判断题数量
    score: number; // 判断题分数
  };
  short_answer: {
    enabled: boolean; // 是否启用简答题
    count: number; // 简答题数量
    score: number; // 简答题分数
  };
  application: {
    enabled: boolean; // 是否启用应用题
    count: number; // 应用题数量
    score: number; // 应用题分数
  };
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
