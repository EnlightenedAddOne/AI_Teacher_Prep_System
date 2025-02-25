# 教学设计模块
from llm_integration import LLMFactory
from utils import teaching_design_prompt


def generate_teaching_design(subject, topic, goals, duration, grade, api_key):
    """
    生成教学设计
    :param subject: 学科名称
    :param topic: 课程主题
    :param goals: 教学目标
    :param duration: 课程时长
    :param grade: 年级
    :param api_key: 通义千问API密钥
    :return: 生成的教学设计内容
    """
    # 初始化API
    LLMFactory.initialize_tongyi(api_key)

    # 构建消息
    messages = [{
        "role": "user",
        "content": teaching_design_prompt.format(
            subject=subject,
            topic=topic,
            goals=goals,
            duration=duration,
            grade=grade
        )
    }]

    # 调用API生成教学设计
    response = LLMFactory.call_tongyi(messages, model_name="qwen-plus-2025-01-25")
    return response.get('content', '') if response else ''
