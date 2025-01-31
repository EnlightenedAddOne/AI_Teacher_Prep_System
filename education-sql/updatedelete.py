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

def delete_exam_with_others(session: Session, exam_id: int) -> bool:
    """删除试卷及其所有关联题目、选项和知识点"""
    try:
        # 开启事务
        session.begin()

        # 1. 获取所有关联题目ID
        question_ids = session.query(ExamQuestion.question_id)\
                            .filter_by(exam_id=exam_id)\
                            .all()
        question_ids = [qid for (qid,) in question_ids]

        # 2. 删除knowledge_graph表中与题目关联的记录
        session.query(KnowledgePoint)\
             .filter(KnowledgePoint.question_id.in_(question_ids))\
             .delete(synchronize_session=False)

        # 3. 删除题目选项
        session.query(QuestionOption)\
             .filter(QuestionOption.question_id.in_(question_ids))\
             .delete(synchronize_session=False)

        # 4. 删除试卷题目关联
        session.query(ExamQuestion).filter_by(exam_id=exam_id).delete()

        # 5. 删除所有关联题目
        session.query(Question)\
             .filter(Question.question_id.in_(question_ids))\
             .delete(synchronize_session=False)

        # 6. 删除试卷主体
        session.query(Exam).filter_by(exam_id=exam_id).delete()

        # 提交事务
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        print(f"删除失败：{str(e)}")
        return False






def delete_question(session, question_id):
    """安全删除题目（级联删除所有关联）"""
    try:
        # 先删除所有关联关系
        session.query(ExamQuestion).filter_by(question_id=question_id).delete(synchronize_session=False)
        session.query(QuestionOption).filter_by(question_id=question_id).delete(synchronize_session=False)
        # 删除题目
        question = session.query(Question).get(question_id)
        if question:
            session.delete(question)
            session.commit()
            print(f"题目 {question_id} 删除成功")
            return True
    except Exception as e:
        session.rollback()
        print(f"删除失败：{str(e)}")
        return False



