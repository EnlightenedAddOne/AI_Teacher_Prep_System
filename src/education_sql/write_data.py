from .Create import *


def import_exam_paper(session, json_data, exam_name: str):
    """完整试卷导入函数"""
    try:
        # 1. 处理学科信息
        subject_name = json_data["questions"][0]["subject"]
        subject = session.query(Subject).filter_by(subject_name=subject_name).first()
        if not subject:
            subject = Subject(subject_name=subject_name)
            session.add(subject)
            session.flush()

        # 2. 创建试卷记录
        test_info = json_data["test_info"]
        if isinstance(test_info, list):
            test_info = test_info[0]
            
        exam = Exam(
            exam_name=json_data.get("exam_name", f"{exam_name}"),
            subject_id=subject.subject_id,
            subject_name=subject_name,
            total_score=int(test_info["total_score"]),
            time_limit=int(test_info["time_limit"])
        )
        session.add(exam)
        session.flush()

        # 3. 处理所有题目
        for order, q in enumerate(json_data["questions"], start=1):
            # 3.1 转换题型
            original_type = q["type"]
            question_type = convert_question_type(original_type)
            
            # 3.2 创建题目主体
            new_question = Question(
                subject_id=subject.subject_id,
                question_type=question_type,
                original_type=original_type,
                content=q["content"],
                explanation=q.get("explanation", ""),
                difficulty=convert_difficulty(q["degree"]),
                topic=q["topic"],
                meta_data={
                    "source_exam_id": exam.exam_id,
                    "original_number": q["number"],
                    "correct_answer": q.get("correct_answer", "")
                }
            )
            session.add(new_question)
            session.flush()

            # 3.3 处理选项
            if "options" in q and q["options"]:
                # 处理选择题和判断题的选项
                for opt_order, opt in enumerate(q["options"]):
                    is_correct = (opt["key"] == q["correct_answer"])
                    option = QuestionOption(
                        question_id=new_question.question_id,
                        option_key=opt["key"],
                        option_content=opt["value"],
                        is_correct=is_correct,
                        sort_order=opt_order
                    )
                    session.add(option)
            
            # 对于填空题、简答题和应用计算题，创建答案选项
            if question_type in ['fill_blank', 'short_answer', 'application'] and "correct_answer" in q:
                option = QuestionOption(
                    question_id=new_question.question_id,
                    option_key="answer",
                    option_content=q["correct_answer"],
                    is_correct=True,
                    sort_order=0
                )
                session.add(option)

            # 3.4 处理知识点
            if "knowledge_points" in q:
                for point_name in q["knowledge_points"]:
                    # 先检查是否已存在相同的知识点
                    existing_point = session.query(KnowledgePoint).filter_by(
                        point_name=point_name,
                        subject_id=subject.subject_id
                    ).first()
                    
                    if existing_point:
                        # 如果存在，更新question_id
                        existing_point.question_id = new_question.question_id
                    else:
                        # 如果不存在，创建新的知识点
                        new_point = KnowledgePoint(
                            point_name=point_name,
                            subject_id=subject.subject_id,
                            question_id=new_question.question_id,
                            parent_point=0,
                            level=1
                        )
                        session.add(new_point)

            # 3.5 关联到试卷
            exam_question = ExamQuestion(
                exam_id=exam.exam_id,
                question_id=new_question.question_id,
                display_number=q["number"],
                assigned_score=int(q["score"]),
                sort_order=order
            )
            session.add(exam_question)

        session.commit()
        return exam.exam_id

    except Exception as e:
        session.rollback()
        print(f"导入失败：{str(e)}")
        return None


def convert_question_type(original_type: str) -> str:
    """将中文题型转换为数据库存储的类型"""
    type_map = {
        '选择题': 'single_choice',
        '多选题': 'multi_choice',
        '判断题': 'judgment',
        '填空题': 'fill_blank',
        '简答题': 'short_answer',
        '应用计算题': 'application'
    }
    
    original_type = original_type.strip()
    
    if original_type not in type_map:
        if original_type in type_map.values():
            return original_type
        if '应用' in original_type and '计算' in original_type:
            return 'application'
        if '简答' in original_type:
            return 'short_answer'
    
    return type_map.get(original_type, original_type)


def convert_difficulty(degree):
    """转换难度到数值"""
    difficulty_map = {
        "简单": 0.3,
        "中等": 0.6,
        "困难": 0.8
    }
    return difficulty_map.get(degree, 0.5)


def verify_exam_import(session, exam_id):
    """验证试卷导入结果,也可查看试卷简要信息"""
    exam = session.query(Exam).get(exam_id)
    if not exam:
        print("试卷不存在")
        return

    print(f"试卷验证报告：{exam.exam_name}")
    print(f"学科：{exam.subject_name}")
    print(f"应含题目数：{len(exam.exam_questions)}")

    # 检查题目关联
    question_count = session.query(ExamQuestion).filter_by(exam_id=exam_id).count()
    print(f"实际关联题目数：{question_count}")

    # 检查知识点覆盖率
    points = session.query(KnowledgePoint.point_name) \
        .join(Question, KnowledgePoint.question_id == Question.question_id) \
        .filter(Question.subject_id == exam.subject_id) \
        .distinct().all()
    print(f"涉及知识点：{[p[0] for p in points]}")

    # 检查选项完整性
    error_questions = []
    for eq in exam.exam_questions:
        q = eq.question
        if q.question_type in ['single_choice', 'judgment']:
            correct_options = [opt for opt in q.options if opt.is_correct]
            if len(correct_options) != 1:
                error_questions.append(q.question_id)

    if error_questions:
        print(f"以下题目选项异常：{error_questions}")
    else:
        print("所有选择题/判断题选项验证通过")

    # 检查分值总和
    total_score = sum([eq.assigned_score for eq in exam.exam_questions])
    print(f"试卷总分：{total_score}（配置总分：{exam.total_score}）")

    # 额外检查：试卷总分是否与配置总分匹配
    if total_score == exam.total_score:
        print("试卷总分与配置总分匹配")
    else:
        print("试卷总分与配置总分不匹配，请检查题目分值分配")
        if input("是否自动更改试卷分值（Y/N）：") == "Y" or "y":
            exam.total_score = total_score
            session.commit()
            print(f"修改成功------试卷总分：{total_score}（配置总分：{exam.total_score}）")
        else:
            print("请检查数据库")





