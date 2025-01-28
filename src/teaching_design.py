# 教学设计模块
from llm_integration import LLMFactory
from utils.prompts import teaching_design_prompt


def generate_teaching_design(subject, topic, goals, duration, grade, api_key):

    llm = LLMFactory.initialize_tongyi(api_key)

    prompt = teaching_design_prompt.format(
        subject=subject, topic=topic, goals=goals, duration=duration, grade=grade
    )
    return llm.invoke(prompt)
