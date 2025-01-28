from llm_integration import LLMFactory
from utils.prompts import online_test_prompt, generate_test_requirements


def generate_online_test(test_config: dict, api_key: str) -> str:
    """
    生成在线测试题目
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
    :param api_key: API密钥
    :return: JSON格式的测试题目
    """
    llm = LLMFactory.initialize_tongyi(api_key)
    
    # 生成模板所需的输入数据
    input_data = generate_test_requirements(test_config)
    
    # 生成提示词
    prompt = online_test_prompt.format(**input_data)
    
    # 调用大模型生成题目
    return llm.invoke(prompt) 