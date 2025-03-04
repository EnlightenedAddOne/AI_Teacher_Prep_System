# 生成在线测试的试卷数据
import json
import re
from typing import Dict, Any, Tuple, Optional

from src.llm_integration import LLMFactory
from src.utils import online_test_prompt
from src.education_sql import import_exam_paper
from src.education_sql import Session


# 处理JSON字符串中的转义字符问题
def fix_escape_chars(json_str):
    """修复JSON字符串中的转义字符问题"""
    # 1. 处理转义字符
    fixed_str = json_str.replace('\\', '\\\\')  # 双重转义反斜杠
    
    # 2. 处理换行和制表符
    fixed_str = fixed_str.replace('\t', '\\t')
    fixed_str = fixed_str.replace('\n', '\\n')
    
    # 3. 处理数学表达式中的^符号
    fixed_str = re.sub(r'(\w+)\^(\d+)', r'\1**\2', fixed_str)
    
    # 4. 确保属性名使用双引号
    fixed_str = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', fixed_str)
    
    # 5. 移除尾部逗号
    fixed_str = re.sub(r',\s*}', '}', fixed_str)
    fixed_str = re.sub(r',\s*]', ']', fixed_str)
    
    return fixed_str


# 替换JSON中的占位符
def replace_placeholders(obj, expressions):
    """递归替换JSON对象中的数学表达式占位符"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                replace_placeholders(value, expressions)
            elif isinstance(value, str) and value.startswith("MATH_EXPR_"):
                try:
                    index = int(value.split("_")[-1])
                    if 0 <= index < len(expressions):
                        obj[key] = expressions[index]
                except (ValueError, IndexError):
                    pass
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                replace_placeholders(item, expressions)
            elif isinstance(item, str) and item.startswith("MATH_EXPR_"):
                try:
                    index = int(item.split("_")[-1])
                    if 0 <= index < len(expressions):
                        obj[i] = expressions[index]
                except (ValueError, IndexError):
                    pass


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
    content = None
    try:
        # 生成题目要求和输入数据
        input_data = generate_test_requirements(test_config)
        
        # 初始化通义千问模型
        LLMFactory.initialize_tongyi(api_key)

        # 构建消息
        messages = [{
            "role": "user",
            "content": online_test_prompt.format(**input_data)
        }]

        # 调用模型生成试卷内容
        response = LLMFactory.call_tongyi(messages, model_name="qwen-plus-2025-01-25")

        # 解析生成的内容
        try:
            if not response:
                raise ValueError("API 返回为空")

            content = response.get('content', '')
            if not content:
                raise ValueError("API 返回内容为空")

            # 提取JSON部分 - 简化处理，专注于常见的格式
            if "```json" in content and "```" in content:
                # 最常见的情况：开头有```json，结尾有```
                clean_data = content.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in content:
                # 备选情况：只有```包裹
                parts = content.split("```")
                if len(parts) >= 3:  # 确保有开始和结束的```
                    clean_data = parts[1].strip()
                    if clean_data.startswith("json"):
                        clean_data = clean_data[4:].strip()
                else:
                    clean_data = content.strip()
            else:
                clean_data = content.strip()
            
            print(f"提取的JSON数据: {clean_data[:100]}...")  # 打印前100个字符用于调试
            
            # 初始化数学表达式列表
            math_expressions = []
            
            # 处理转义字符问题 - 更安全的方式
            try:
                # 尝试直接解析，如果成功就不需要额外处理
                test_data = json.loads(clean_data)

                # 将数学表达式占位符替换回原始表达式
                if math_expressions:
                    # 应用替换
                    replace_placeholders(test_data, math_expressions)
            except json.JSONDecodeError as e:
                print(f"初步JSON解析失败: {str(e)}，尝试修复...")
                
                # 处理常见的JSON格式问题
                # 使用修复函数处理转义字符
                clean_data = fix_escape_chars(clean_data)
                
                # 处理数学表达式中的其他特殊字符
                # 先将数学表达式中的特殊字符替换为临时标记
                # 例如：将 "f(x) = x^2" 中的 ^ 替换为安全的标记
                math_expressions = []
                
                def replace_math_expr(match):
                    expr = match.group(1)
                    # 保存原始表达式
                    math_expressions.append(expr)
                    # 返回一个安全的占位符
                    return f'"MATH_EXPR_{len(math_expressions)-1}"'
                
                # 查找并替换引号内的数学表达式
                clean_data = re.sub(r'"([^"]*?[+\-*/^=()][^"]*?)"', replace_math_expr, clean_data)
                
                # 4. 确保属性名使用双引号
                clean_data = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', clean_data)
                
                # 5. 移除尾部逗号
                clean_data = re.sub(r',\s*}', '}', clean_data)
                clean_data = re.sub(r',\s*]', ']', clean_data)
                
                print(f"修复后的JSON数据: {clean_data[:100]}...")  # 打印前100个字符用于调试
                
                try:
                    test_data = json.loads(clean_data)
                    
                    # 将数学表达式占位符替换回原始表达式
                    if math_expressions:
                        # 应用替换
                        replace_placeholders(test_data, math_expressions)
                except json.JSONDecodeError as e2:
                    print(f"修复后JSON解析仍然失败: {str(e2)}，尝试使用更宽松的解析方法...")
                    
                    # 尝试使用更宽松的解析方法
                    try:
                        # 尝试使用json5库（如果可用）
                        try:
                            import json5
                            test_data = json5.loads(clean_data)
                            print("使用json5成功解析")
                        except (ImportError, Exception):
                            # 尝试使用ast.literal_eval
                            import ast
                            
                            # 将JSON格式转换为Python字典格式
                            py_data = clean_data.replace('null', 'None')
                            py_data = py_data.replace('true', 'True')
                            py_data = py_data.replace('false', 'False')
                            
                            try:
                                test_data = ast.literal_eval(py_data)
                                print("使用ast.literal_eval成功解析")
                            except (SyntaxError, ValueError) as ast_err:
                                print(f"ast.literal_eval解析失败: {str(ast_err)}")
                                
                                # 最后的尝试：手动解析关键部分
                                print("尝试手动提取关键数据...")
                                
                                # 提取questions和test_info部分
                                questions_match = re.search(r'"questions"\s*:\s*\[(.*?)]', content, re.DOTALL)
                                test_info_match = re.search(r'"test_info"\s*:\s*\[(.*?)]', content, re.DOTALL)
                                
                                if questions_match and test_info_match:
                                    # 构建基本结构
                                    test_data = {
                                        "questions": [],
                                        "test_info": []
                                    }
                                    
                                    # 提取总分和时间限制
                                    time_limit_match = re.search(r'"time_limit"\s*:\s*(\d+)', test_info_match.group(1))
                                    total_score_match = re.search(r'"total_score"\s*:\s*(\d+)', test_info_match.group(1))
                                    
                                    if time_limit_match and total_score_match:
                                        test_data["test_info"].append({
                                            "time_limit": int(time_limit_match.group(1)),
                                            "total_score": int(total_score_match.group(1))
                                        })
                                    
                                    print("成功构建基本数据结构")
                                else:
                                    raise ValueError("无法提取关键数据结构")
                    except Exception as final_err:
                        print(f"所有解析方法都失败: {str(final_err)}")
                        print(f"原始内容: {content}")
                        raise ValueError(f"无法解析JSON数据: {str(final_err)}")
            
        except Exception as e:
            print(f"解析错误: {str(e)}")
            print(f"原始内容: {content}")
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
