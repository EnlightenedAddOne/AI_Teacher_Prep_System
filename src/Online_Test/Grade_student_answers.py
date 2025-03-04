# 批改学生作答数据的主函数
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.configs import config
from src.education_sql import (
    ExamQuestion, Question, StudentAnswerRecord,
    QuestionAnswerDetail, save_student_answers,
    grade_objective_questions
)
from src.models import (
    StudentAnswerRequest, StudentAnswerResponse,
    QuestionDetail, ScoreSummary, GradingStatus
)
from .AI_correcting_paper import ai_grade_subjective

# 添加状态映射
STATUS_MAPPING = {
    'pending': GradingStatus.PENDING,
    'auto_graded': GradingStatus.GRADED,
    'manually_graded': GradingStatus.GRADED,
    'pending_manual': GradingStatus.PENDING_MANUAL
}


def grade_student_answers(session: Session, request: StudentAnswerRequest) -> StudentAnswerResponse:
    """批改学生作答的主函数
    
    Args:
        session: 数据库会话
        request: 学生作答请求
        
    Returns:
        StudentAnswerResponse: 批改结果响应
        
    Raises:
        ValueError: 当保存作答记录失败或API密钥未配置时
    """
    # 确保学生和考试记录存在
    student_id = request.student_id
    exam_id = request.exam_id

    # 获取试卷中的所有题目，按照sort_order排序
    exam_questions = session.query(ExamQuestion).filter(
        and_(ExamQuestion.exam_id == exam_id)
    ).order_by(ExamQuestion.sort_order).all()

    # 创建学生答案中的题目ID到实际数据库题目ID的映射
    student_eq_id_to_actual_eq_id = {}
    for i, eq in enumerate(exam_questions, start=1):
        student_eq_id_to_actual_eq_id[i] = eq.eq_id

    # 更新学生答案中的exam_question_id为实际数据库中的ID
    answers_data = request.answers
    for answer in answers_data:
        student_eq_id = answer.exam_question_id
        if student_eq_id in student_eq_id_to_actual_eq_id:
            answer.exam_question_id = student_eq_id_to_actual_eq_id[student_eq_id]

    # 保存学生作答记录
    answer_data = {
        "exam_id": exam_id,
        "student_id": student_id,
        "answers": [answer.dict() for answer in answers_data]
    }
    record_id = save_student_answers(session, answer_data)

    if not record_id:
        raise ValueError("保存作答记录失败")

    # 自动批改客观题
    grade_objective_questions(session, record_id)
    session.commit()

    # AI批改主观题
    api_key = config['api_keys'].get('deepseek_api_key')
    if not api_key:
        raise ValueError("DeepSeek API密钥未配置")

    # 确保主观题的question_category正确设置
    subjective_types = ['short_answer', 'application', 'fill_blank']
    exam_questions = session.query(ExamQuestion).filter(
        and_(ExamQuestion.exam_id == exam_id)
    ).all()

    for eq in exam_questions:
        question = session.query(Question).filter(
            and_(Question.question_id == eq.question_id)
        ).first()

        if question and question.question_type in subjective_types:
            if question.question_category != 'subjective':
                question.question_category = 'subjective'
                session.add(question)

    session.commit()

    # 调用AI批改
    ai_grade_subjective(session, record_id, api_key)
    session.commit()

    # 获取批改结果
    record = session.get(StudentAnswerRecord, record_id)

    # 将数据库中的状态转换为GradingStatus枚举
    record_status = STATUS_MAPPING.get(record.status, GradingStatus.PENDING)

    # 获取题目详情
    details = session.query(
        QuestionAnswerDetail.exam_question_id,
        QuestionAnswerDetail.final_score,
        QuestionAnswerDetail.status,
        QuestionAnswerDetail.student_answer,  # 添加学生答案字段
        Question.question_type,
        Question.content,
        Question.meta_data,  # 添加meta_data字段
        Question.explanation,
        ExamQuestion.assigned_score
    ).join(
        ExamQuestion, and_(QuestionAnswerDetail.exam_question_id == ExamQuestion.eq_id)
    ).join(
        Question, and_(ExamQuestion.question_id == Question.question_id)
    ).filter(
        QuestionAnswerDetail.record_id == record_id
    ).all()

    # 计算得分统计
    objective_score = 0
    subjective_score = 0
    objective_total = 0
    subjective_total = 0

    question_details = []
    for detail in details:
        final_score = detail.final_score or 0

        # 统计客观题和主观题得分
        if detail.question_type in ['single_choice', 'multi_choice', 'judgment']:
            objective_score += final_score
            objective_total += detail.assigned_score
        else:
            subjective_score += final_score
            subjective_total += detail.assigned_score

        # 从meta_data中获取correct_answer
        correct_answer = ""
        try:
            if detail.meta_data:
                if isinstance(detail.meta_data, str):
                    import json
                    meta_data = json.loads(detail.meta_data)
                else:
                    meta_data = detail.meta_data

                # 尝试从meta_data中获取correct_answer
                if isinstance(meta_data, dict):
                    correct_answer = meta_data.get('correct_answer', '')

                    # 如果是"见解析"类型的答案，使用解析作为正确答案
                    reference_phrases = ["见解析", "参考解析", "见答案解析", "见详解", "详见解析", "略", "略。", "略"]
                    if not correct_answer or correct_answer.strip() in reference_phrases:
                        correct_answer = detail.explanation or ""

                print(f"题目ID: {detail.exam_question_id}, 从meta_data获取的正确答案: {correct_answer}")
        except Exception as e:
            print(f"解析meta_data时出错: {str(e)}, 题目ID: {detail.exam_question_id}")
            correct_answer = ""

        # 映射状态值到GradingStatus枚举
        status_str = detail.status if detail.status else 'pending'
        mapped_status = STATUS_MAPPING.get(status_str, GradingStatus.PENDING)

        # 构建题目详情
        question_detail = QuestionDetail(
            exam_question_id=detail.exam_question_id,
            question_type=detail.question_type,
            content=detail.content,
            assigned_score=detail.assigned_score,
            student_answer=detail.student_answer,
            correct_answer=correct_answer,  # 使用从meta_data中获取的correct_answer
            explanation=detail.explanation,
            final_score=final_score,
            status=mapped_status  # 使用映射后的状态
        )
        question_details.append(question_detail)

    # 构建响应
    return StudentAnswerResponse(
        record_id=record_id,
        student_id=student_id,
        exam_id=exam_id,
        status=record_status,  # 使用记录的状态
        score_summary=ScoreSummary(
            objective_score=objective_score,
            objective_total=objective_total,
            subjective_score=subjective_score,
            subjective_total=subjective_total,
            total_score=objective_score + subjective_score,
            total_possible=objective_total + subjective_total
        ),
        question_details=question_details
    )
