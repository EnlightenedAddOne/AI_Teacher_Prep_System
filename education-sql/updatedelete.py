from Create import *


def update_question_content(session, question_id, new_content):
    """更新题目内容"""
    question = session.query(Question).get(question_id)
    if not question:
        print("题目不存在")
        return False

    question.content = new_content
    session.commit()
    print("题目内容更新成功")
    return True


def delete_exam(session, exam_id):
    """安全删除试卷（级联删除关联题目关系）"""
    try:
        # 先手动删除关联关系（双保险）
        session.query(ExamQuestion).filter_by(exam_id=exam_id).delete()

        exam = session.query(Exam).get(exam_id)
        if exam:
            session.delete(exam)
            session.commit()
            print(f"试卷 {exam_id} 删除成功")
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"删除失败：{str(e)}")
        return False

def adjust_exam_question(session, exam_id, question_id, new_score=None, new_order=None):
    """调整试卷中的题目"""
    eq = session.query(ExamQuestion).filter_by(exam_id=exam_id, question_id=question_id).first()
    if not eq:
        print("试卷中不存在该题目")
        return False

    if new_score is not None:
        eq.assigned_score = new_score

    if new_order is not None:
        eq.sort_order = new_order

    session.commit()
    print("试卷题目调整成功")
    return True


def delete_question(session, question_id):
    """安全删除题目（级联删除所有关联）"""
    try:
        # 先删除所有关联关系
        session.query(ExamQuestion).filter_by(question_id=question_id).delete()
        session.query(QuestionOption).filter_by(question_id=question_id).delete()
        session.query(QuestionPoint).filter_by(question_id=question_id).delete()

        question = session.query(Question).get(question_id)
        if question:
            session.delete(question)
            session.commit()
            print(f"题目 {question_id} 删除成功")
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"删除失败：{str(e)}")
        return False


