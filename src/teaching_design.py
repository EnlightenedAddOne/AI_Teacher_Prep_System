# 教学设计模块
from llm_integration import initialize_llm_Tongyi
from utils.prompts import teaching_design_prompt


def generate_teaching_design(subject, topic, goals, duration, grade, api_key):

    llm = initialize_llm_Tongyi(api_key)

    prompt = teaching_design_prompt.format(
        subject=subject, topic=topic, goals=goals, duration=duration, grade=grade
    )
    return llm.invoke(prompt)
