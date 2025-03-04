from typing import List, Optional, Dict, Union
from enum import Enum
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
    title: str  # 书名
    authors: List[str]  # 作者
    publisher: str  # 出版社
    publication_year: int  # 出版年份
    isbn: Optional[str]  # 国际标准书号


class RecommendedPaper(BaseModel):
    title: str  # 论文标题
    authors: List[str]  # 作者
    journal: str  # 期刊名称
    publication_year: int  # 发表年份
    doi: Optional[str]  # 数字对象标识符（Digital Object Identifier）


class RecommendedVideo(BaseModel):
    title: str  # 视频标题
    platform: str  # 平台名称
    url: str  # 视频链接
    duration: Optional[str]  # 视频时长
    view_count: Optional[str]  # 播放量字段


class TeachingDesignResponse(BaseModel):
    """教学设计响应"""
    content: str  # markdown格式的教学设计内容
    teach_pdf_url: str  # 教学设计PDF下载链接
    images: Optional[List[TeachingImage]] = None
    ppt_video_path: Optional[str] = None  # ppt转视频的输出路径
    books: Optional[List[RecommendedBook]] = None
    papers: Optional[List[RecommendedPaper]] = None
    videos: Optional[List[RecommendedVideo]] = None
    design_id: str  # 唯一ID


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


class GradingStatus(str, Enum):
    """批改状态枚举"""
    PENDING = "pending"  # 待批改
    GRADED = "graded"  # 已批改
    PENDING_MANUAL = "pending_manual"  # 待人工批改


class QuestionDetail(BaseModel):
    """单个题目的批改详情"""
    exam_question_id: int  # 试卷题目ID
    question_type: str  # 题目类型(single_choice/judgment/fill_blank/short_answer/application)
    content: str  # 题目内容
    assigned_score: float  # 题目分值
    student_answer: str  # 学生答案
    correct_answer: str  # 正确答案
    explanation: Optional[str] = None  # 答案解析
    final_score: float  # 最终得分
    status: GradingStatus  # 批改状态


class ScoreSummary(BaseModel):
    """得分统计信息"""
    objective_score: float  # 客观题得分(选择题和判断题)
    objective_total: float  # 客观题总分
    subjective_score: float  # 主观题得分(填空题、简答题和应用计算题)
    subjective_total: float  # 主观题总分
    total_score: float  # 总分
    total_possible: float  # 试卷总分


class StudentAnswerResponse(BaseModel):
    """学生作答批改响应"""
    record_id: int  # 作答记录ID
    student_id: str  # 学生ID
    exam_id: int  # 试卷ID
    status: GradingStatus  # 批改状态
    score_summary: ScoreSummary  # 得分统计
    question_details: List[QuestionDetail]  # 题目批改详情列表
