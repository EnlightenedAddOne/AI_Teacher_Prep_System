# 多媒体资源生成模块
from llm_integration import LLMFactory
from utils.prompts import ppt_prompt, image_prompt, video_prompt
from langchain_community.tools import DalleTool
from langchain_community.tools import StableDiffusionTool
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os


class MultimediaGenerator:
    """多媒体资源生成器"""

    def __init__(self, api_key: str):
        """
        初始化多媒体生成器
        :param api_key: API密钥
        """
        self.llm = LLMFactory.initialize_tongyi(api_key)
        self.image_generator = DalleTool(api_key=api_key)
        self.video_generator = None  # 待接入视频生成API

    def generate_ppt(self, subject: str, topic: str, content: str, output_path: str):
        """
        生成PPT
        :param subject: 学科
        :param topic: 主题
        :param content: 教学内容
        :param output_path: 输出路径
        :return: PPT文件路径
        """
        # 使用LLM生成PPT大纲和内容
        prompt = ppt_prompt.format(
            subject=subject,
            topic=topic,
            content=content
        )
        ppt_content = self.llm.invoke(prompt)

        # 将内容转换为PDF格式(示例)
        c = canvas.Canvas(output_path, pagesize=A4)
        c.drawString(100, 750, f"主题: {topic}")
        c.drawString(100, 700, ppt_content)
        c.save()

        return output_path

    def generate_images(self,
                        description: str,
                        count: int = 1,
                        size: str = "1024x1024",
                        output_dir: str = "output/images"):
        """
        生成教学相关图片
        :param description: 图片描述
        :param count: 生成数量
        :param size: 图片尺寸
        :param output_dir: 输出目录
        :return: 生成的图片路径列表
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        image_paths = []
        for i in range(count):
            # 使用DALL-E生成图片
            prompt = image_prompt.format(description=description)
            image_url = self.image_generator.run(prompt)

            # 保存图片
            image_path = os.path.join(output_dir, f"image_{i}.png")
            # TODO: 下载并保存图片
            image_paths.append(image_path)

        return image_paths

    def generate_video(self,
                       script: str,
                       duration: int,
                       style: str = "教学",
                       output_path: str = "output/videos/lesson.mp4"):
        """
        生成教学视频
        :param script: 视频脚本
        :param duration: 视频时长(秒)
        :param style: 视频风格
        :param output_path: 输出路径
        :return: 视频文件路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 使用LLM优化视频脚本
        prompt = video_prompt.format(
            script=script,
            duration=duration,
            style=style
        )
        enhanced_script = self.llm.invoke(prompt)

        # TODO: 接入视频生成API
        # self.video_generator.generate(
        #     script=enhanced_script,
        #     output_path=output_path
        # )

        return output_path

    def generate_teaching_materials(self,
                                    subject: str,
                                    topic: str,
                                    content: str,
                                    requirements: dict):
        """
        根据教学需求生成完整的多媒体教学资料
        :param subject: 学科
        :param topic: 主题
        :param content: 教学内容
        :param requirements: 具体需求
        :return: 生成的资源路径字典
        """
        resources = {}

        # 生成PPT
        if requirements.get("ppt", False):
            ppt_path = self.generate_ppt(
                subject=subject,
                topic=topic,
                content=content,
                output_path=f"output/ppt/{topic}.pdf"
            )
            resources["ppt"] = ppt_path

        # 生成配图
        if requirements.get("images", False):
            image_count = requirements.get("image_count", 3)
            image_paths = self.generate_images(
                description=f"{subject} {topic} 教学插图",
                count=image_count
            )
            resources["images"] = image_paths

        # 生成视频
        if requirements.get("video", False):
            video_duration = requirements.get("video_duration", 300)  # 默认5分钟
            video_path = self.generate_video(
                script=content,
                duration=video_duration
            )
            resources["video"] = video_path

        return resources


# 使用示例
if __name__ == "__main__":
    generator = MultimediaGenerator(api_key="your_api_key")

    # 生成教学资料
    materials = generator.generate_teaching_materials(
        subject="数学",
        topic="勾股定理",
        content="通过实例讲解勾股定理的概念和应用...",
        requirements={
            "ppt": True,
            "images": True,
            "image_count": 5,
            "video": True,
            "video_duration": 300
        }
    )

    print("生成的资源路径:", materials)
