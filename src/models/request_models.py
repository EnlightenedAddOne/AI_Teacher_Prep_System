from pydantic import BaseModel


class TeachingDesignRequest(BaseModel):
    subject: str
    topic: str
    goals: str
    duration: str
    grade: str


class ExerciseRequest(BaseModel):
    subject: str
    topic: str
    degree: str
    exercise_config: dict


class OnlineTestRequest(BaseModel):
    """在线测试请求体"""
    subject: str  # 学科名称
    topic: str  # 课程主题
    degree: str  # 难度(简单/中等/困难)
    time_limit: int  # 考试时长(分钟)
    questions: dict  # 题型配置
