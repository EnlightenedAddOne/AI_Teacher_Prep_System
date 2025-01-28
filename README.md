# AI-ZGLOSH

AI-ZGLOSH是一个基于大语言模型的智能教学助手,旨在帮助教师提高教学效率和质量。

## 功能特性

- 教学设计生成 - 自动生成教案和教学设计方案
- 习题生成与解析 - 根据知识点生成练习题并提供答案解析
- 多模型支持 - 支持多个大语言模型,可灵活切换
- PDF文档生成 - 将生成的内容导出为PDF格式

## 项目结构  
python
AI_zglosh/
├── config/ # 配置文件目录
│ └── config.ini # 系统配置文件
├── src/ # 源代码目录
│ ├── llm_integration.py # 大语言模型集成
│ ├── exercise_generation.py # 习题生成
│ ├── teaching_design.py # 教学设计生成
│ ├── multimedia_generation.py # 多媒体生成
│ ├── student_analysis.py # 学生分析
│ └── utils/ # 工具函数
│ ├── helpers.py # 辅助函数
│ └── prompts.py # 提示词模板
└── output/ # 输出文件目录
└── PDF/ # 生成的PDF文件
└── exercises/ # 生成的习题文件

## 支持的模型

### 通义千问
- 基于LangChain集成
- 适用于教学设计和习题生成
- 无需指定模型版本,自动使用最新版本

### 智谱清言
- 支持多个模型版本:
  - chatglm_turbo
  - chatglm_pro
  - chatglm_std
  - chatglm_lite
- 可配置参数:
  - temperature: 0.7
  - top_p: 0.7
  - max_tokens: 2048

## 使用方法

1. 安装依赖库
```bash
pip install -r requirements.txt
```

2. 配置API密钥:
在`config/config.ini`中配置:

```ini
[API_KEYS]
tongyi = your_tongyi_api_key
zhipu = your_zhipu_api_key
```


3. 代码示例:

```python
# 初始化模型
from src.llm_integration import LLMFactory

# 使用通义千问
tongyi_llm = LLMFactory.initialize_tongyi(api_key="your_tongyi_api_key")

# 或使用智谱清言
zhipu_llm = LLMFactory.initialize_zhipu(
    api_key="your_zhipu_api_key",
    model_name="chatglm_turbo"
)

# 生成教学设计
from src.teaching_design import generate_teaching_design

design = generate_teaching_design(
    subject="数学",
    topic="勾股定理",
    goals="理解勾股定理的概念和应用",
    duration="45分钟",
    grade="初中二年级",
    api_key=api_key
)

# 生成习题和答案解析
from src.exercise_generation import generate_exercises

exercises, answers = generate_exercises(
    subject="数学",
    topic="勾股定理", 
    degree="中等",
    exercise_config={
        "type": "选择题",
        "count": 5
    },
    api_key=api_key
)
```

## 注意事项

1. API密钥安全
   - 请妥善保管API密钥
   - 不要将密钥提交到代码仓库
   - 建议使用环境变量或配置文件管理密钥

2. 模型使用
   - 不同模型可能产生不同风格的输出
   - 建议根据具体需求选择合适的模型
   - 注意API调用频率限制

3. 内容审核
   - 生成的内容仅供参考
   - 建议教师进行审核和调整
   - 特别注意习题答案的准确性

## 开发计划

- [ ] 添加更多模型支持
- [ ] 优化提示词模板
- [ ] 增加Web界面
- [ ] 添加批量生成功能
- [ ] 支持更多文档格式导出

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用MIT许可证。请查看LICENSE文件了解更多信息。
