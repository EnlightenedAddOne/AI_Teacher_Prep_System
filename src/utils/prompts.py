# Prompt模板定义
from langchain.prompts import PromptTemplate

# 教学设计的LangChain Prompt模板
teaching_design_prompt = PromptTemplate(
    input_variables=["subject", "topic", "goals", "duration", "grade"],
    template="""
    你是一位在教育领域拥有丰富经验的专家，精通教学设计的各个环节，能够从宏观和微观角度审视教学方案，发现潜在问题并提出切实可行的设计方案。你熟悉不同年龄段和学习水平学生的特点，能够根据学生特点调整教学策略，使教学内容更加贴合学生需求。
    请根据以下步骤为教师生成一份详细的教学设计方案,确保教学设计清晰、全面，符合教学目标，并且能够激发学生兴趣，提高课堂参与度。输出不应包含任何XML标签。一级标号从"学科名称"开始。输出的一级标题的标号为1、2、3，二级标题的标号为(1)、(2)、(3)，三级标题的标号为1)、2)、3)。
    
    1. **学科名称**：{subject}
    2. **课程主题**：{topic}
    3. **教学目标**：{goals}
    4. **课程时长**：{duration}
    5. **教学活动安排**：
    (1) 导入新课（时间：{{导入新课时间}}分钟）
    (2) 讲授新知（时间：{{讲授新知时间}}分钟）
    (3) 小组讨论与互动（时间：{{小组讨论时间}}分钟）
    (4) 实践练习（时间：{{实践练习时间}}分钟）
    (5) 课堂小结与布置作业（时间：{{课堂小结时间}}分钟）

    6. **教学内容**：
    (1) {{内容要点1}}
    (2) {{内容要点2}}
    (3) {{内容要点3}}

    7. **教学方法**：
    (1) {{教学方法1}}
    (2) {{教学方法2}}
    (3) {{教学方法3}}

    8. **小组讨论与互动**：
    (1) 环节一
        ***环节内容***：{{互动环节1内容}}
        ***目的与作用***：{{互动环节1目的}}
    (2) 环节二
        ***环节内容***：{{互动环节2内容}}
        ***目的与作用***：{{互动环节2目的}}
    (3) 环节三
        ***环节内容***：{{互动环节3内容}}
        ***目的与作用***：{{互动环节3目的}}

    9. **评估方式**：
    (1) {{评估方式1}}
    (2) {{评估方式2}}
    (3) {{评估方式3}}

    10. **预期成果**：
    (1) {{预期成果1}}
    (2) {{预期成果2}}
    (3) {{预期成果3}}
    """
)


def create_dynamic_template(exercise_config):
    # 动态生成输入数据和模板
    input_data = {}
    template_parts = []
    chinese_numbers = ["一", "二", "三", "四", "五"]  # 汉字编号
    section_index = 0  # 用于选择汉字编号

    if "choice_count" in exercise_config:
        input_data["choice_total"] = exercise_config["choice_score"] * exercise_config["choice_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、选择题（每题{exercise_config["choice_score"]}分，共{exercise_config["choice_count"]}题，总计{input_data["choice_total"]}分）
        {{生成选择题内容}}
        """)
        section_index += 1

    if "fill_count" in exercise_config:
        input_data["fill_total"] = exercise_config["fill_score"] * exercise_config["fill_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、填空题（每题{exercise_config["fill_score"]}分，共{exercise_config["fill_count"]}题，总计{input_data["fill_total"]}分）
        {{生成填空题内容}}
        """)
        section_index += 1

    if "judge_count" in exercise_config:
        input_data["judge_total"] = exercise_config["judge_score"] * exercise_config["judge_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、判断题（每题{exercise_config["judge_score"]}分，共{exercise_config["judge_count"]}题，总计{input_data["judge_total"]}分）
        {{生成判断题内容}}
        """)
        section_index += 1

    if "short_answer_count" in exercise_config:
        input_data["short_answer_total"] = exercise_config["short_answer_score"] * exercise_config["short_answer_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、简答题（每题{exercise_config["short_answer_score"]}分，共{exercise_config["short_answer_count"]}题，总计{input_data["short_answer_total"]}分）
        {{生成简答题内容}}
        """)
        section_index += 1

    if "application_count" in exercise_config:
        input_data["application_total"] = exercise_config["application_score"] * exercise_config["application_count"]
        template_parts.append(f"""
        {chinese_numbers[section_index]}、应用计算题（每题{exercise_config["application_score"]}分，共{exercise_config["application_count"]}题，总计{input_data["application_total"]}分）
        {{生成应用计算题内容}}
        """)

    # 合并模板
    template = "\n".join(template_parts)
    return template, input_data


exercise_prompt = PromptTemplate(
    input_variables=[
        "subject", "topic", "degree",
        "choice_score", "choice_count", "choice_total",
        "fill_score", "fill_count", "fill_total",
        "judge_score", "judge_count", "judge_total",
        "short_answer_score", "short_answer_count", "short_answer_total",
        "application_score", "application_count", "application_total",
        "template"
    ],
    template="""
    请根据以上教学方案和要求为下面学科的课程内容生成一份练习题。练习题涵盖的题型由下面提供的模板信息决定,确保题目内容准确、难度适中，能够全面考察学生对本课程主题的掌握情况。输出时请按照题型分类列出题目，并标注好题号和分值。题目后面不需要跟答案。
    "学科":{subject}, "课程内容":{topic}, "难易程度":{degree}。
    {template}
    """
)

# 答案和解析生成的LangChain Prompt模板
answer_explanation_prompt = PromptTemplate(
    input_variables=[
        "subject", "topic", "questions"
    ],
    template="""
    请为以下{subject}的{topic}练习题生成答案和详细解析。直接输出答案和解析，不用再把题目内容输出一遍了。确保答案准确，解析清晰，能够帮助学生理解每道题的解题思路和知识点。

    练习题：
    {questions}

    输出格式：
    1.答案：{{答案}}
      解析：{{解析}}

    2.答案：{{答案}}
      解析：{{解析}}

    （以此类推，根据需要生成相应数量的答案和解析）
    """
)


def multimedia_prompt():
    return None
