# 练习题生成模块
from llm_integration import initialize_llm_Tongyi
from utils.prompts import exercise_prompt, answer_explanation_prompt, create_dynamic_template


def generate_answers_and_explanations(subject, topic, questions, api_key):
    llm = initialize_llm_Tongyi(api_key)
    prompt = answer_explanation_prompt.format(
        subject=subject, topic=topic, questions=questions
    )
    return llm.invoke(prompt)


def generate_exercises(subject, topic, degree, exercise_config, api_key):
    llm = initialize_llm_Tongyi(api_key)
    
    # 生成模板和输入数据
    template, input_data = create_dynamic_template(exercise_config)
    
    prompt = exercise_prompt.format(
        subject=subject, topic=topic, degree=degree, **exercise_config, **input_data, template=template
    )
    exercises = llm.invoke(prompt)

    # 生成答案和解析
    answers_and_explanations = generate_answers_and_explanations(subject, topic, exercises, api_key)

    return exercises, answers_and_explanations



