# 程序入口
import logging
import os
from pathlib import Path
import datetime

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from Multimedia import BingImagesSpider, ResourceRecommender, get_bilibili_videos
from Online_Test import generate_online_test
from configs import config
from education_sql import Session, export_exam_to_json

from exercise_generation import generate_exercises
from models import (TeachingDesignRequest, ExerciseRequest,
                    TeachingDesignResponse, ExerciseResponse,
                    OnlineTestRequest, OnlineTestResponse, TeachingImage,
                    RecommendedBook, RecommendedPaper, RecommendedVideo)
from pdf_generator import content_to_pdf
from teaching_design import generate_teaching_design
from utils import setup_cors  # 导入工具函数
from ppt_turn_video import create_ppt_videos

app = FastAPI()

# 使用工具函数设置 CORS 中间件
setup_cors(app)

# 配置静态文件服务
app.mount("/static-images", StaticFiles(directory=r'E:\AIdev\LangChain\host_2\Langchain\output\Images'), name="images")
app.mount("/ppt-videos", StaticFiles(directory=r'E:\AIdev\LangChain\host_2\Langchain\output\Ppt-turn-video'), name="ppt-videos")

logger = logging.getLogger(__name__)

router = APIRouter()


# 在路由处理函数前添加ID生成函数
def generate_design_id():
    """生成唯一教学设计ID TD-年月日-时分秒"""
    now = datetime.datetime.now()
    return f"TD-{now.strftime('%Y%m%d-%H%M%S')}"


# 教学设计
@app.post("/generate-teaching-design", response_model=TeachingDesignResponse)
async def generate_teaching_design_endpoint(request: TeachingDesignRequest):
    tongyi_api_key = config['api_keys'].get('tongyi_api_key')
    deepseek_api_key = config['api_keys'].get('deepseek_api_key')
    images = []
    video_path = None
    books = []
    papers = []
    videos = []

    if not tongyi_api_key:
        raise HTTPException(status_code=500, detail="通义API密钥未配置")
    if not deepseek_api_key:
        raise HTTPException(status_code=500, detail="Deepseek API密钥未配置")

    try:
        # 生成教学设计内容
        content = generate_teaching_design(
            request.subject, request.topic, request.goals,
            request.duration, request.grade, tongyi_api_key
        )
        # 使用 content_to_pdf 生成 PDF
        pdf_urls = content_to_pdf([content], ["教学设计"], ["teaching_design.pdf"])

        # 如果需要图片，调用爬虫
        if request.with_images and request.image_count > 0:
            try:
                spider = BingImagesSpider(
                    keyword=request.topic,
                    amount=request.image_count,
                    proxy_list=["http://127.0.0.1:8080"]
                )
                image_data = spider.run()
                images = [
                    TeachingImage(
                        title=img['title'],
                        url=img['url'],
                        type=img['type'],
                        md5=img['md5'],
                        download_url=f"/static-images/{Path(img['local_path']).name}" if img.get('local_path') else ""
                    ) for img in image_data if img.get('local_path')
                ]
            except Exception as e:
                logger.error(f"图片爬取失败: {str(e)}")

        # 如果需要生成视频
        if request.ppt_turn_video:
            try:
                # 调用ppt_turn_video中的函数生成视频
                output_video_path = await create_ppt_videos(
                    api_key=deepseek_api_key,
                    subject=request.subject,
                    topic=request.topic,
                    voice_type=request.voice_type  # 直接传递中文声线名称
                )

                # 设置相对路径用于返回
                video_path = f"/ppt-videos/{os.path.basename(os.path.dirname(output_video_path))}/output.mp4"

            except Exception as e:
                logger.error(f"视频生成失败: {str(e)}")

        # 如果需要推荐资源
        if request.resource_recommendation:
            try:
                # 获取书籍和论文推荐
                if (request.resource_recommendation.require_books and request.resource_recommendation.book_count > 0) or \
                   (request.resource_recommendation.require_papers and request.resource_recommendation.paper_count > 0):
                    # 初始化资源推荐器
                    recommender = ResourceRecommender()
                    recommendations = recommender.recommend_books_and_papers(
                        topic=request.topic,
                        book_count=request.resource_recommendation.book_count if request.resource_recommendation.require_books else 0,
                        paper_count=request.resource_recommendation.paper_count if request.resource_recommendation.require_papers else 0
                    )

                    # 转换书籍推荐为响应模型
                    if request.resource_recommendation.require_books and request.resource_recommendation.book_count > 0:
                        books = [
                            RecommendedBook(
                                title=book['title'],
                                authors=[book['author']],
                                publisher=book['publisher'],
                                publication_year=book['year'],
                                isbn=book.get('isbn')
                            ) for book in recommendations.get('books', [])
                        ]

                    # 转换论文推荐为响应模型
                    if request.resource_recommendation.require_papers and request.resource_recommendation.paper_count > 0:
                        papers = [
                            RecommendedPaper(
                                title=paper['title'],
                                authors=[paper['author']],
                                journal=paper['journal'],
                                publication_year=paper['year'],
                                doi=paper.get('doi')
                            ) for paper in recommendations.get('papers', [])
                        ]

                # 获取视频推荐
                if request.resource_recommendation.require_videos and request.resource_recommendation.video_count > 0:
                    video_results = get_bilibili_videos(
                        course_name=request.topic,
                        video_count=request.resource_recommendation.video_count
                    )
                    videos = [
                        RecommendedVideo(
                            title=video['title'],
                            platform="Bilibili",
                            url=video['url'],
                            duration=video['duration'],
                            view_count=video['view_count']
                        ) for video in video_results
                    ]

            except Exception as e:
                logger.error(f"资源推荐失败: {str(e)}")

        return TeachingDesignResponse(
            design_id=generate_design_id(),
            content=content,
            teach_pdf_url=pdf_urls[0],
            images=images if request.with_images and request.image_count > 0 else None,
            ppt_video_path=video_path if request.ppt_turn_video else None,
            books=books if request.resource_recommendation and request.resource_recommendation.require_books and request.resource_recommendation.book_count > 0 else None,
            papers=papers if request.resource_recommendation and request.resource_recommendation.require_papers and request.resource_recommendation.paper_count > 0 else None,
            videos=videos if request.resource_recommendation and request.resource_recommendation.require_videos and request.resource_recommendation.video_count > 0 else None
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
