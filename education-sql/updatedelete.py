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
    """删除题目（自动处理关联关系）"""
    question = session.query(Question).get(question_id)
    if not question:
        print("题目不存在")
        return False

    # 检查是否被试卷引用
    if len(question.exam_links) > 0:
        print("该题目已被试卷使用，无法删除")
        return False

    try:
        # 删除关联选项和知识点
        session.query(QuestionOption).filter_by(question_id=question_id).delete()
        session.query(QuestionPoint).filter_by(question_id=question_id).delete()
        session.delete(question)
        session.commit()
        print("题目删除成功")
        return True
    except Exception as e:
        session.rollback()
        print(f"删除失败：{str(e)}")
        return False


