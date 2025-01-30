from llm_integration import LLMFactory
from utils import online_test_prompt
from typing import Dict, Any


# 生成题型要求文本和相关输入数据
def generate_test_requirements(test_config: Dict) -> Dict[str, Any]:
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


def generate_online_test(test_config: dict, api_key: str) -> str:
    """生成在线测试题目"""
    if not api_key:
        raise ValueError("API密钥不能为空")

    llm = LLMFactory.initialize_tongyi(api_key)  # 启用JSON Mode
    input_data = generate_test_requirements(test_config)
    prompt = online_test_prompt.format(**input_data)

    try:
        response = llm.invoke(prompt)
        clean_data = response.lstrip("```json").rstrip("```").strip()
        return clean_data
    except Exception as e:
        print(f"API调用错误: {str(e)}")
        raise
