from .Create import *


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
                "total_score": int(exam.total_score),
                "time_limit": exam.time_limit
            },
            "questions": []
        }

        # 处理所有题目，使用新的题号
        for index, eq in enumerate(exam_questions, start=1):
            question = eq.question

            # 转换题型到原始中文格式
            question_type = reverse_convert_type(question.question_type)

            # 获取正确答案
            if question.question_type in ['single_choice', 'multi_choice', 'judgment']:
                # 选择题和判断题从选项中获取正确答案
                correct_options = [opt.option_key for opt in question.options if opt.is_correct]
                correct_answer = correct_options[0] if correct_options else ""
            else:
                # 填空题和简答题从选项或元数据中获取答案
                answer_option = next((opt for opt in question.options if opt.option_key == "answer"), None)
                if answer_option:
                    correct_answer = answer_option.option_content
                else:
                    # 如果没有找到答案选项，从元数据中获取
                    correct_answer = question.meta_data.get("correct_answer", "")
                    if not correct_answer:
                        # 如果元数据中也没有，使用解析的第一句作为答案
                        correct_answer = question.explanation.split("。")[0]

            # 构建题目基础信息
            question_data = {
                "number": eq.display_number,
                "type": question_type,
                "score": int(eq.assigned_score),
                "id": index,
                "content": question.content,
                "explanation": question.explanation,
                "correct_answer": correct_answer,  # 添加正确答案
                "knowledge_points": [p.point_name for p in question.knowledge_points],
                "subject": question.subject.subject_name,
                "topic": question.topic,
                "degree": reverse_convert_difficulty(question.difficulty)
            }

            # 处理选项
            if question.question_type in ['single_choice', 'multi_choice', 'judgment']:
                options = []
                for opt in sorted(question.options, key=lambda x: x.sort_order):
                    if opt.option_key != "answer":  # 跳过答案选项
                        option_item = {
                            "key": opt.option_key,
                            "value": opt.option_content
                        }
                        options.append(option_item)
                question_data["options"] = options

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
        'short_answer': '简答题',
        'application': '应用计算题'
    }
    # 先标准化输入
    db_type = db_type.strip()  # 移除空白字符
    
    if db_type not in type_map:
        print(f"警告：未知的题型 {db_type}")
        # 如果输入已经是中文类型，检查是否是有效的源类型
        if db_type in [v for v in type_map.values()]:
            return db_type
    
    return type_map.get(db_type, db_type)


def reverse_convert_difficulty(difficulty_value):
    """将难度系数转换为中文描述"""
    if difficulty_value >= 0.7:
        return "困难"
    elif difficulty_value >= 0.4:
        return "中等"
    else:
        return "简单"


def verify_question_types(session):
    """验证数据库中的题型"""
    questions = session.query(Question).all()
    for q in questions:
        print(f"题目ID: {q.question_id}, "
              f"存储类型: {q.question_type}, "
              f"原始类型: {q.original_type}")
