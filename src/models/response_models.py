from typing import List, Optional, Dict, Union

from pydantic import BaseModel, Field


class TeachingImage(BaseModel):
    """教学图片信息"""
    title: str
    url: str  # 原始图片URL
    type: str
    md5: str
    source: str = "Bing Images"
    download_url: str  # 图片下载链接


class RecommendedBook(BaseModel):
    title: str
    authors: List[str]
    publisher: str
    publication_year: int
    isbn: Optional[str]


class RecommendedPaper(BaseModel):
    title: str
    authors: List[str]
    journal: str
    publication_year: int
    doi: Optional[str]


class RecommendedVideo(BaseModel):
    title: str
    platform: str
    url: str
    duration: Optional[str]


class TeachingDesignResponse(BaseModel):
    """教学设计响应"""
    content: str  # markdown格式的教学设计内容
    teach_pdf_url: str  # 教学设计PDF下载链接
    images: Optional[List[TeachingImage]] = None
    ppt_video_path: Optional[str] = None  # ppt转视频的输出路径
    books: Optional[List[RecommendedBook]] = None
    videos: Optional[List[RecommendedVideo]] = None
    papers: Optional[List[RecommendedPaper]] = None
    design_id: str
    

class ExerciseResponse(BaseModel):
    """练习题响应"""
    exercises: str  # markdown格式的练习题内容
    answers_and_explanations: str  # markdown格式的答案和解析
    exercises_pdf_url: str  # 练习题PDF下载链接
    answers_pdf_url: str  # 答案解析PDF下载链接


class QuestionOption(BaseModel):
    """题目选项"""
    key: str  # 选项标识(A/B/C/D/√/×)
    value: str  # 选项内容


class Question(BaseModel):
    """题目信息"""
    number: str  # 题型序号(一/二/三/四/五)
    type: str  # 题目类型(选择题/填空题/判断题/简答题/应用计算题)
    score: int  # 题目分值
    id: int  # 题目ID
    content: str  # 题目内容
    options: Optional[List[QuestionOption]] = None  # 选项列表(选择题和判断题必填)
    correct_answer: str  # 正确答案
    explanation: str  # 答案解析
    knowledge_points: List[str]  # 知识点标签
    subject: str  # 学科
    topic: str  # 主题
    degree: str  # 难度


class TestInfo(BaseModel):
    """试卷信息"""
    total_score: int  # 总分
    time_limit: int  # 考试时长(分钟)


class OnlineTestResponse(BaseModel):
    """在线测试响应"""
    exam_id: int  # 试卷ID
    questions: List[Question]  # 题目列表
    test_info: TestInfo  # 试卷信息
