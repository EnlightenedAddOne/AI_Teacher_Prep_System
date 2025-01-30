# 程序入口
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from configs import config
from exercise_generation import generate_exercises
from models import (TeachingDesignRequest, ExerciseRequest,
                    TeachingDesignResponse, ExerciseResponse)
from pdf_generator import content_to_pdf
from teaching_design import generate_teaching_design
from utils import setup_cors  # 导入工具函数

app = FastAPI()

# 使用工具函数设置 CORS 中间件
setup_cors(app)


@app.post("/generate-teaching-design", response_model=TeachingDesignResponse)
async def generate_teaching_design_endpoint(request: TeachingDesignRequest):
    api_key = config['api_keys'].get('tongyi_api_key')
    if not api_key:
        raise HTTPException(status_code=500, detail="通义API密钥未配置")
        
    content = generate_teaching_design(
        request.subject, request.topic, request.goals,
        request.duration, request.grade, api_key
    )
    # 使用 content_to_pdf 生成 PDF
    pdf_urls = content_to_pdf([content], ["教学设计"], ["teaching_design.pdf"])
    
    return TeachingDesignResponse(
        content=content,
        teach_pdf_url=pdf_urls[0]
    )


@app.post("/generate-exercises", response_model=ExerciseResponse)
async def generate_exercises_endpoint(request: ExerciseRequest):
    api_key = config['api_keys']['tongyi_api_key']
    exercises, answers_and_explanations = generate_exercises(
        request.subject, request.topic, request.degree,
        request.exercise_config, api_key
    )
    pdf_urls = content_to_pdf(
        [exercises, answers_and_explanations],
        ["练习题", "答案解析"],
        ["exercises.pdf", "answers_and_explanations.pdf"]
    )

    return ExerciseResponse(
        exercises=exercises,
        answers_and_explanations=answers_and_explanations,
        exercises_pdf_url=pdf_urls[0],
        answers_pdf_url=pdf_urls[1]
    )


# 下载 PDF 文件
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(os.path.dirname(__file__), '../output/PDF', filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


