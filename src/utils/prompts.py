# Prompt模板定义
from langchain.prompts import PromptTemplate
from typing import Dict, Tuple, Any

# 教学设计的LangChain Prompt模板
teaching_design_prompt = PromptTemplate(
    input_variables=["subject", "topic", "goals", "duration", "grade"],
    template="""
        你是一位在教育领域拥有丰富经验的专家，精通教学设计的各个环节，能够从宏观和微观角度审视教学方案，发现潜在问题并提出切实可行的设计方案。你熟悉不同年龄段和学习水平学生的特点，能够根据学生特点调整教学策略，使教学内容更加贴合学生需求。
    请根据以下步骤为教师生成一份详细的教学设计方案,确保教学设计清晰、全面，符合教学目标，并且能够激发学生兴趣，提高课堂参与度。

    输出格式要求：
    1. 使用markdown格式
    2. 标题层级说明：
       - 所有数字编号的主标题(如"1 学科名称"、"2 课程主题"等)必须使用一个"#"号，这些都是同级的一级标题
       - 使用(1)、(2)等形式编号的子标题使用两个"#"号
       - 最下层的标题(如标题'9.小组讨论与互动'内容中的"环节内容"、"目的与作用"等)使用三个"#"号
    3. 不要包含任何XML标签

    # 1.学科名称：{subject}
    # 2.课程主题：{topic}
    # 3.教学目标：{goals}
    # 4.课程时长：{duration}
    # 5.重点难点：{{详细说明本课程的重难点}}
    # 6.教学活动安排：
      ## (1)导入新课（时间：{{导入新课时间}}分钟）
      ## (2)讲授新知（时间：{{讲授新知时间}}分钟）
      ## (3)小组讨论与互动（时间：{{小组讨论时间}}分钟）
      ## (4)实践练习（时间：{{实践练习时间}}分钟）
      ## (5)课堂小结与布置作业（时间：{{课堂小结时间}}分钟）

    # 7.教学内容：
      ## (1){{详细阐述内容要点1}}
      ## (2){{详细阐述内容要点2}}
      ## (3){{详细阐述内容要点3}}

    # 8.教学方法：
      ## (1){{教学方法1}}
      ## (2){{教学方法2}}
      ## (3){{教学方法3}}

    # 9.小组讨论与互动：
      ## (1)环节一
         ### 环节内容：{{详细阐述互动环节1内容}}
         ### 目的与作用：{{详细阐述互动环节1目的}}
      ## (2)环节二
         ### 环节内容：{{详细阐述互动环节2内容}}
         ### 目的与作用：{{详细阐述互动环节2目的}}
      ## (3)环节三
         ### 环节内容：{{详细阐述互动环节3内容}}
         ### 目的与作用：{{详细阐述互动环节3目的}}

    # 10.评估方式：
      ## (1){{评估方式1}}
      ## (2){{评估方式2}}
      ## (3){{评估方式3}}

    # 11.预期成果：
      ## (1){{预期成果1}}
      ## (2){{预期成果2}}
      ## (3){{预期成果3}}
    """
)


# 练习题生成的LangChain Prompt模板
def create_dynamic_template(exercise_config):
    # 动态生成输入数据和模板
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
    请根据以上教学方案和要求为下面学科的课程内容生成一份练习题。练习题涵盖的题型由下面提供的模板信息决定,确保题目内容准确、难度适中，能够全面考察学生对本课程主题的掌握情况。输出时请按照题型分类列出题目，并标注好题号和分值，题号连续。题目后面不需要跟答案。
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


def ppt_prompt():
    return None


def image_prompt():
    return None


def video_prompt():
    return None


def create_online_test_template() -> str:
    """
    生成在线测试题目模板字符串
    :return: 模板字符串
    """
    return """
    请根据以下要求生成适合在线测试的题目。每道题必须包含题目内容、选项、正确答案、解析等信息，并按照指定的JSON格式输出。

    学科：{subject}
    主题：{topic}
    难度：{degree}
    考试时长：{time_limit}分钟
    要求：
    1. 题目类型及分值要求：
    {test_requirements}

    2. 输出格式必须是合法的JSON格式
    3. 每道题的结构如下：
    {{
        "questions": [
            {{
                "number": "{question_number}",  // 题型序号(一/二/三/四/五)
                "type": "{question_type}",  // 题目类型(choice/fill/judge/short_answer/application)
                "score": {question_score},
                "id": "题目ID(自增数字)",
                "content": "题目内容",
                "options": [  // 选择题选项，判断题固定为["√","×"]
                    {{
                        "key": "选项标识(A/B/C/D)",
                        "value": "选项内容"
                    }}
                ],
                "correct_answer": "正确答案的选项标识",  // 选择题为选项标识，填空题为答案文本
                "explanation": "答案解析",
                "knowledge_points": ["相关知识点1", "相关知识点2"],  // 知识点标签
                "subject": "{subject}",
                "topic": "{topic}",
                "degree": "{degree}"
            }}
        ],
        "test_info": {{
            "total_score": {total_score},  // 试卷总分
            "time_limit": {time_limit}  // 考试时长(分钟)
        }}
    }}
    """


# 在线测试题目生成的模板
online_test_prompt = PromptTemplate(
    input_variables=[
        "subject", "topic", "degree", "time_limit",  # 基本信息
        "test_requirements",  # 题型要求文本
        "question_number", "question_type", "question_score",  # 题目信息
        "total_score"  # 试卷总分
    ],
    template=create_online_test_template()
)


def generate_test_requirements(test_config: Dict) -> Dict[str, Any]:
    """
    生成题型要求文本和相关数据
    :param test_config: {
        'subject': '学科名称',
        'topic': '课程主题',
        'degree': '难度(easy/medium/hard)',
        'time_limit': 考试时长(分钟),
        'questions': {
            'choice': {'count': 数量, 'score': 分值},
            'fill': {'count': 数量, 'score': 分值},
            ...
        }
    }
    :return: 模板所需的输入数据
    """
    input_data = {
        'subject': test_config['subject'],
        'topic': test_config['topic'],
        'degree': test_config['degree'],
        'time_limit': test_config['time_limit']
    }
    requirements = []
    
    # 题型中英文映射
    question_types = {
        'choice': '选择题',
        'fill': '填空题', 
        'judge': '判断题',
        'short_answer': '简答题',
        'application': '应用计算题'
    }
    
    # 汉字数字映射
    chinese_numbers = ['一', '二', '三', '四', '五']
    
    total_score = 0
    section_index = 0  # 用于动态分配题号
    
    # 遍历用户配置的题型（保持题型顺序）
    for q_type, q_config in test_config['questions'].items():
        if q_type in question_types:  # 确保是支持的题型
            name = question_types[q_type]
            total = q_config['count'] * q_config['score']
            requirements.append(
                f"   - {name}：每题{q_config['score']}分，共{q_config['count']}题，总计{total}分"
            )
            
            input_data.update({
                'question_number': chinese_numbers[section_index],  # 动态分配题号
                'question_type': question_types[q_type],  # 使用中文题型名称
                'question_score': q_config['score']
            })
            total_score += total
            section_index += 1
    
    input_data.update({
        'test_requirements': '\n'.join(requirements),
        'total_score': total_score
    })
    
    return input_data
