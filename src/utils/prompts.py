# Prompt模板定义
from langchain.prompts import PromptTemplate

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


def pptx_prompt() -> str:
    """PPT生成提示词模板"""
    return '''你是一位PPT设计专家。请根据以下教学设计内容生成PPT结构和配音文案。要求如下：
1. 生成一个包含封面和多个章节的PPT结构
2. 每个章节包含标题、要点和讲解文案
3. 确保内容逻辑清晰，适合教学使用
4. 输出格式为JSON，包含以下字段：
   - title: PPT标题
   - title_narration: 封面讲解文案
   - sections: 章节列表，每个章节包含：
     - title: 章节标题
     - points: 章节要点列表
     - narration: 章节讲解文案

示例格式：
{
    "title": "PPT标题",
    "title_narration": "封面讲解文案",
    "sections": [
        {
            "title": "章节标题1",
            "points": ["要点1", "要点2"],
            "narration": "章节讲解文案1"
        },
        {
            "title": "章节标题2",
            "points": ["要点1", "要点2"],
            "narration": "章节讲解文案2"
        }
    ]
}

教学设计内容：
{content}'''


ppt_prompt = PromptTemplate(
    input_variables=["content"],
    template=pptx_prompt()
)


def image_prompt() -> str:
    """教学图片生成提示词模板"""
    return """
    你是一位专业的教学图片设计专家。请根据以下教学内容，生成一个详细的图片描述提示词，用于生成教学图片。

    教学内容: {description}

    要求：
    1. 图片类型可以是：
       - 流程图：展示步骤、过程或因果关系
       - 结构图：展示概念之间的关系、层次或组成部分
       - 实物图：展示具体物体、设备或现象
       - 对比图：展示不同概念的异同
       - 统计图：展示数据关系或变化趋势
       
    2. 图片要求：
       - 清晰度：4K高清质量
       - 风格：扁平化设计，简洁明快
       - 配色：使用适合教育的柔和色调
       - 布局：主次分明，重点突出
       
    3. 教学特点：
       - 适合目标年级学生理解
       - 突出教学重点和难点
       - 便于教师讲解和学生理解
       
    请生成DALL-E图片生成提示词，确保包含以下要素：
    - 图片类型说明
    - 具体内容描述
    - 视觉风格要求
    - 布局和构图说明
    - 教学用途说明
    """


def video_prompt():
    return None


# 在线测试题目生成的LangChain Prompt模板
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
        "test_info": [
            {{
                "total_score": {total_score},  // 试卷总分
                "time_limit": {time_limit}  // 考试时长(分钟)
            }}
        ]
    }}
    """


online_test_prompt = PromptTemplate(
    input_variables=[
        "subject", "topic", "degree", "time_limit",  # 基本信息
        "test_requirements",  # 题型要求文本
        "question_number", "question_type", "question_score",  # 题目信息
        "total_score"  # 试卷总分
    ],
    template=create_online_test_template()
)

# 演讲稿优化提示词
text_polishing_prompt = PromptTemplate(
    input_variables=[
        "original_text"
    ],
    template="""
        请对以下演讲稿文本进行润色优化，特别关注段落间的自然过渡与连接词使用：
        {original_text}
        
        要求：
        1. 保持原有技术内容的准确性
        2. 优化段落间过渡语句，使用更自然的连接词（例如：接下来、在此基础上、值得关注的是等）
        3. 输出为规范的JSON格式：
        {{
            "enhanced": [
                "优化后段落1",
                "优化后段落2",
                // ...其他段落...
            ]
        }}
        4. 确保JSON格式严格合规，可直接被Python的json模块解析
        5. 保留原始段落顺序，空段落保持为空字符串""
        6. 每个段落必须使用至少1个连接词
        
        示例：
        原始段落：'这部分我将探讨TCP协议概述...'
        优化后应标注：
        {{
            "enhanced": [
                "接下来我们将系统探讨...值得关注的是...",
                // ...其他优化段落...
            ]
        }}
        """
)