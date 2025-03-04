import json
import re

from sqlalchemy import and_

from src.education_sql.Create import *


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
            question_type, chinese_type = convert_question_type(q["type"])

            # 3.2 创建题目主体
            new_question = Question(
                subject_id=subject.subject_id,
                question_type=question_type,
                original_type=chinese_type,  # 保存中文题型
                content=q["content"],
                explanation=q.get("explanation", ""),
                difficulty=convert_difficulty(q["degree"]),
                topic=q["topic"],
                meta_data={
                    "source_exam_id": exam.exam_id,
                    "original_number": q["number"],
                    "correct_answer": q.get("correct_answer", "")
                },
                question_category=get_question_category(question_type)
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


def convert_question_type(original_type: str) -> tuple:
    """将中文题型或简化英文题型转换为数据库存储的类型和中文类型"""
    type_map = {
        '选择题': 'single_choice',
        '多选题': 'multi_choice',
        '判断题': 'judgment',
        '填空题': 'fill_blank',
        '简答题': 'short_answer',
        '应用计算题': 'application'
    }

    # 反向映射
    reverse_map = {v: k for k, v in type_map.items()}

    # 简化英文题型映射到中文
    simplified_to_chinese = {
        'choice': '选择题',
        'fill': '填空题',
        'judge': '判断题',
        'short_answer': '简答题',
        'application': '应用计算题'
    }

    original_type = original_type.strip()

    # 如果是简化英文，转换为中文和数据库类型
    if original_type in simplified_to_chinese:
        chinese_type = simplified_to_chinese[original_type]
        return type_map[chinese_type], chinese_type

    # 如果是中文，直接使用
    if original_type in type_map:
        return type_map[original_type], original_type

    # 如果已经是标准数据库类型，转换为中文
    if original_type in reverse_map:
        return original_type, reverse_map[original_type]

    # 特殊处理
    if '应用' in original_type and '计算' in original_type:
        return 'application', '应用计算题'
    if '简答' in original_type:
        return 'short_answer', '简答题'
    if '选择' in original_type:
        return 'single_choice', '选择题'
    if '判断' in original_type:
        return 'judgment', '判断题'
    if '填空' in original_type:
        return 'fill_blank', '填空题'

    # 默认返回原始类型
    return original_type, original_type


def get_question_category(question_type):
    """根据题型判断主客观"""
    objective_types = ['single_choice', 'multi_choice', 'judgment']
    return 'objective' if question_type in objective_types else 'subjective'


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
        .join(Question, and_(KnowledgePoint.question_id == Question.question_id)) \
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


def grade_objective_questions(session, record_id):
    """自动批改客观题"""
    record = session.get(StudentAnswerRecord, record_id)
    
    # 获取试卷ID
    exam_id = record.exam_id
    print(f"批改试卷ID: {exam_id}的客观题")
    
    # 获取试卷中的所有题目信息
    exam_questions = session.query(ExamQuestion).filter(
        ExamQuestion.exam_id == exam_id
    ).all()
    
    # 创建exam_question_id到question的映射
    eq_to_question = {}
    for eq in exam_questions:
        question = session.query(Question).filter(
            and_(Question.question_id == eq.question_id)
        ).first()
        if question:
            eq_to_question[eq.eq_id] = question
            print(f"试卷题目映射: exam_question_id={eq.eq_id}, question_id={question.question_id}, 类型={question.question_type}, 类别={question.question_category}")
    
    # 获取学生回答的所有题目
    details = session.query(QuestionAnswerDetail).filter(
        QuestionAnswerDetail.record_id == record_id
    ).all()
    
    # 检查学生回答的题目ID是否在映射中
    for detail in details:
        eq_id = detail.exam_question_id
        if eq_id not in eq_to_question:
            print(f"警告: 未找到exam_question_id为{eq_id}的题目映射，尝试获取题目信息")
            # 尝试直接从数据库获取题目信息
            eq = session.query(ExamQuestion).filter(
                and_(ExamQuestion.eq_id == eq_id)
            ).first()
            
            if eq:
                question = session.query(Question).filter(
                    and_(Question.question_id == eq.question_id)
                ).first()
                if question:
                    eq_to_question[eq_id] = question
                    print(f"成功获取题目信息: exam_question_id={eq_id}, question_id={question.question_id}, 类型={question.question_type}")
    
    # 筛选出客观题
    objective_details = []
    for detail in details:
        eq_id = detail.exam_question_id
        if eq_id in eq_to_question and eq_to_question[eq_id].question_category == 'objective':
            objective_details.append(detail)
    
    print(f"找到{len(objective_details)}道客观题需要批改")

    total_score = 0
    for detail in objective_details:
        eq_id = detail.exam_question_id
        if eq_id not in eq_to_question:
            print(f"警告: 未找到exam_question_id为{eq_id}的题目映射")
            continue
            
        question = eq_to_question[eq_id]
        question_type = question.question_type

        print(f"\n处理题目：{eq_id}")
        print(f"题目类型：{question_type}")

        # 获取正确答案和判分逻辑
        if question_type in ['single_choice', 'multi_choice']:
            # 处理选择题
            correct_options = [opt.option_key for opt in question.options if opt.is_correct]
            correct_answer = ','.join(sorted(correct_options))
            student_answer = detail.student_answer or ''

            # 处理多选题答案比较
            if question_type == 'multi_choice':
                student_options = sorted(student_answer.split(','))
                student_answer = ','.join(student_options)

            print(f"正确答案：{correct_answer}")
            print(f"学生答案：{student_answer}")

            if student_answer.strip().upper() == correct_answer.strip().upper():
                detail.auto_score = detail.exam_question.assigned_score
            else:
                detail.auto_score = 0

        elif question_type == 'judgment':
            # 处理判断题
            correct_options = [opt for opt in question.options if opt.is_correct]
            if correct_options:
                # 从选项中获取正确答案
                correct_option = correct_options[0].option_key
                # 转换为标准格式进行比较
                if correct_option in ['A', '对', 'T', 'True', 'TRUE', '√']:
                    correct_answer = 'T'
                elif correct_option in ['B', '错', 'F', 'False', 'FALSE', '×']:
                    correct_answer = 'F'
                else:
                    correct_answer = correct_option
            else:
                # 从correct_answer字段获取
                correct_answer = question.correct_answer or ''
                # 转换为标准格式
                if correct_answer in ['√', '对', 'A']:
                    correct_answer = 'T'
                elif correct_answer in ['×', '错', 'B']:
                    correct_answer = 'F'

            student_answer = detail.student_answer or ''
            # 标准化学生答案
            if student_answer in ['√', '对', 'A']:
                student_answer = 'T'
            elif student_answer in ['×', '错', 'B']:
                student_answer = 'F'

            print(f"正确答案：{correct_answer}")
            print(f"学生答案：{student_answer}")

            # 标准化比较
            if student_answer.strip().upper() == correct_answer.strip().upper():
                detail.auto_score = detail.exam_question.assigned_score
            else:
                detail.auto_score = 0

        elif question_type == 'fill_blank':
            # 处理填空批改
            try:
                correct_answer = question.correct_answer or ''
                student_answer = detail.student_answer or ''

                # 分割答案进行比较
                correct_parts = correct_answer.split('|||')
                student_parts = student_answer.split('|||')

                # 确保学生答案和正确答案数量一致
                if len(student_parts) != len(correct_parts):
                    print(
                        f"警告：填空题答案数量不匹配 - 正确答案:{len(correct_parts)}个, 学生答案:{len(student_parts)}个")

                # 计算正确的填空数
                correct_count = 0
                for i, (student_part, correct_part) in enumerate(zip(student_parts, correct_parts)):
                    # 清理和标准化答案进行比较
                    student_clean = re.sub(r'\s+', '', student_part).lower()
                    correct_clean = re.sub(r'\s+', '', correct_part).lower()

                    if student_clean == correct_clean:
                        correct_count += 1
                        print(f"填空{i + 1}正确")
                    else:
                        print(f"填空{i + 1}错误: 学生答案='{student_part}', 正确答案='{correct_part}'")

                # 计算得分
                if len(correct_parts) > 0:
                    detail.auto_score = round(
                        (correct_count / len(correct_parts)) * detail.exam_question.assigned_score, 1)
                else:
                    detail.auto_score = 0

                print(
                    f"填空题得分: {detail.auto_score}/{detail.exam_question.assigned_score} ({correct_count}/{len(correct_parts)}正确)")

            except Exception as e:
                print(f"填空批改错误：{str(e)}")
                detail.auto_score = 0
        else:
            # 其他未知客观题类型
            print(f"未知客观题类型: {question_type}")
            detail.auto_score = 0

        # 更新最终得分和状态
        detail.final_score = detail.auto_score
        detail.status = 'auto_graded'
        total_score += detail.final_score
        print(f"最终得分：{detail.final_score}/{detail.exam_question.assigned_score}")

    # 更新总分
    record.total_score = total_score

    # 检查是否需要人工批改
    has_subjective = session.query(ExamQuestion).join(
        Question, and_(ExamQuestion.question_id == Question.question_id)
    ).filter(
        ExamQuestion.exam_id == record.exam_id,
        Question.question_category == 'subjective'
    ).count() > 0

    # 如果没有主观题，则标记为已完成批改
    if not has_subjective:
        record.status = 'graded'
    else:
        # 如果有主观题，则标记为需要人工批改
        record.status = 'pending_manual'

    print(f"客观题总分：{total_score}")
    print(f"记录状态：{record.status}")

    # 提交更改
    session.commit()


def save_student_answers(session, answer_data):
    """存储学生作答记录"""
    try:
        # 创建答题记录
        new_record = StudentAnswerRecord(
            student_id=answer_data['student_id'],
            exam_id=answer_data['exam_id'],
            start_time=datetime.now(),
            status='in_progress'
        )
        session.add(new_record)
        session.flush()  # 获取生成的record_id

        # 处理每道题的答案
        for answer in answer_data['answers']:
            # print(answer)
            answer_detail = process_single_answer(new_record.id, answer)
            session.add(answer_detail)

        session.commit()
        return new_record.id
    except Exception as e:
        session.rollback()
        raise e


def process_single_answer(record_id, answer):
    """处理单个题目答案"""
    # 统一处理不同题型
    question_type = answer['question_type']

    # 题型映射，确保兼容性
    type_mapping = {
        'single_choice': handle_choice,
        'multi_choice': handle_choice,
        'fill_blank': handle_fill_blank,
        'judgment': handle_judgment,  # 只保留judgment类型
        'short_answer': handle_essay,  # 简答题
        'application': handle_essay  # 应用计算题
    }

    handler = type_mapping.get(question_type, handle_unknown)
    return handler(record_id, answer)


def handle_choice(record_id, answer):
    """处理选择题型"""
    return QuestionAnswerDetail(
        record_id=record_id,
        exam_question_id=answer['exam_question_id'],
        student_answer=answer['answer_data']["selected_option"],
        status='pending'
    )


def handle_fill_blank(record_id, answer):
    """处理填空题（添加清洗）"""
    # 打印调试信息
    print(f"处理填空题: {answer['exam_question_id']}")
    print(f"原始答案数据: {answer['answer_data']}")
    
    # 检查答案格式
    if 'filled_answers' in answer['answer_data']:
        filled_answers = answer['answer_data']['filled_answers']
        print(f"填空答案: {filled_answers}")
        
        # 确保filled_answers是列表
        if not isinstance(filled_answers, list):
            filled_answers = [str(filled_answers)]
            
        # 清洗答案：移除空格和特殊符号
        cleaned = [re.sub(r'\s+', '', ans).replace('^', '') for ans in filled_answers]
        student_answer = "|||".join(cleaned)
    elif 'content' in answer['answer_data']:
        # 如果已经转换为content格式
        student_answer = answer['answer_data']['content']
    else:
        # 默认空答案
        student_answer = ""
        print(f"警告: 填空题 {answer['exam_question_id']} 没有有效答案")

    print(f"处理后的答案: {student_answer}")
    
    return QuestionAnswerDetail(
        record_id=record_id,
        exam_question_id=answer['exam_question_id'],
        student_answer=student_answer,
        status='pending'
    )


def handle_judgment(record_id, answer):
    """处理判断题"""
    return QuestionAnswerDetail(
        record_id=record_id,
        exam_question_id=answer['exam_question_id'],
        student_answer=answer['answer_data']['selected_option'],
        status='pending'
    )


def handle_essay(record_id, answer):
    """处理主观题"""
    return QuestionAnswerDetail(
        record_id=record_id,
        exam_question_id=answer['exam_question_id'],
        student_answer=answer['answer_data']['content'],
        status='pending'
    )


def handle_unknown(record_id, answer):
    """处理未知题型（默认方法）"""
    return QuestionAnswerDetail(
        record_id=record_id,
        exam_question_id=answer['exam_question_id'],
        student_answer=json.dumps(answer['answer_data']),
        status='pending',
        feedback='未知题型需要人工批改'
    )
