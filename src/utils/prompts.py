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

# 资源推荐提示模板
integrated_recommendation_prompt = PromptTemplate(
    input_variables=["topic", "book_count", "paper_count"],
    template="""请使用web_search工具搜索并推荐以下教育资源：

主题：{topic}

1. 书籍推荐要求：
   - 需要推荐 {book_count} 本书
   - 优先推荐近5年出版的教材或专业书籍
   - 必须包含：书名、作者、出版社、出版年份、ISBN号（如有）
   - 必须使用web_search验证信息准确性
   - 优先选择：
     * 知名出版社出版的教材
     * 被广泛使用的经典著作
     * 评分较高的专业书籍

2. 论文推荐要求：
   - 需要推荐 {paper_count} 篇论文
   - 优先推荐近3年发表的核心期刊论文
   - 必须包含：标题、作者、期刊名称、发表年份、DOI（如有）
   - 必须使用web_search验证信息准确性
   - 优先选择：
     * 高引用量的论文
     * 核心期刊发表的论文
     * 最新研究成果

请按以下JSON格式返回：
{{
    "books": [
        {{
            "title": "书名",
            "author": "作者",
            "publisher": "出版社",
            "year": "出版年份",
            "isbn": "ISBN号（如有）"
        }}
    ],
    "papers": [
        {{
            "title": "论文标题",
            "author": "作者",
            "journal": "期刊名称",
            "year": "发表年份",
            "doi": "DOI号（如有）"
        }}
    ]
}}

注意事项：
1. 必须使用web_search工具获取真实数据
2. 所有信息必须来自搜索结果
3. 不要生成虚假信息
4. 优先推荐近期出版或发表的资源
5. 宁可推荐少也不要推荐虚假信息
6. 如果搜索失败，返回空数组而不是虚构数据
7. 确保所有推荐的资源都与主题高度相关
8. 对于每个推荐项，都需要通过web_search验证其真实性"""
)

# 演讲稿优化提示词
text_polishing_prompt = PromptTemplate(
    input_variables=[
        "original_text"
    ],
    template="""
        请对以下演讲稿文本进行润色优化，特别关注段落间的自然过渡与连接词使用：
        {original_text}
        
        已知：
        1. 原始数据是一个文本列表，列表中的每个元素对应ppt每一页的讲授稿中，其中每页讲的内容都用逗号隔开了，你在处理时须将其作为一个整体
        
        要求：
        1. 保持原有技术内容的准确性
        2. 将原文本优化润色使其更加通顺流畅，同时注意页与页之间的连接词使用，避免多次使用同一个连接词。
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
        6. 你的角色是一位老师，授课对象仅是学生，修改原始文案使其更加符合老师的语气

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

# PPT大纲生成提示词
ppt_outline_prompt = PromptTemplate(
    input_variables=["subject", "topic"],
    template="""作为一个专业的教育PPT设计专家，请为{subject}学科的{topic}课程，生成一份适合教学使用的PPT大纲。
要求：
1. 结构清晰，层次分明
2. PPT封面大标题使用{topic}
3. 每个章节要有明确的标题
4. 将章节控制在六点以内
5. 适合课堂教学使用
6. 输出格式为JSON，包含以下字段：
   - title: PPT标题
   - sections: 章节数组，每个章节包含：
     - title: 章节标题
     - points: 要点数组

"""
)

# AI批改提示模板
ai_grading_system_prompt = PromptTemplate(
    input_variables=["question_type", "max_score"],
    template="""
    你是一个专业的教育评分AI，需要严格按照以下规则评分：
    1. 题型：{question_type}
    2. 评分规则：
       - 填空题：逐空比对答案，每空完全正确得部分分，全部正确得满分
       - 简答题：根据关键知识点覆盖度和表述准确性评分
       - 应用题：按解题步骤、公式应用和最终结果综合评分
    3. 满分：{max_score}分
    4. 给出0~{max_score}之间的分数，可以是小数
    """
)

ai_grading_user_prompt = PromptTemplate(
    input_variables=["correct_answer", "student_answer"],
    template="""
    请根据以下内容评分：
    【正确答案】
    {correct_answer}
    
    【学生答案】
    {student_answer}
    
    请直接返回JSON格式：{{"score": 分数}}
    """
)
