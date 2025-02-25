from Create import *
import json
from datetime import datetime
import re


def import_exam_paper(session, json_data, exam_name:str):
    """完整试卷导入函数"""
    try:
        # 1. 处理学科信息
        subject_name = json_data["questions"][0]["subject"]  # 从题目中获取学科
        subject = session.query(Subject).filter_by(subject_name=subject_name).first()
        if not subject:
            subject = Subject(subject_name=subject_name)
            session.add(subject)
            session.flush()  # 立即获取subject_id

        # 2. 创建试卷记录
        exam = Exam(
            exam_name=json_data.get("exam_name", f"{exam_name}"),
            subject_id=subject.subject_id,
            subject_name=subject_name,
            total_score=json_data["test_info"]["total_score"],
            time_limit=json_data["test_info"]["time_limit"]
        )
        session.add(exam)
        session.flush()

        # 3. 处理所有题目
        for order, q in enumerate(json_data["questions"], start=1):
            # 3.1 转换题型
            question_type = convert_question_type(q["type"])

            # 3.2 创建题目主体
            new_question = Question(
                subject_id=subject.subject_id,
                question_type=question_type,
                original_type=q["type"],  # 保留原始题型名称
                content=q["content"],
                explanation=q.get("explanation", ""),
                difficulty=convert_difficulty(q["degree"]),
                topic=q["topic"],
                meta_data={
                    "source_exam_id": exam.exam_id,
                    "original_number": q["number"]
                },
                question_category=get_question_category(question_type)
            )

            # 3.3 处理选项
            if question_type in ['single_choice', 'multi_choice', 'judgment']:
                for opt in q["options"]:
                    is_correct = (opt["key"] == q["correct_answer"])
                    new_question.options.append(
                        QuestionOption(
                            option_key=opt["key"],
                            option_content=opt["value"],
                            is_correct=is_correct
                        )
                    )

            # 3.4 处理知识点
            for point_name in q["knowledge_points"]:
                new_point = KnowledgePoint(
                    point_name=point_name,
                    subject_id=subject.subject_id
                )
                new_question.knowledge_points.append(new_point)

            session.add(new_question)
            session.flush()  # 立即获取question_id

            # 3.5 关联到试卷
            exam_question = ExamQuestion(
                exam_id=exam.exam_id,
                question_id=new_question.question_id,
                display_number=q["number"],
                assigned_score=q["score"],
                sort_order=order
            )
            session.add(exam_question)

        session.commit()
        print(f"试卷导入成功！试卷ID：{exam.exam_id}")
        return exam.exam_id

    except Exception as e:
        session.rollback()
        print(f"导入失败：{str(e)}")
        return None


def convert_question_type(original_type):
    """转换题型到标准格式"""
    type_map = {
        "选择题": "single_choice",
        "填空题": "fill_blank",
        "判断题": "judgment",
        "简答题": "essay",
        "应用计算题": "essay"
    }
    return type_map.get(original_type, "essay")

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
            exam.total_score=total_score
            session.commit()
            print(f"修改成功------试卷总分：{total_score}（配置总分：{exam.total_score}）")
        else:
            print("请检查数据库")


def grade_objective_questions(session, record_id):
    """自动批改客观题"""
    record = session.get(StudentAnswerRecord, record_id)
    details = session.query(QuestionAnswerDetail).join(ExamQuestion).join(Question).filter(
        QuestionAnswerDetail.record_id == record_id,
        Question.is_objective
    )
    
    total_score = 0
    for detail in details:
        question = detail.exam_question.question
        
        print(f"\n处理题目：{detail.exam_question_id}")
        print(f"题目类型：{question.question_type}")
        
        # 获取正确答案逻辑
        if question.question_type in ['single_choice', 'judgment']:
            correct_options = [opt.option_key for opt in question.options if opt.is_correct]
            correct_answer = correct_options[0] if correct_options else ''
            print(f"正确答案：{correct_answer}")
        elif question.question_type == 'fill_blank':
            # 处理填空批改
            try:
                correct_answer = question.correct_answer or ''
                student_answer = detail.student_answer or ''
                
                # 分割答案进行比较
                correct_parts = correct_answer.split('|||')
                student_parts = student_answer.split('|||')
                
                correct_count = sum(1 for s, c in zip(student_parts, correct_parts) if s.strip() == c.strip())
                detail.auto_score = round((correct_count / len(correct_parts)) * detail.exam_question.assigned_score, 1)
                
            except Exception as e:
                print(f"填空批改错误：{str(e)}")
                detail.auto_score = 0
        else:
            correct_answer = question.correct_answer
            print(f"填空答案：{correct_answer}")
        
        print(f"学生答案：{detail.student_answer}")
        
        # 判分逻辑
        if detail.student_answer.strip().upper() == correct_answer.strip().upper():
            detail.auto_score = detail.exam_question.assigned_score
        else:
            detail.auto_score = 0
            
        detail.final_score = detail.auto_score
        detail.status = 'auto_graded'
        total_score += detail.final_score
        print(f"得分：{detail.auto_score}")
    
    record.total_score = total_score
    record.status = 'graded' if record.exam.require_manual_grading else 'submitted'
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
    handler = {
        'single_choice': handle_choice,
        'multi_choice': handle_choice,
        'fill_blank': handle_fill_blank,
        'true_false': handle_judgment,
        'essay': handle_essay
    }.get(answer['question_type'], handle_unknown)

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
    # 清洗答案：移除空格和特殊符号
    cleaned = [re.sub(r'\s+', '', ans).replace('^', '') for ans in answer['answer_data']['filled_answers']]
    filled_answers = "|||".join(cleaned)
    
    return QuestionAnswerDetail(
        record_id=record_id,
        exam_question_id=answer['exam_question_id'],
        student_answer=filled_answers,
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

# def create_subject(session, name, parent_id=0):
#     """创建学科"""
#     try:
#         subject = Subject(subject_name=name, parent_id=parent_id)
#         session.add(subject)
#         session.commit()
#         print(f"创建学科成功：{subject.subject_id}-{name}")
#         return subject
#     except IntegrityError:
#         session.rollback()
#         print("学科已存在")
#         return None
#
#
# def create_exam(session, exam_name, subject_name, total_score, time_limit):
#     """创建试卷"""
#     subject = session.query(Subject).filter_by(subject_name=subject_name).first()
#     if not subject:
#         print(f"学科 {subject_name} 不存在")
#         return None
#
#     exam = Exam(
#         exam_name=exam_name,
#         subject_id=subject.subject_id,
#         total_score=total_score,
#         time_limit=time_limit
#     )
#     session.add(exam)
#     session.commit()
#     print(f"创建试卷成功：{exam.exam_id}-{exam_name}")
#     return exam
#
#
# def create_question(session, question_data):
#     """创建题目"""
#     # question_data示例结构
#     # {
#     #     "subject": "数学",
#     #     "type": "single_choice",
#     #     "content": "题目内容...",
#     #     "explanation": "解析内容...",
#     #     "options": [
#     #         {"key": "A", "content": "选项内容", "correct": True},
#     #         ...
#     #     ],
#     #     "knowledge_points": ["导数", "函数"],
#     #     "meta": {"degree": "困难", "topic": "微积分"}
#     # }
#
#     subject = session.query(Subject).filter_by(subject_name=question_data["subject"]).first()
#     if not subject:
#         print("学科不存在")
#         return None
#
#     # 创建题目主体
#     question = Question(
#         subject_id=subject.subject_id,
#         question_type=question_data["type"],
#         content=question_data["content"],
#         explanation=question_data.get("explanation", ""),
#         meta_data=question_data.get("meta", {})
#     )
#
#     # 添加选项
#     for opt in question_data["options"]:
#         question.options.append(QuestionOption(
#             option_key=opt["key"],
#             option_content=opt["content"],
#             is_correct=opt.get("correct", False)
#         ))
#
#     # 关联知识点
#     for point_name in question_data["knowledge_points"]:
#         point = session.query(KnowledgePoint).filter_by(point_name=point_name).first()
#         if not point:
#             point = KnowledgePoint(
#                 point_name=point_name,
#                 subject_id=subject.subject_id
#             )
#             session.add(point)
#         question.knowledge_points.append(point)
#
#     session.add(question)
#     session.commit()
#     print(f"创建题目成功：{question.question_id}")
#     return question