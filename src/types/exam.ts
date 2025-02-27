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
  voice_type: string;
  resource_recommendation: ResourceRecommendation;
}

export interface TeachingDesignResponse {
  content: string;
  teach_pdf_url: string;
  images?: TeachingImage[];
  ppt_video_path?: string;
  books?: RecommendedBook[];
  papers?: RecommendedPaper[];
  videos?: RecommendedVideo[];
  design_id: string;
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
  view_count?: string;
}

export interface ExerciseRequest {
  subject: string;
  topic: string;
  degree: string;
  exercise_config: ExerciseConfig;
}

export interface ExerciseConfig {
  choice?: {
    enabled: boolean;
    count: number;
    score: number;
  };
  fill?: {
    enabled: boolean;
    count: number;
    score: number;
  };
  application?: {
    enabled: boolean;
    count: number;
    score: number;
  };
  [key: string]: unknown;
}

export interface ExerciseResponse {
  exercises: string;
  answers_and_explanations: string;
  exercises_pdf_url: string;
  answers_pdf_url: string;
}

export interface OnlineTestRequest {
  subject: string;
  topic: string;
  degree: string;
  time_limit: number;
  questions: {
    [key: string]: {
      count: number;
      score: number;
    };
  };
}

export interface Question {
  number: string;
  type: string;
  score: number;
  id: number;
  content: string;
  options?: QuestionOption[];
  correct_answer: string;
  explanation: string;
  knowledge_points: string[];
  subject: string;
  topic: string;
  degree: string;
}

export interface QuestionOption {
  key: string;
  value: string;
}

export interface TestInfo {
  total_score: number;
  time_limit: number;
}

export interface OnlineTestResponse {
  exam_id: number;
  questions: Question[];
  test_info: TestInfo;
}
