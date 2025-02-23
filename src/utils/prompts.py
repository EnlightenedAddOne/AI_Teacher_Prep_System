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


def image_prompt():
    return None


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

# 资源推荐提示模板
book_recommendation_prompt = PromptTemplate(
    input_variables=["topic", "count"],
    template="""作为图书推荐专家，请推荐{count}本关于'{topic}'的权威教材或参考书籍。
要求：
1. 必须包含以下字段：title（书名）、authors（作者列表）、publisher（出版社）、publication_year（出版年份）
2. 优先推荐近5年的出版物
3. 使用严格JSON格式返回，结构示例：
{{"books": [
  {{
    "title": "计算机网络（第7版）",
    "authors": ["谢希仁"],
    "publisher": "电子工业出版社",
    "publication_year": 2023,
    "isbn": "9787121373133"
  }}
]}}"""
)

paper_recommendation_prompt = PromptTemplate(
    input_variables=["topic", "count"],
    template="""作为学术推荐专家，请推荐{count}篇关于'{topic}'的核心期刊论文。
要求：
1. 必须包含以下字段：title（标题）、authors（作者列表）、journal（期刊名称）、publication_year（发表年份）
2. 优先推荐近3年的高被引论文
3. 使用严格JSON格式返回，结构示例：
{{"papers": [
  {{
    "title": "TCP拥塞控制算法研究",
    "authors": ["李明", "王强"],
    "journal": "计算机学报",
    "publication_year": 2022,
    "doi": "10.1234/12345678"
  }}
]}}"""
)

video_recommendation_prompt = PromptTemplate(
    input_variables=["topic", "count"],
    template="""# 联网搜索指令
请使用web_search函数获取实时数据！

# 搜索参数
search_query: "{topic} 教学视频"
max_results: 10

# 筛选标准
1. 平台：哔哩哔哩
2. 发布时间：最近6个月
3. 播放量 ≥ 2万
4. 时长5-30分钟

# 输出格式
{{
  "videos": [
    {{
      "title": "视频标题（必须包含'{topic}'）",
      "url": "https://www.bilibili.com/video/BVxxx",
      "duration": "MM:SS",
      "view_count": "数字+万",
      "uploader": "认证机构名称",
      "score": 0-100
    }}
  ]
}}"""
)


integrated_recommendation_prompt = PromptTemplate(
    input_variables=["topic", "book_count", "paper_count", "video_count"],
    template="""请使用web_search工具搜索并推荐以下教育资源：

主题：{topic}
需求：
- {book_count}本相关书籍
- {paper_count}篇学术论文
- {video_count}个教学视频

搜索关键词：
1. "{topic} 教材 书籍 豆瓣"
2. "{topic} 论文 知网 核心期刊"
3. "{topic} 教学视频 bilibili"

请按以下JSON格式返回结果：
{{
  "recommendations": {{
    "books": [
      {{
        "title": "Python编程：从入门到实践",  # 示例
        "author": "埃里克·马瑟斯",
        "publisher": "人民邮电出版社",
        "publish_year": "2023",
        "douban_score": "9.2"
      }}
    ],
    "papers": [
      {{
        "title": "Python程序设计课程教学改革与实践",  # 示例
        "authors": ["张三", "李四"],
        "journal": "计算机教育",
        "publish_year": "2023",
        "citation_count": "12"
      }}
    ],
    "videos": [
      {{
        "title": "Python基础教程完整版",  # 示例
        "url": "https://www.bilibili.com/video/xxx",
        "duration_minutes": "45",
        "view_count": "12.5万",
        "platform": "bilibili"
      }}
    ]
  }}
}}

注意事项：
1. 必须使用web_search工具获取真实数据
2. 所有数值必须返回字符串格式
3. 确保资源质量（高评分、高引用、高播放量）
4. 优先推荐近两年的资源"""
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



