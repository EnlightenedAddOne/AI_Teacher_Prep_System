# 测试文件

from teaching_design import generate_teaching_design
from exercise_generation import generate_exercises
from student_analysis import analyze_student_performance
from configs import config  # 修改导入路径
from Online_Test import generate_online_test
from education_sql import Session, verify_exam_import, export_exam_to_json  # 从正确的模块导入
import json


def test_online_test():
    """测试在线测试题目生成和数据库保存"""
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

    api_key = config['api_keys'].get('tongyi_api_key')
    if not api_key:
        print("错误: 未找到通义千问API密钥")
        return None

    try:
        # 生成试卷并保存到数据库
        test_data, exam_id = generate_online_test(test_config, api_key, save_to_db=True)

        if exam_id:
            print(f"\n试卷已保存到数据库，ID: {exam_id}")
            session = Session()
            try:
                # 验证导入结果
                verify_exam_import(session, exam_id)

                # 从数据库导出试卷
                print("\n=== 从数据库导出的试卷数据 ===")
                exported_data = export_exam_to_json(session, exam_id)
                if exported_data:
                    print(json.dumps(exported_data, indent=2, ensure_ascii=False))
                else:
                    print("试卷导出失败")
            finally:
                session.close()
        else:
            print("\n试卷保存失败")

        return test_data

    except Exception as e:
        print(f"\n生成在线测试题目时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


"""
# 测试教学设计生成
def test_teaching_design():
    api_key = config['api_keys'].get('tongyi_api_key')

    teaching_design = generate_teaching_design(
        subject="数学",
        topic="函数",
        goals="理解函数的概念和基本性质",
        duration="45分钟",
        grade="初中二年级",
        api_key=api_key
    )
    print("\n=== 教学设计 ===")
    print(teaching_design)
"""

"""
# 测试练习题生成
def test_generate_exercises():
    api_key = config['api_keys'].get('tongyi_api_key')
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
    print("\n=== 练习题 ===")
    print(exercises)

    print("\n=== 答案和解析 ===")
    print(answers)
"""


if __name__ == "__main__":
    test_online_test()

@app.get("/api/status")
async def api_status():
    return {
        "requests": {
            "total": recommender.metrics["total_requests"],
            "success_rate": recommender.metrics["success_requests"] / recommender.metrics["total_requests"] if recommender.metrics["total_requests"] > 0 else 0,
            "cache_hit_rate": recommender.metrics["cache_hits"] / recommender.metrics["total_requests"] if recommender.metrics["total_requests"] > 0 else 0
        },
        "rate_limit": recommender.rate_limit,
        "last_request": recommender.last_request_time
    }
