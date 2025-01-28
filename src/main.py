# 测试文件
from teaching_design import generate_teaching_design
from exercise_generation import generate_exercises
from student_analysis import analyze_student_performance
from config import config
from Online_Test import generate_online_test


def test_online_test():
    """测试在线测试题目生成"""
    test_config = {
        'subject': '数学',
        'topic': '函数',
        'degree': '困难',
        'time_limit': 45,
        'questions': {
            'choice': {'count': 5, 'score': 2},  # 选择题：5题，每题2分
            'fill': {'count': 3, 'score': 3},  # 填空题：3题，每题3分
            'judge': {'count': 4, 'score': 1},  # 判断题：4题，每题1分
            'short_answer': {'count': 2, 'score': 5},  # 简答题：2题，每题5分
            'application': {'count': 2, 'score': 10}  # 应用题：2题，每题10分
        }
    }

    api_key = config['api_keys']['tongyi_api_key']

    try:
        test_questions = generate_online_test(test_config, api_key)
        return test_questions
    except Exception as e:
        print(f"生成在线测试题目时出错: {str(e)}")
        return None


def main():
    """
    api_key = config['api_keys']['tongyi_api_key']
    
    # 测试教学设计生成
    teaching_design = generate_teaching_design(
        subject="数学",
        topic="函数",
        goals="理解函数的概念和基本性质",
        duration="45分钟",
        grade="初中二年级",
        api_key=api_key
    )
    
    # 测试练习题生成
    exercise_config = {
        'choice_count': 5,
        'choice_score': 2,
        'fill_count': 3,
        'fill_score': 3,
        'judge_count': 4,
        'judge_score': 1
    }
    
    exercises, answers = generate_exercises(
        subject="数学",
        topic="函数",
        degree="medium",
        exercise_config=exercise_config,
        api_key=api_key
    )
    """
    # 测试在线测试题目生成
    test_questions = test_online_test()

    # 输出结果
    """
    print("\n=== 教学设计 ===")
    print(teaching_design)
    
    print("\n=== 练习题 ===")
    print(exercises)
    
    print("\n=== 答案和解析 ===")
    print(answers)
    """

    print("\n=== 在线测试题目 ===")
    print(test_questions)


if __name__ == "__main__":
    main()
