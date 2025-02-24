// 教学设计请求和响应类型
// @/types/exam.ts
export interface ResourceRecommendation {
  require_books: boolean;
  book_count: number;
  require_papers: boolean;
  paper_count: number;
  require_videos: boolean;
  video_count: number;
}

export interface TeachingDesignRequest {
  subject: string;
  topic: string;
  goals: string;
  duration: string;
  grade: string;
  with_images: boolean;
  image_count: number;
  ppt_turn_video: boolean;
  resource_recommendation: ResourceRecommendation; // 非可选字段
}

export interface TeachingDesignResponse {
  content: string; // 教学设计内容
  teach_pdf_url: string; // 教学设计 PDF 链接
  images?: TeachingImage[]; // 图片列表
  ppt_video_path?: string; // PPT 视频路径
  books?: RecommendedBook[]; // 推荐书籍
  videos?: RecommendedVideo[]; // 推荐视频
  papers?: RecommendedPaper[]; // 推荐论文
  design_id: string; // 教学设计 ID
}

export interface TeachingImage {
  title: string;
  url: string;
  type: string;
  md5: string;
  download_url: string;
}

export interface RecommendedBook {
  title: string;
  authors: string[];
  publisher: string;
  publication_year: number;
  isbn?: string;
}

export interface RecommendedPaper {
  title: string;
  authors: string[];
  journal: string;
  publication_year: number;
  doi?: string;
}

export interface RecommendedVideo {
  title: string;
  platform: string;
  url: string;
  duration?: string;
}

// 练习题请求和响应类型
export interface ExerciseRequest {
  subject: string; // 科目
  topic: string; // 主题
  degree: string; // 难度
  exercise_config: ExerciseConfig; // 练习题配置
}

export interface ExerciseConfig {
  choice?: {
    enabled: boolean; // 是否启用选择题
    count: number; // 选择题数量
    score: number; // 选择题分数
  };
  fill?: {
    enabled: boolean; // 是否启用填空题
    count: number; // 填空题数量
    score: number; // 填空题分数
  };
  application?: {
    enabled: boolean; // 是否启用应用题
    count: number; // 应用题数量
    score: number; // 应用题分数
  };
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
  questions: {
    [key: string]: {
      count: number; // 题目数量
      score: number; // 题目分数
    };
  }; // 题型配置
}

export interface Question {
  number: string; // 题目编号
  type: string; // 题目类型
  score: number; // 分值
  id: number; // 题目 ID
  content: string; // 题目内容
  options?: QuestionOption[]; // 选项列表
  correct_answer: string; // 正确答案
  explanation: string; // 答案解析
  knowledge_points: string[]; // 知识点标签
  subject: string; // 科目
  topic: string; // 主题
  degree: string; // 难度
}

export interface QuestionOption {
  key: string; // 选项标识
  value: string; // 选项内容
}

export interface TestInfo {
  total_score: number; // 总分
  time_limit: number; // 考试时长
}

export interface OnlineTestResponse {
  exam_id: number; // 试卷 ID
  questions: Question[]; // 题目列表
  test_info: TestInfo; // 试卷信息
}
