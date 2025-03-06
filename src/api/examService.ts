import axios from 'axios';
import type {
  TeachingDesignRequest,
  TeachingDesignResponse,
  ExerciseRequest,
  ExerciseResponse,
  OnlineTestRequest,
  OnlineTestResponse
} from '@/types/exam';

export const baseURL ='http://192.168.63.215:8000';
const apiClient = axios.create({
  baseURL: baseURL,  // 后端运行地址
  timeout: 100* 60 * 1000, // 设置超时时间为 10 分钟
});

// 教学设计接口
export async function generateTeachingDesign(
  request: TeachingDesignRequest
): Promise<TeachingDesignResponse> {
  const response = await apiClient.post<TeachingDesignResponse>(
    '/generate-teaching-design',
    request
  );
  return response.data;
}

// 练习题生成接口
export async function generateExercises(
  request: ExerciseRequest
): Promise<ExerciseResponse> {
  const response = await apiClient.post<ExerciseResponse>(
    '/generate-exercises',
    request
  );
  return response.data;
}


// 获取试卷详情接口
export async function getExamById(examId: number): Promise<OnlineTestResponse> {
  const response = await apiClient.get<OnlineTestResponse>(`/get-exam/${examId}`);
  return response.data;
}

// 下载 PDF 文件接口
export async function downloadPdf(filename: string): Promise<Blob> {
  const response = await apiClient.get(`/download/${filename}`, {
    responseType: 'blob', // 以 Blob 格式接收文件
  });
  return response.data;
}

// 声线选择功能
export const voiceOptions = [
  { label: '年轻男声', value: '年轻男声' },
  { label: '温暖女声', value: '温暖女声' },
  { label: '播音男声', value: '播音男声' },
  { label: '甜美女声', value: '甜美女声' },
  { label: '活泼女声', value: '活泼女声' }
]

// 在线测试生成接口
export async function generateOnlineTest(
  request: OnlineTestRequest
): Promise<OnlineTestResponse> {
  const response = await apiClient.post<OnlineTestResponse>(
    '/generate-online-test',
    request
  );
  return response.data;
}

export async function gradeStudentAnswers(request: {
  exam_id: number;
  student_id: string;
  answers: {
      exam_question_id: number;
      question_type: string;
      answer_data: {
          selected_option?: string;
          filled_answers?: string[];
          content?: string;
      };
  }[];
}): Promise<{
  record_id: number;
  student_id: string;
  exam_id: number;
  status: string;
  score_summary: {
      objective_score: number;
      objective_total: number;
      subjective_score: number;
      subjective_total: number;
      total_score: number;
      total_possible: number;
  };
  question_details: {
      exam_question_id: number;
      question_type: string;
      content: string;
      assigned_score: number;
      student_answer: string;
      correct_answer: string;
      explanation: string;
      final_score: number;
      status: string;
  }[];
}> {
  const response = await apiClient.post(
      '/grade-student-answers',
      request
  );
  return response.data;
}
