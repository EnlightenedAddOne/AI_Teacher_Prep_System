# 程序入口
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from Online_Test import generate_online_test
from configs import config
from education_sql import (
    Session,
    export_exam_to_json
)
from exercise_generation import generate_exercises
from models import (TeachingDesignRequest, ExerciseRequest,
                    TeachingDesignResponse, ExerciseResponse,
                    OnlineTestRequest, OnlineTestResponse)
from multimedia_generation import MultimediaGenerator
from pdf_generator import content_to_pdf
from teaching_design import generate_teaching_design
from utils import setup_cors  # 导入工具函数
from Image_crawling import BingImagesSpider
from models import TeachingImage
import logging

app = FastAPI()

# 使用工具函数设置 CORS 中间件
setup_cors(app)

logger = logging.getLogger(__name__)


# 教学设计
@app.post("/generate-teaching-design", response_model=TeachingDesignResponse)
async def generate_teaching_design_endpoint(request: TeachingDesignRequest):
    tongyi_api_key = config['api_keys'].get('tongyi_api_key')
    images = []

    if not tongyi_api_key:
        raise HTTPException(status_code=500, detail="通义API密钥未配置")

    try:
        content = generate_teaching_design(
            request.subject, request.topic, request.goals,
            request.duration, request.grade, tongyi_api_key
        )

        # 如果需要图片，调用爬虫
        if request.with_images:
            try:
                spider = BingImagesSpider(
                    keyword=request.topic,
                    amount=request.image_count,
                    img_type="diagram",
                    proxy_list=["http://127.0.0.1:8080"]
                )
                image_data = spider.run()
                images = [
                    TeachingImage(
                        title=img['title'],
                        url=img['url'],
                        type=img['type'],
                        md5=img['md5'],
                        download_url=f"/download/image/{Path(img['local_path']).name}" if img.get('local_path') else ""
                    ) for img in image_data if img.get('local_path')
                ]
            except Exception as e:
                logger.error(f"图片爬取失败: {str(e)}")

        # 使用 content_to_pdf 生成 PDF
        pdf_urls = content_to_pdf([content], ["教学设计"], ["teaching_design.pdf"])

        return TeachingDesignResponse(
            content=content,
            teach_pdf_url=pdf_urls[0],
            images=images if request.with_images else None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 练习题
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


# 在线测试
@app.post("/generate-online-test", response_model=OnlineTestResponse)
async def generate_online_test_endpoint(request: OnlineTestRequest):
    api_key = config['api_keys']['tongyi_api_key']

    test_config = {
        'subject': request.subject,
        'topic': request.topic,
        'degree': request.degree,
        'time_limit': request.time_limit,
        'questions': request.questions
    }

    try:
        # 生成试卷并保存到数据库
        test_data, exam_id = generate_online_test(test_config, api_key, save_to_db=True)

        if not test_data:
            raise HTTPException(status_code=500, detail="试卷生成失败")

        if not exam_id:
            raise HTTPException(status_code=500, detail="试卷保存失败")

        # 从数据库导出试卷数据
        session = Session()
        try:
            exported_data = export_exam_to_json(session, exam_id)
            if not exported_data:
                raise HTTPException(status_code=500, detail="试卷导出失败")

            return OnlineTestResponse(
                exam_id=exam_id,
                questions=exported_data['questions'],
                test_info=exported_data['test_info']
            )
        finally:
            session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-exam/{exam_id}", response_model=OnlineTestResponse)
async def get_exam_endpoint(exam_id: int):
    try:
        session = Session()
        try:
            exported_data = export_exam_to_json(session, exam_id)
            if not exported_data:
                raise HTTPException(status_code=404, detail="试卷不存在")

            return OnlineTestResponse(
                exam_id=exam_id,
                questions=exported_data['questions'],
                test_info=exported_data['test_info']
            )
        finally:
            session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 在现有下载端点后添加图片下载端点
IMAGE_DIR = Path(__file__).parent.parent / "output" / "Images"


@app.get("/download/image/{filename}")
async def download_image(filename: str):
    """图片下载端点"""
    file_path = IMAGE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)
