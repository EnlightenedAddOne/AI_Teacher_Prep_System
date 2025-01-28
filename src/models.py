from pydantic import BaseModel


# 定义请求体模型
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
