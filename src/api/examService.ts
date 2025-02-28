import axios from 'axios';
import type {
  TeachingDesignRequest,
  TeachingDesignResponse,
  ExerciseRequest,
  ExerciseResponse,
  OnlineTestRequest,
  OnlineTestResponse
} from '@/types/exam';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // 后端运行地址
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
