import json
from typing import Dict, Any, Tuple, Optional

from llm_integration import LLMFactory
from utils import online_test_prompt
from education_sql import import_exam_paper
from education_sql import Session


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
    section_index = 0

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
                'question_type': name,  # 使用中文题型名称
                'question_score': q_config['score']
            })
            total_score += total
            section_index += 1

    input_data.update({
        'test_requirements': '\n'.join(requirements),
        'total_score': total_score
    })

    return input_data


def generate_online_test(test_config: Dict, api_key: str, save_to_db: bool = True) -> Tuple[Dict, Optional[int]]:
    """生成在线测试题目"""
    try:
     
        # 生成题目要求和输入数据
        input_data = generate_test_requirements(test_config)
        
        # 使用LLM生成试卷内容
        llm = LLMFactory.initialize_tongyi(api_key)
        prompt = online_test_prompt.format(**input_data)
        
        # 解析生成的内容
        try:
            response = llm.invoke(prompt)
            if not response:
                raise ValueError("API 返回为空")
                
            clean_data = response.lstrip("```json").rstrip("```").strip() if isinstance(response, str) else response
            test_data = json.loads(clean_data)
            
        except Exception as e:
            raise ValueError(f"生成试卷失败: {str(e)}")
        
        # 验证数据格式
        if not isinstance(test_data, dict) or "questions" not in test_data:
            raise ValueError("API返回的数据格式错误")
            
        if not test_data["questions"]:
            raise ValueError("API返回的数据格式错误: questions 列表为空")
        
        # 标准化应用计算题
        for question in test_data["questions"]:
            if "应用" in question["type"] and "计算" in question["type"]:
                question["type"] = "应用计算题"
        
        # 保存到数据库
        if save_to_db:
            # 创建数据库会话
            session = Session()
            try:            
                exam_id = save_test_to_database(
                    test_data, 
                    f"{test_config['subject']}_{test_config['topic']}_测试",
                    session
                )

                return test_data, exam_id
            finally:
                session.close()
        return test_data, None
        
    except Exception as e:
        raise ValueError(f"生成试卷失败: {str(e)}")


def save_test_to_database(test_data: Dict, exam_name: str, session) -> Optional[int]:
    """保存试卷到数据库"""
    try:
        exam_id = import_exam_paper(session, test_data, exam_name)
        return exam_id
    except Exception as e:
        raise ValueError(f"保存试卷失败: {str(e)}")
