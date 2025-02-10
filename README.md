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

2. API接口说明

- 生成教学设计：
```bash
POST /generate-teaching-design
{
    "subject": "数学",
    "topic": "函数",
    "goals": "理解函数的概念和基本性质",
    "duration": "45分钟",
    "grade": "初中二年级"
}
```

- 生成在线测试：
```bash
POST /generate-online-test
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

3. 使用示例代码

```python
from src.Online_Test import generate_online_test
from src.configs import config

# 配置测试参数
test_config = {
    'subject': '数学',
    'topic': '函数',
    'degree': '中等',
    'time_limit': 45,
    'questions': {
        'choice': {'count': 5, 'score': 2},
        'fill': {'count': 3, 'score': 3},
        'judge': {'count': 4, 'score': 1},
        'short_answer': {'count': 2, 'score': 5},
        'application': {'count': 2, 'score': 10}
    }
}

# 生成试卷
api_key = config['api_keys']['tongyi_api_key']
test_data, exam_id = generate_online_test(test_config, api_key, save_to_db=True)
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
