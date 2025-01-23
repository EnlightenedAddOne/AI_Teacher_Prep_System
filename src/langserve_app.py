from fastapi import FastAPI
from pydantic import BaseModel
from langserve import add_routes
from langchain_core.runnables import Runnable
from teaching_design import generate_teaching_design
from exercise_generation import generate_exercises
from config import config
from utils.helpers import setup_cors  # 导入工具函数

app = FastAPI()

# 使用工具函数设置 CORS 中间件
setup_cors(app)


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


# 添加路由
@app.post("/generate-teaching-design")
async def generate_teaching_design_endpoint(request: TeachingDesignRequest):
    api_key = config['api_keys']['tongyi_api_key']
    result = generate_teaching_design(
        request.subject, request.topic, request.goals,
        request.duration, request.grade, api_key
    )
    return {"teaching_design": result}


@app.post("/generate-exercises")
async def generate_exercises_endpoint(request: ExerciseRequest):
    api_key = config['api_keys']['tongyi_api_key']
    exercises, answers_and_explanations = generate_exercises(
        request.subject, request.topic, request.degree,
        request.exercise_config, api_key
    )
    return {
        "exercises": exercises,
        "answers_and_explanations": answers_and_explanations
    }
