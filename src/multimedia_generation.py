# 多媒体资源生成模块
from llm_integration import initialize_llm_Tongyi
from utils.prompts import multimedia_prompt


def generate_multimedia(subject, topic, content_points, api_key):
    llm = initialize_llm_Tongyi(api_key)
    prompt = multimedia_prompt().format(
        subject=subject, topic=topic, content_points=content_points
    )
    return llm(prompt)
