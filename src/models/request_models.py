from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationInfo
from typing import Dict, Any, Optional


class ResourceRecommendationRequest(BaseModel):
    """资源推荐请求模型"""
    require_books: bool = Field(default=True, description="是否需要推荐书籍")
    book_count: int = Field(default=3, description="推荐书籍数量", ge=1, le=5)
    require_papers: bool = Field(default=True, description="是否需要推荐论文")
    paper_count: int = Field(default=3, description="推荐论文数量", ge=1, le=5)
    require_videos: bool = Field(default=True, description="是否需要推荐视频")
    video_count: int = Field(default=3, description="推荐视频数量", ge=1, le=5)

    @field_validator('*', mode='before')
    def validate_counts(cls, v, info: ValidationInfo):
        if info.field_name and info.field_name.endswith('_count') and v < 1:
            raise ValueError(f"{info.field_name}不能小于1")
        return v


class TeachingDesignRequest(BaseModel):
    """教学设计请求模型"""
    subject: str
    topic: str
    goals: str
    duration: str
    grade: str
    with_images: bool = Field(default=False)
    image_count: int = Field(default=5, ge=1, le=20, description="图片数量范围1-20")
    ppt_turn_video: bool = Field(default=False)
    resource_recommendation: Optional[ResourceRecommendationRequest] = None

    @field_validator('image_count')
    def validate_image_count(cls, v, info: ValidationInfo):
        values = info.data
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

    @field_validator('questions')
    def validate_questions(cls, v):
        valid_types = {
            'choice', 'fill', 'judge', 
            'short_answer', 'application'
        }
        for q_type in v.keys():
            if q_type not in valid_types:
                raise ValueError(f"无效题型: {q_type}")
            if not isinstance(v[q_type], dict):
                raise ValueError(f"题型配置必须为字典: {q_type}")
            if 'count' not in v[q_type] or 'score' not in v[q_type]:
                raise ValueError(f"必须包含count和score字段: {q_type}")
        return v
