# AI-ZGLOSH

## 项目结构

```
AI-ZGLOSH/
├── src/                        # 源代码目录
│   ├── configs/                # 配置文件目录
│   │   ├── __init__.py        # 配置模块初始化
│   │   ├── config.ini         # 配置文件(API密钥和数据库配置)
│   │   └── config_get.py      # 配置读取工具
│   │
│   ├── education_sql/         # 数据库相关代码
│   │   ├── __init__.py        # 导出主要接口
│   │   ├── Create.py          # 数据库模型定义
│   │   ├── read.py            # 数据读取操作
│   │   ├── write_data.py      # 数据写入操作
│   │   ├── updatedelete.py    # 更新和删除操作
│   │   └── main.py            # 数据库维护工具
│   │
│   ├── models/                # 数据模型
│   │   ├── __init__.py        # 导出所有模型
│   │   ├── request_models.py  # 请求数据模型
│   │   └── response_models.py # 响应数据模型
│   │
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   ├── helpers.py         # 通用辅助函数
│   │   └── prompts.py         # 提示词模板
│   │
│   ├── ziti/                  # 字体文件
│   │   └── simkai.ttf         # 楷体字体
│   │
│   ├── llm_integration.py     # LLM模型集成
│   ├── Online_Test.py         # 在线测试生成
│   ├── exercise_generation.py # 习题生成
│   ├── teaching_design.py     # 教学设计生成
│   ├── multimedia_generation.py # 多媒体资源生成
│   ├── pdf_generator.py       # PDF文档生成
│   ├── Image_crawling.py      # 图片爬取
│   ├── langserve_app.py       # FastAPI应用主程序
│   └── main.py               # 测试程序
│
├── output/                    # 输出文件目录
│   ├── PDF/                  # 生成的PDF文件
│   └── multimedia/          # 生成的多媒体文件
│
└── requirements.txt          # 项目依赖
```

## 功能特性

1. 教学设计生成
   - 根据学科、主题、教学目标等生成完整教案
   - 支持生成PPT和教学视频
   - 可导出为PDF格式

2. 在线测试系统
   - 支持多种题型：选择题、填空题、判断题、简答题、应用题
   - 自动生成试卷和答案解析
   - 试卷数据持久化存储

3. 习题生成
   - 根据知识点生成练习题
   - 提供详细的答案和解析
   - 支持难度调节

4. 多媒体资源生成
   - 自动生成教学PPT
   - 支持PPT转视频
   - 图片资源获取

## 环境要求

1. Python 3.8+
2. MySQL 8.0+
3. 系统依赖：
   - unoconvert (用于PPT转换)
   - ffmpeg (用于视频处理)

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-username/AI-ZGLOSH.git
cd AI-ZGLOSH
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库
```sql
CREATE DATABASE online_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. 配置API密钥
编辑 `src/configs/config.ini`:
```ini
[API_KEYS]
tongyi_api_key = your_tongyi_api_key
zhipu_api_key = your_zhipu_api_key

[DATABASE]
host = localhost
port = 3306
user = your_username
password = your_password
database = online_test
```

## 使用方法

1. 启动服务器
```bash
cd src
uvicorn langserve_app:app --reload
```

1. API接口说明

以下请求格式和响应格式中的各字段的含义请具体参考models目录下定义的请求模型和响应模型
- 生成教学设计：

请求格式：
```bash
POST http://0.0.0.0:8000/generate-teaching-design
{
    "subject": "计算机网络",
    "topic": "TCP协议",
    "goals": "掌握相关知识",
    "duration": "80",
    "grade": "大二",
    "with_images": false,
    "image_count": 2,
    "ppt_turn_video":true,
    "voice_type": "温暖女声",
    "resource_recommendation": {
        "require_books": false,
        "book_count": 3,
        "require_papers": false,
        "paper_count": 4,
        "require_videos": false,
        "video_count": 3
    }
}

```
响应格式：
```bash
{
    "content":  # 教学设计markdown格式的文本内容
    "teach_pdf_url": # 教学设计PDF文档
    "images": # 图片
    "ppt_video_path": # AI生成视频
    "books": # 推荐书籍
    "papers": # 推荐论文
    "videos": # 推荐视频
    "design_id": # 唯一ID
}
```

- 生成练习题：

请求格式：
```bash
POST http://0.0.0.0:8000/generate-exercises
{
    "subject": "计算机网络",
    "topic": "网络协议",
    "degree": "困难",
    "exercise_config": {
        "choice_score": 10,
        "choice_count": 3,
        "fill_score": 10,
        "fill_count": 2,
        "application_score": 20,
        "application_count": 1
    }
}
```
响应格式：
```bash
{
    "exercises":  # 练习题文本内容
    "answers_and_explanations":  # 答案解析文本内容
    "exercises_pdf_url":  # 练习题PDF文档
    "answers_pdf_url":  # 答案解析PDF文档
}


```

- 生成在线测试：

请求格式示例：
```bash
POST http://0.0.0.0:8000/generate-online-test
{
    "subject": "数学",
    "topic": "函数",
    "degree": "中等",
    "time_limit": 45,
    "questions": {
        "choice": {"count": 5, "score": 2},
        "fill": {"count": 3, "score": 3},
        "judge": {"count": 4, "score": 1},
        "short_answer": {"count": 2, "score": 5},
        "application": {"count": 2, "score": 10}
    }
}
```
响应格式示例：
```bash
{
    "exam_id": 2,
    "questions": [
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 1,
            "content": "已知函数f(x) = ax^2 + bx + c，若其图像通过点(1, 3)和(-1, 5)，则a + b + c的值为：",
            "options": [
                {
                    "key": "A",
                    "value": "3"
                },
                {
                    "key": "B",
                    "value": "4"
                },
                {
                    "key": "C",
                    "value": "5"
                },
                {
                    "key": "D",
                    "value": "6"
                }
            ],
            "correct_answer": "B",
            "explanation": "根据题目条件，代入点(1, 3)和(-1, 5)可以得到两个方程：a + b + c = 3 和 a - b + c = 5。解这两个方程可得a + b + c = 4。",
            "knowledge_points": [
                "方程求解"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 2,
            "content": "设函数f(x) = e^x + ln(x)，则f'(x)等于：",
            "options": [
                {
                    "key": "A",
                    "value": "e^x + 1/x"
                },
                {
                    "key": "B",
                    "value": "e^x - 1/x"
                },
                {
                    "key": "C",
                    "value": "e^x * ln(x)"
                },
                {
                    "key": "D",
                    "value": "e^x / x"
                }
            ],
            "correct_answer": "A",
            "explanation": "根据导数规则，e^x的导数是e^x，ln(x)的导数是1/x。因此f'(x) = e^x + 1/x。",
            "knowledge_points": [],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 3,
            "content": "已知函数f(x) = sin(x) + cos(x)，则其最大值为：",
            "options": [
                {
                    "key": "A",
                    "value": "1"
                },
                {
                    "key": "B",
                    "value": "√2"
                },
                {
                    "key": "C",
                    "value": "2"
                },
                {
                    "key": "D",
                    "value": "π/2"
                }
            ],
            "correct_answer": "B",
            "explanation": "使用三角恒等变换sin(x) + cos(x) = √2 * sin(x + π/4)，最大值为√2。",
            "knowledge_points": [],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 4,
            "content": "函数f(x) = x^3 - 3x^2 + 2在区间[0, 2]上的最小值为：",
            "options": [
                {
                    "key": "A",
                    "value": "-2"
                },
                {
                    "key": "B",
                    "value": "0"
                },
                {
                    "key": "C",
                    "value": "1"
                },
                {
                    "key": "D",
                    "value": "2"
                }
            ],
            "correct_answer": "A",
            "explanation": "求导f'(x) = 3x^2 - 6x，令f'(x) = 0得驻点x = 0或x = 2。计算f(0) = 2，f(2) = -2，故最小值为-2。",
            "knowledge_points": [],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 5,
            "content": "设f(x) = |x|，g(x) = x^2，则复合函数(f ∘ g)(x) = ：",
            "options": [
                {
                    "key": "A",
                    "value": "x^2"
                },
                {
                    "key": "B",
                    "value": "|x|^2"
                },
                {
                    "key": "C",
                    "value": "x^4"
                },
                {
                    "key": "D",
                    "value": "|x^2|"
                }
            ],
            "correct_answer": "A",
            "explanation": "根据复合函数定义，(f ∘ g)(x) = f(g(x)) = |x^2| = x^2。",
            "knowledge_points": [
                "绝对值函数",
                "复合函数"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "二",
            "type": "填空题",
            "score": 3,
            "id": 6,
            "content": "设函数f(x) = x^2 + 2x + 1，则f(-1) = ________。",
            "options": null,
            "correct_answer": "0",
            "explanation": "直接代入x = -1计算，f(-1) = (-1)^2 + 2*(-1) + 1 = 0。",
            "knowledge_points": [
                "函数求值"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "二",
            "type": "填空题",
            "score": 3,
            "id": 7,
            "content": "已知函数f(x) = log₂(x)，则f(8) = ________。",
            "options": null,
            "correct_answer": "3",
            "explanation": "根据对数定义，log₂(8) = 3，因为2^3 = 8。",
            "knowledge_points": [],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "二",
            "type": "填空题",
            "score": 3,
            "id": 8,
            "content": "函数f(x) = sin(x)的周期为________。",
            "options": null,
            "correct_answer": "2π",
            "explanation": "正弦函数的周期为2π。",
            "knowledge_points": [],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 9,
            "content": "函数f(x) = x^2在其定义域内是单调递增的。",
            "options": [
                {
                    "key": "A",
                    "value": "√"
                },
                {
                    "key": "B",
                    "value": "×"
                }
            ],
            "correct_answer": "B",
            "explanation": "二次函数f(x) = x^2在x < 0时是单调递减的，在x > 0时是单调递增的。",
            "knowledge_points": [
                "二次函数"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 10,
            "content": "函数f(x) = e^x在其定义域内是严格递增的。",
            "options": [
                {
                    "key": "A",
                    "value": "√"
                },
                {
                    "key": "B",
                    "value": "×"
                }
            ],
            "correct_answer": "A",
            "explanation": "指数函数e^x在其定义域内始终是严格递增的。",
            "knowledge_points": [],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 11,
            "content": "所有奇函数的图像关于y轴对称。",
            "options": [
                {
                    "key": "A",
                    "value": "√"
                },
                {
                    "key": "B",
                    "value": "×"
                }
            ],
            "correct_answer": "B",
            "explanation": "奇函数的图像是关于原点对称的，而不是y轴。",
            "knowledge_points": [
                "奇偶函数",
                "对称性"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 12,
            "content": "函数f(x) = ln(x)在其定义域内是严格递增的。",
            "options": [
                {
                    "key": "A",
                    "value": "√"
                },
                {
                    "key": "B",
                    "value": "×"
                }
            ],
            "correct_answer": "A",
            "explanation": "对数函数ln(x)在其定义域内始终是严格递增的。",
            "knowledge_points": [
                "对数函数"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "四",
            "type": "简答题",
            "score": 5,
            "id": 13,
            "content": "解释为什么函数f(x) = e^x在其定义域内是严格递增的。",
            "options": null,
            "correct_answer": "因为e^x的导数为e^x，而e^x总是大于0，所以e^x在其定义域内始终是严格递增的。",
            "explanation": "指数函数e^x的导数为e^x，且e^x > 0对于所有x成立，因此e^x在其定义域内是严格递增的。",
            "knowledge_points": [
                "单调性"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "四",
            "type": "简答题",
            "score": 5,
            "id": 14,
            "content": "描述如何确定一个函数是否为奇函数。",
            "options": null,
            "correct_answer": "如果对于所有的x，f(-x) = -f(x)，则该函数为奇函数。",
            "explanation": "根据奇函数的定义，若对于所有x，f(-x) = -f(x)，则该函数为奇函数。",
            "knowledge_points": [
                "奇函数",
                "函数性质"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "五",
            "type": "应用计算题",
            "score": 10,
            "id": 15,
            "content": "给定函数f(x) = x^3 - 3x^2 + 2x，求其在区间[-1, 2]上的最大值和最小值。",
            "options": null,
            "correct_answer": "最大值为f(2) = 2，最小值为f(1) = 0。",
            "explanation": "首先求导f'(x) = 3x^2 - 6x + 2，令f'(x) = 0解得驻点x = 1 ± √(2/3)。然后计算端点值f(-1) = -6，f(2) = 2，以及驻点值f(1 - √(2/3)) ≈ 0.385，f(1 + √(2/3)) ≈ 0.385。比较这些值，最大值为f(2) = 2，最小值为f(1) = 0。",
            "knowledge_points": [
                "多项式函数"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "五",
            "type": "应用计算题",
            "score": 10,
            "id": 16,
            "content": "设函数f(x) = e^x + sin(x)，求其在区间[0, π]上的最大值和最小值。",
            "options": null,
            "correct_answer": "最大值为f(π) ≈ 23.14，最小值为f(0) = 1。",
            "explanation": "首先求导f'(x) = e^x + cos(x)，令f'(x) = 0解得驻点。然后计算端点值f(0) = 1，f(π) ≈ 23.14，以及驻点值（如果有）。比较这些值，最大值为f(π) ≈ 23.14，最小值为f(0) = 1。",
            "knowledge_points": [
                "导数",
                "指数函数",
                "三角函数",
                "极值"
            ],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        }
    ],
    "test_info": {
        "total_score": 53,
        "time_limit": 45
    }
}
```


- 批改学生提交的作答结果：

请求格式示例(将学生的作答数据发送至后端)：
```bash
POST http://0.0.0.0:8000/grade-student-answers
{
    "exam_id": 2,
    "student_id": "1",
    "answers": [
        {
            "exam_question_id": 1,
            "question_type": "single_choice",
            "answer_data": {
                "selected_option": "D"
            }
        },
        {
            "exam_question_id": 2,
            "question_type": "single_choice",
            "answer_data": {
                "selected_option": "A"
            }
        },
        {
            "exam_question_id": 3,
            "question_type": "single_choice",
            "answer_data": {
                "selected_option": "A"
            }
        },
        {
            "exam_question_id": 4,
            "question_type": "single_choice",
            "answer_data": {
                "selected_option": "B"
            }
        },
        {
            "exam_question_id": 5,
            "question_type": "single_choice",
            "answer_data": {
                "selected_option": "B"
            }
        },
        {
            "exam_question_id": 6,
            "question_type": "fill_blank",
            "answer_data": {
                "filled_answers": ["ln(x / (1-x))"]
            }
        },
        {
            "exam_question_id": 7,
            "question_type": "fill_blank",
            "answer_data": {
                "filled_answers": ["√2"]
            }
        },
        {
            "exam_question_id": 8,
            "question_type": "fill_blank",
            "answer_data": {
                "filled_answers": ["(2, 3)"]
            }
        },
        {
            "exam_question_id": 9,
            "question_type": "judgment",
            "answer_data": {
                "selected_option": "A"
            }
        },
        {
            "exam_question_id": 10,
            "question_type": "judgment",
            "answer_data": {
                "selected_option": "B"
            }
        },
        {
            "exam_question_id": 11,
            "question_type": "judgment",
            "answer_data": {
                "selected_option": "A"
            }
        },
        {
            "exam_question_id": 12,
            "question_type": "judgment",
            "answer_data": {
                "selected_option": "B"
            }
        },
        {
            "exam_question_id": 13,
            "question_type": "short_answer",
            "answer_data": {
                "content": "设f(x)是偶函数，则f(-x) = f(x)。对等式两边求导数，得到：f'(-x)·(-1) = f'(x)，即f'(-x) = -f'(x)。这表明f'(x)是奇函数，因为奇函数的定义就是g(-x) = -g(x)。因此，偶函数的导数是奇函数。"
            }
        },
        {
            "exam_question_id": 14,
            "question_type": "short_answer",
            "answer_data": {
                "content": "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。"
            }
        },
        {
            "exam_question_id": 15,
            "question_type": "application",
            "answer_data": {
                "content": "求导得f'(x) = 3x^2 - 12x + 9，令f'(x) = 0，得3(x^2 - 4x + 3) = 0，解得x = 1或x = 3。计算二阶导数f''(x) = 6x - 12，当x = 1时，f''(1) = -6 < 0，所以x = 1是极大值点；当x = 3时，f''(3) = 6 > 0，所以x = 3是极小值点。由于题目要求f(x)在x = 1处取得极小值，所以C的值应使得f''(1) > 0。但是f''(x) = 6x - 12只与x有关，与C无关。如果假设x = 1是极小值点，则C = -4，此时f(1) = 0，f(3) = 4。"
            }
        },
        {
            "exam_question_id": 16,
            "question_type": "application",
            "answer_data": {
                "content": "求导得f'(x) = e^x - 2x。对于任意x > 0，我们有e^x > 1 + x（泰勒展开的性质）。当x > 0时，1 + x > 2x仅在0 < x < 1时成立。但即使在0 < x < 1区间，我们仍有e^x > 1 + x > 2x，所以f'(x) = e^x - 2x > 0。当x ≥ 1时，e^x增长速度远大于2x，所以f'(x) > 0仍然成立。因此，在整个区间(0, +∞)上，f'(x) > 0，函数f(x)单调递增。函数的最小值出现在区间的左端点x = 0处，f(0) = e^0 - 0^2 = 1。"
            }
        }
    ]
}
```
响应格式示例(将批改后的结果发送至前端，供其呈现)：
```bash
{
    "record_id": 21,
    "student_id": "1",
    "exam_id": 2,
    "status": "pending_manual",
    "score_summary": {
        "objective_score": 11.0,
        "objective_total": 14.0,
        "subjective_score": 36.5,
        "subjective_total": 39.0,
        "total_score": 47.5,
        "total_possible": 53.0
    },
    "question_details": [
        {
            "exam_question_id": 17,
            "question_type": "single_choice",
            "content": "设函数f(x) = x^3 - 3x + 1，则f(x)在区间[-2, 2]上的最大值为：",
            "assigned_score": 2.0,
            "student_answer": "D",
            "correct_answer": "B",
            "explanation": "求导f'(x) = 3x^2 - 3，令f'(x) = 0得驻点x = ±1。计算端点和驻点处的函数值，f(-2) = -1, f(2) = 3, f(1) = -1, f(-1) = 3，因此最大值为f(2)=5。",
            "final_score": 0.0,
            "status": "graded"
        },
        {
            "exam_question_id": 18,
            "question_type": "single_choice",
            "content": "已知f(x)是一个偶函数，且满足f(x+2) = f(x)，则下列选项正确的是：",
            "assigned_score": 2.0,
            "student_answer": "A",
            "correct_answer": "A",
            "explanation": "由f(x+2) = f(x)可知f(x)是以2为周期的周期函数，同时f(x)是偶函数，进一步说明其具有对称性。",
            "final_score": 2.0,
            "status": "graded"
        },
        {
            "exam_question_id": 19,
            "question_type": "single_choice",
            "content": "若函数f(x) = ax^2 + bx + c (a≠0)的图像关于直线x=1对称，则b的值为：",
            "assigned_score": 2.0,
            "student_answer": "A",
            "correct_answer": "A",
            "explanation": "二次函数的对称轴为x = -b/(2a)，由题目条件x=1可得-b/(2a) = 1，解得b = -2a。",
            "final_score": 2.0,
            "status": "graded"
        },
        {
            "exam_question_id": 20,
            "question_type": "single_choice",
            "content": "设f(x) = |x| + |x-1|，则f(x)的最小值为：",
            "assigned_score": 2.0,
            "student_answer": "B",
            "correct_answer": "B",
            "explanation": "分段讨论f(x)，当x≤0时f(x) = -2x+1，当0<x<1时f(x) = 1，当x≥1时f(x) = 2x-1，最小值出现在x=0或x=1，f(x) = 1。",
            "final_score": 2.0,
            "status": "graded"
        },
        {
            "exam_question_id": 21,
            "question_type": "single_choice",
            "content": "设f(x)是定义在R上的奇函数，且f(x+2) = -f(x)，则f(x)的周期为：",
            "assigned_score": 2.0,
            "student_answer": "B",
            "correct_answer": "B",
            "explanation": "由f(x+2) = -f(x)，再代入f(x+4) = -f(x+2) = f(x)，可得f(x)的周期为4。",
            "final_score": 2.0,
            "status": "graded"
        },
        {
            "exam_question_id": 22,
            "question_type": "fill_blank",
            "content": "设函数f(x) = e^x / (e^x + 1)，则f(x)的反函数f^-1(x)为__________。",
            "assigned_score": 3.0,
            "student_answer": "ln(x/(1-x))",
            "correct_answer": "ln(x / (1-x))",
            "explanation": "令y = f(x)，即y = e^x / (e^x + 1)，解出x = ln(y / (1-y))，故f^-1(x) = ln(x / (1-x))。",
            "final_score": 3.0,
            "status": "graded"
        },
        {
            "exam_question_id": 23,
            "question_type": "fill_blank",
            "content": "已知f(x) = sin(x) + cos(x)，则f(x)的最大值为__________。",
            "assigned_score": 3.0,
            "student_answer": "√2",
            "correct_answer": "√2",
            "explanation": "利用辅助角公式，f(x) = √2sin(x + π/4)，最大值为√2。",
            "final_score": 3.0,
            "status": "graded"
        },
        {
            "exam_question_id": 24,
            "question_type": "fill_blank",
            "content": "设f(x) = x^3 - 6x^2 + 9x + 1，则f(x)的拐点坐标为__________。",
            "assigned_score": 3.0,
            "student_answer": "(2,3)",
            "correct_answer": "(2, 3)",
            "explanation": "求二阶导数f''(x) = 6x - 12，令f''(x) = 0得x = 2，代入f(x)得拐点为(2, 3)。",
            "final_score": 3.0,
            "status": "graded"
        },
        {
            "exam_question_id": 25,
            "question_type": "judgment",
            "content": "若f(x)是定义在R上的偶函数，则f(x)的导数f'(x)也是偶函数。",
            "assigned_score": 1.0,
            "student_answer": "A",
            "correct_answer": "B",
            "explanation": "偶函数的导数是奇函数，而非偶函数。",
            "final_score": 0.0,
            "status": "graded"
        },
        {
            "exam_question_id": 26,
            "question_type": "judgment",
            "content": "若f(x)是定义在R上的单调递增函数，则f(x)必然是连续函数。",
            "assigned_score": 1.0,
            "student_answer": "B",
            "correct_answer": "B",
            "explanation": "单调递增函数未必连续，例如分段函数可能不连续。",
            "final_score": 1.0,
            "status": "graded"
        },
        {
            "exam_question_id": 27,
            "question_type": "judgment",
            "content": "若f(x)是周期函数，则f(x)的导数f'(x)也是周期函数。",
            "assigned_score": 1.0,
            "student_answer": "A",
            "correct_answer": "A",
            "explanation": "周期函数的导数仍是周期函数，且周期相同。",
            "final_score": 1.0,
            "status": "graded"
        },
        {
            "exam_question_id": 28,
            "question_type": "judgment",
            "content": "若f(x)是定义在R上的奇函数，则f(x)的积分F(x)也是奇函数。",
            "assigned_score": 1.0,
            "student_answer": "B",
            "correct_answer": "B",
            "explanation": "奇函数的积分是偶函数，而非奇函数。",
            "final_score": 1.0,
            "status": "graded"
        },
        {
            "exam_question_id": 29,
            "question_type": "short_answer",
            "content": "证明：若f(x)是定义在R上的偶函数，则f'(x)是奇函数。",
            "assigned_score": 5.0,
            "student_answer": "设f(x)是偶函数，则f(-x) = f(x)。对等式两边求导数，得到：f'(-x)·(-1) = f'(x)，即f'(-x) = -f'(x)。这表明f'(x)是奇函数，因为奇函数的定义就是g(-x) = -g(x)。因此，偶函数的导数是奇函数。",
            "correct_answer": "设f(x)是偶函数，则f(-x) = f(x)。两边求导得-f'(-x) = f'(x)，即f'(-x) = -f'(x)，故f'(x)是奇函数。",
            "explanation": "设f(x)是偶函数，则f(-x) = f(x)。两边求导得-f'(-x) = f'(x)，即f'(-x) = -f'(x)，故f'(x)是奇函数。",
            "final_score": 5.0,
            "status": "graded"
        },
        {
            "exam_question_id": 30,
            "question_type": "short_answer",
            "content": "已知f(x) = x^3 - 3x^2 + 2x，求f(x)的所有零点及其对应的重数。",
            "assigned_score": 5.0,
            "student_answer": "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。",
            "correct_answer": "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。",
            "explanation": "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。",
            "final_score": 5.0,
            "status": "graded"
        },
        {
            "exam_question_id": 31,
            "question_type": "application",
            "content": "已知函数f(x) = x^3 - 6x^2 + 9x + C，其中C为常数，若f(x)在x=1处取得极小值，求C的值以及f(x)的极值点和极值。",
            "assigned_score": 10.0,
            "student_answer": "求导得f'(x) = 3x^2 - 12x + 9，令f'(x) = 0，得3(x^2 - 4x + 3) = 0，解得x = 1或x = 3。计算二阶导数f''(x) = 6x - 12，当x = 1时，f''(1) = -6 < 0，所以x = 1是极大值点；当x = 3时，f''(3) = 6 > 0，所以x = 3是极小值点。由于题目要求f(x)在x = 1处取得极小值，所以C的值应使得f''(1) > 0。但是f''(x) = 6x - 12只与x有关，与C无关。如果假设x = 1是极小值点，则C = -4，此时f(1) = 0，f(3) = 4。",
            "correct_answer": "求导f'(x) = 3x^2 - 12x + 9，令f'(x) = 0得x = 1或x = 3。由f''(x) = 6x - 12可知x=1为极小值点，代入f(1) = C+4，由于f(1)为极小值，故C=-4，极值点为x=1，极小值为0；极值点为x=3，极大值为4。",
            "explanation": "求导f'(x) = 3x^2 - 12x + 9，令f'(x) = 0得x = 1或x = 3。由f''(x) = 6x - 12可知x=1为极小值点，代入f(1) = C+4，由于f(1)为极小值，故C=-4，极值点为x=1，极小值为0；极值点为x=3，极大值为4。",
            "final_score": 7.5,
            "status": "graded"
        },
        {
            "exam_question_id": 32,
            "question_type": "application",
            "content": "已知f(x) = e^x - x^2，求证f(x)在区间(0, +∞)上单调递增，并求f(x)的最小值。",
            "assigned_score": 10.0,
            "student_answer": "求导得f'(x) = e^x - 2x。对于任意x > 0，我们有e^x > 1 + x（泰勒展开的性质）。当x > 0时，1 + x > 2x仅在0 < x < 1时成立。但即使在0 < x < 1区间，我们仍有e^x > 1 + x > 2x，所以f'(x) = e^x - 2x > 0。当x ≥ 1时，e^x增长速度远大于2x，所以f'(x) > 0仍然成立。因此，在整个区间(0, +∞)上，f'(x) > 0，函数f(x)单调递增。函数的最小值出现在区间的左端点x = 0处，f(0) = e^0 - 0^2 = 1。",
            "correct_answer": "求导f'(x) = e^x - 2x，在(0, +∞)上，e^x增长速度大于2x，故f'(x) > 0，f(x)单调递增。f(x)的最小值出现在x=0，f(0) = 1。",
            "explanation": "求导f'(x) = e^x - 2x，在(0, +∞)上，e^x增长速度大于2x，故f'(x) > 0，f(x)单调递增。f(x)的最小值出现在x=0，f(0) = 1。",
            "final_score": 10.0,
            "status": "graded"
        }
    ]
}
```

## 注意事项

1. API密钥安全
   - 不要将API密钥提交到代码仓库
   - 建议使用环境变量管理密钥
   - 定期更换密钥

2. 数据库维护
   - 定期备份数据库
   - 及时清理无用数据
   - 优化数据库性能

3. 系统限制
   - 注意API调用频率限制
   - 图片爬取需遵守网站规则
   - 生成内容需人工审核

## 常见问题

1. 数据库连接失败
   - 检查数据库配置是否正确
   - 确保MySQL服务已启动
   - 验证用户权限

2. API调用失败
   - 检查API密钥是否有效
   - 确认网络连接正常
   - 查看错误日志

3. PDF生成失败
   - 检查字体文件是否存在
   - 确保输出目录可写
   - 验证内容格式

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。
