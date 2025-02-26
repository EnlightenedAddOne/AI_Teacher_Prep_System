from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationInfo
from typing import Dict, Any, Optional


class ResourceRecommendationRequest(BaseModel):
    """资源推荐请求模型"""
    require_books: bool = Field(default=True, description="是否需要推荐书籍")
    book_count: int = Field(default=3, ge=0, le=20, description="推荐书籍数量")
    require_papers: bool = Field(default=True, description="是否需要推荐论文")
    paper_count: int = Field(default=3, ge=0, le=20, description="推荐论文数量")
    require_videos: bool = Field(default=True, description="是否需要推荐视频")
    video_count: int = Field(default=3, ge=0, le=20, description="推荐视频数量")

    @field_validator('*', mode='before')
    def validate_counts(cls, v, info: ValidationInfo):
        if info.field_name and info.field_name.endswith('_count') and v < 0:
            raise ValueError(f"{info.field_name}不能小于0")
        return v


class TeachingDesignRequest(BaseModel):
    """教学设计请求模型"""
    subject: str
    topic: str
    goals: str
    duration: str
    grade: str
    with_images: bool = Field(default=False, description="是否需要生成图片")
    image_count: int = Field(default=5, ge=0, le=20, description="图片数量")
    ppt_turn_video: bool = Field(default=False, description="是否需要将生成的PPT转换为视频")
    voice_type: str = Field(
        default="年轻男声",
        description="选择中文声线类型（可选：年轻男声、温暖女声、播音男声、甜美女声、活泼女声）"
    )
    resource_recommendation: Optional[ResourceRecommendationRequest] = None

    @field_validator('image_count')
    def validate_image_count(cls, v, info: ValidationInfo):
        if v < 0:
            raise ValueError("图片数量不能小于0")
        return v

    @field_validator('voice_type')
    def validate_voice_type(cls, v):
        valid_voices = {"年轻男声", "温暖女声", "播音男声", "甜美女声", "活泼女声"}
        if v not in valid_voices:
            raise ValueError(f"不支持的声线类型。支持的声线类型: {', '.join(valid_voices)}")
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
