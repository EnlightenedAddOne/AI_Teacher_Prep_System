from Create import *


def export_exam_to_json(session, exam_id):
    """将数据库中的试卷导出为原始JSON格式"""
    try:
        # 获取试卷基本信息
        exam = session.query(Exam).get(exam_id)
        if not exam:
            print("试卷不存在")
            return None

        # 获取关联的题目及试卷配置
        exam_questions = session.query(ExamQuestion).filter_by(exam_id=exam_id) \
            .order_by(ExamQuestion.sort_order).all()

        result = {
            "test_info": {
                "total_score": float(exam.total_score),
                "time_limit": exam.time_limit
            },
            "questions": []
        }

        # 处理所有题目
        for eq in exam_questions:
            question = eq.question
            subject = question.subject

            # 转换题型到原始中文格式
            question_type = reverse_convert_type(question.question_type)

            # 构建题目基础信息
            question_data = {
                "number": eq.display_number,
                "type": question_type,
                "score": float(eq.assigned_score),
                "id": eq.eq_id,  # 使用试卷题目关系ID作为临时标识
                "content": question.content,
                "explanation": question.explanation,
                "knowledge_points": [p.point_name for p in question.knowledge_points],
                "subject": subject.subject_name,
                "topic": question.topic,
                "degree": reverse_convert_difficulty(question.difficulty)
            }

            # 处理选择题/判断题的选项
            if question.question_type in ['single_choice', 'multi_choice', 'judgment']:
                options = []
                correct_answer = None
                for opt in sorted(question.options, key=lambda x: x.sort_order):
                    option_item = {
                        "key": opt.option_key,
                        "value": opt.option_content
                    }
                    options.append(option_item)
                    if opt.is_correct:
                        correct_answer = opt.option_key

                question_data["options"] = options
                if correct_answer:
                    question_data["correct_answer"] = correct_answer

            # 处理填空题和简答题的答案
            else:
                # 需要根据业务逻辑获取正确答案，此处示例处理填空题
                if question.question_type == 'fill_blank':
                    # 假设正确答案存储在第一个选项的option_content中
                    if question.options:
                        question_data["correct_answer"] = question.options[0].option_content
                elif question.question_type == 'essay':
                    # 简答题答案可能存储在explanation或单独字段
                    question_data["correct_answer"] = question.explanation.split("。")[0]

            result["questions"].append(question_data)

        # 添加学科信息到根节点（根据原始数据格式）
        if exam_questions:
            result["subject"] = exam_questions[0].question.subject.subject_name

        return result

    except Exception as e:
        print(f"导出失败：{str(e)}")
        return None


def reverse_convert_type(db_type):
    """将数据库题型转换为原始中文类型"""
    type_map = {
        'single_choice': '选择题',
        'multi_choice': '多选题',
        'judgment': '判断题',
        'fill_blank': '填空题',
        'essay': '简答题'
    }
    return type_map.get(db_type, '简答题')


def reverse_convert_difficulty(difficulty_value):
    """将难度系数转换为中文描述"""
    if difficulty_value >= 0.7:
        return "困难"
    elif difficulty_value >= 0.4:
        return "中等"
    else:
        return "简单"

