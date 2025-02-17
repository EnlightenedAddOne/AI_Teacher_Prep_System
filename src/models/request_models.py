from pydantic import BaseModel, Field, validator
from typing import Dict, Any


class TeachingDesignRequest(BaseModel):
    """教学设计请求模型"""
    subject: str
    topic: str
    goals: str
    duration: str
    grade: str
    with_images: bool = Field(default=False)
    image_count: int = Field(default=5, ge=1, le=20, description="图片数量范围1-20")

    @validator('image_count')
    def validate_image_count(cls, v, values):
        if values.get('with_images') and v < 1:
            raise ValueError("当需要图片时，图片数量至少为1")
        if not values.get('with_images') and v > 0:
            raise ValueError("未选择需要图片时，图片数量应设为0")
        return v


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
    questions: Dict[str, Any]  # 题型配置

    @validator('questions')
    def validate_questions(cls, v):
        # 验证题型配置
        valid_types = {
            'choice',  # 选择题
            'fill',  # 填空题
            'judge',  # 判断题
            'short_answer',  # 简答题
            'application'  # 应用计算题
        }
        for q_type in v.keys():
            if q_type not in valid_types:
                raise ValueError(f"Invalid question type: {q_type}")
            if not isinstance(v[q_type], dict):
                raise ValueError(f"Question config must be a dict: {q_type}")
            if 'count' not in v[q_type] or 'score' not in v[q_type]:
                raise ValueError(f"Question config must contain 'count' and 'score': {q_type}")
        return v
