# 练习题生成模块
from llm_integration import LLMFactory
from utils import exercise_prompt, answer_explanation_prompt


# 动态生成输入数据和模板
def create_dynamic_template(exercise_config):
    input_data = {}
    template_parts = []
    chinese_numbers = ["一", "二", "三", "四", "五"]  # 汉字编号
    section_index = 0  # 用于选择汉字编号

    if "choice_count" in exercise_config:
        input_data["choice_total"] = exercise_config["choice_score"] * exercise_config["choice_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、选择题（每小题{exercise_config["choice_score"]}分，共{exercise_config["choice_count"]}题，总计{input_data["choice_total"]}分）
        {{生成选择题内容}}
        """)
        section_index += 1

    if "fill_count" in exercise_config:
        input_data["fill_total"] = exercise_config["fill_score"] * exercise_config["fill_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、填空题（每小题{exercise_config["fill_score"]}分，共{exercise_config["fill_count"]}题，总计{input_data["fill_total"]}分）
        {{生成填空题内容}}
        """)
        section_index += 1

    if "judge_count" in exercise_config:
        input_data["judge_total"] = exercise_config["judge_score"] * exercise_config["judge_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、判断题（每小题{exercise_config["judge_score"]}分，共{exercise_config["judge_count"]}题，总计{input_data["judge_total"]}分）
        {{生成判断题内容}}
        """)
        section_index += 1

    if "short_answer_count" in exercise_config:
        input_data["short_answer_total"] = exercise_config["short_answer_score"] * exercise_config["short_answer_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、简答题（每小题{exercise_config["short_answer_score"]}分，共{exercise_config["short_answer_count"]}题，总计{input_data["short_answer_total"]}分）
        {{生成简答题内容}}
        """)
        section_index += 1

    if "application_count" in exercise_config:
        input_data["application_total"] = exercise_config["application_score"] * exercise_config["application_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、应用计算题（每小题{exercise_config["application_score"]}分，共{exercise_config["application_count"]}题，总计{input_data["application_total"]}分）
        {{生成应用计算题内容}}
        """)

    # 合并模板
    template = "\n".join(template_parts)
    return template, input_data


def generate_answers_and_explanations(subject, topic, questions, api_key):
    llm = LLMFactory.initialize_tongyi(api_key)
    prompt = answer_explanation_prompt.format(
        subject=subject, topic=topic, questions=questions
    )
    return llm.invoke(prompt)


def generate_exercises(subject, topic, degree, exercise_config, api_key):
    llm = LLMFactory.initialize_tongyi(api_key)

    # 生成模板和输入数据
    template, input_data = create_dynamic_template(exercise_config)

    prompt = exercise_prompt.format(
        subject=subject, topic=topic, degree=degree, **exercise_config, **input_data, template=template
    )
    exercises = llm.invoke(prompt)

    # 生成答案和解析
    answers_and_explanations = generate_answers_and_explanations(subject, topic, exercises, api_key)

    return exercises, answers_and_explanations
