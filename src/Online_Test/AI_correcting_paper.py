# AI批改主观题
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.education_sql import QuestionAnswerDetail, Question, ExamQuestion, StudentAnswerRecord
from src.llm_integration import LLMFactory
from src.utils.prompts import ai_grading_system_prompt, ai_grading_user_prompt
import json
import re


class AIGrader:
    def __init__(self, api_key: str):
        self.client = LLMFactory.initialize_deepseek(api_key)

    def grade_single_answer(self, question_type: str, student_answer: str, correct_answer: str,
                            max_score: int) -> float:
        """单题批改核心逻辑"""
        # 确保输入参数不为None
        student_answer = student_answer or ""
        correct_answer = correct_answer or ""
        max_score = max_score or 0
        
        # 生成提示词
        system_msg = ai_grading_system_prompt.format(
            question_type=question_type,
            max_score=max_score
        )
        user_msg = ai_grading_user_prompt.format(
            correct_answer=correct_answer,
            student_answer=student_answer
        )

        # 调用AI接口
        try:
            response = LLMFactory.call_deepseek(
                client=self.client,
                system_prompt=system_msg,
                user_prompt=user_msg,
                model="deepseek-reasoner",
                temperature=0.1
            )
        except Exception as e:
            print(f"AI接口调用失败: {str(e)}")
            return 0.0

        # 解析结果
        try:
            # 检查响应是否为空
            if not response or response.isspace():
                print(f"警告: AI返回了空响应")
                return 0.0
                
            # 清理响应中的Markdown代码块标记
            cleaned_response = re.sub(r'```json\s*|\s*```', '', response.strip())
            
            # 尝试解析JSON
            try:
                result = json.loads(cleaned_response)
                if "score" in result:
                    score = min(max(float(result["score"]), 0), max_score)
                    return round(score, 1)
                else:
                    print(f"警告: AI响应中没有score字段: {cleaned_response}")
                    # 尝试直接从文本中提取分数
                    score_match = re.search(r'(\d+(\.\d+)?)', cleaned_response)
                    if score_match:
                        score = min(max(float(score_match.group(1)), 0), max_score)
                        return round(score, 1)
                    return 0.0
            except json.JSONDecodeError:
                # 如果不是JSON格式，尝试直接从文本中提取分数
                print(f"警告: AI响应不是有效的JSON格式: {cleaned_response}")
                score_match = re.search(r'(\d+(\.\d+)?)', cleaned_response)
                if score_match:
                    score = min(max(float(score_match.group(1)), 0), max_score)
                    return round(score, 1)
                return 0.0
        except Exception as e:
            print(f"评分解析失败: {str(e)}, 响应内容: {response[:100]}...")
            return 0.0


def ai_grade_subjective(session: Session, record_id: int, api_key: str):
    """主批改入口函数"""
    try:
        grader = AIGrader(api_key)
        
        # 首先获取学生作答记录，确定是哪套试卷
        student_record = session.query(StudentAnswerRecord).filter(
            and_(StudentAnswerRecord.id == record_id)
        ).first()
        
        if not student_record:
            print(f"错误: 未找到ID为{record_id}的作答记录")
            return
        
        # 获取学生实际作答的试卷ID
        exam_id = student_record.exam_id
        print(f"正在批改试卷ID: {exam_id}的主观题")
        
        # 获取试卷中的所有题目信息
        exam_questions = session.query(ExamQuestion).filter(
            and_(ExamQuestion.exam_id == exam_id)
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
        all_answers = session.query(QuestionAnswerDetail).filter(
            and_(QuestionAnswerDetail.record_id == record_id)
        ).all()
        print(f"学生总共回答了{len(all_answers)}道题目")
        
        # 直接从学生的答题记录中获取需要批改的主观题
        print("开始查询需要批改的主观题...")
        
        # 修改查询方式，使用预先建立的映射来确定题目类型
        answers = []
        for answer_detail in all_answers:
            try:
                eq_id = answer_detail.exam_question_id
                
                # 使用映射获取题目信息
                if eq_id not in eq_to_question:
                    print(f"警告: 未找到exam_question_id为{eq_id}的题目映射")
                    # 尝试直接从数据库获取题目信息
                    eq = session.query(ExamQuestion).filter(
                        and_(ExamQuestion.eq_id == eq_id)
                    ).first()
                    
                    if not eq:
                        print(f"警告: 未找到题目ID为{eq_id}的考试题目")
                        continue
                        
                    question = session.query(Question).filter(
                        and_(Question.question_id == eq.question_id)
                    ).first()
                    
                    if not question:
                        print(f"警告: 未找到题目ID为{eq.question_id}的题目")
                        continue
                        
                    eq_to_question[eq_id] = question
                    print(f"成功获取题目信息: exam_question_id={eq_id}, question_id={question.question_id}, 类型={question.question_type}")
                
                question = eq_to_question[eq_id]
                
                # 获取题目所属的ExamQuestion
                eq = session.query(ExamQuestion).filter(
                    and_(ExamQuestion.eq_id == eq_id)
                ).first()
                
                if not eq:
                    print(f"警告: 未找到题目ID为{eq_id}的考试题目")
                    continue
                
                print(f"题目ID: {eq_id}, 类型: {question.question_type}, 类别: {question.question_category}")
                
                # 检查是否为主观题
                if question.question_type in ['short_answer', 'application', 'essay', 'fill_blank'] or question.question_category == 'subjective':
                    print(f"找到主观题: ID={eq_id}, 类型={question.question_type}")
                    # 确保类别正确
                    if question.question_category != 'subjective':
                        question.question_category = 'subjective'
                        session.add(question)
                        session.commit()
                        print(f"已更新题目类别为subjective")
                    
                    # 添加到需要批改的列表
                    answer_detail.exam_question = eq
                    answer_detail.exam_question.question = question
                    answers.append(answer_detail)
            except Exception as e:
                print(f"处理题目时出错: {str(e)}")
                continue
        
        print(f"找到{len(answers)}道主观题需要批改")
        
        if not answers:
            print("没有找到需要批改的主观题")
            
            # 调试: 检查question_category字段是否正确设置
            question_types = session.query(Question.question_type, Question.question_category).join(
                ExamQuestion, and_(ExamQuestion.question_id == Question.question_id)
            ).filter(
                and_(ExamQuestion.exam_id == exam_id)
            ).all()
            print("试卷中的题目类型和类别:")
            for qtype, qcat in question_types:
                print(f"题型: {qtype}, 类别: {qcat}")
            
            # 尝试直接从学生回答的题目中找出主观题
            print("尝试从学生回答中直接识别主观题...")
            for answer_detail in all_answers:
                eq = session.query(ExamQuestion).filter(and_(ExamQuestion.eq_id == answer_detail.exam_question_id)).first()
                if eq and eq.exam_id == exam_id:
                    q = session.query(Question).filter(and_(Question.question_id == eq.question_id)).first()
                    if q and q.question_type in ['short_answer', 'application', 'fill_blank']:
                        print(f"找到主观题: ID={q.question_id}, 类型={q.question_type}")
                        # 手动更新question_category
                        q.question_category = 'subjective'
                        session.add(q)
            
            session.commit()
            print("已更新题目类别，请重新运行批改")
            return
        
        for answer in answers:
            try:
                exam_question = answer.exam_question
                question = exam_question.question
                
                # 确认题目所属试卷
                if exam_question.exam_id != exam_id:
                    print(f"警告: 题目所属试卷ID: {exam_question.exam_id}, 与当前处理试卷ID: {exam_id} 不一致，跳过此题")
                    continue
    
                # 获取正确答案
                correct_answer = ""
                if question.meta_data and "correct_answer" in question.meta_data:
                    correct_answer = question.meta_data.get("correct_answer", "")
                    print(f"从meta_data获取的正确答案: {correct_answer}")
                
                # 如果meta_data中没有答案或答案为空，尝试从选项中获取
                if not correct_answer and question.options:
                    try:
                        correct_answer = next(
                            (opt.option_content for opt in question.options if opt.option_key == "answer"),
                            ""
                        )
                        print(f"从选项获取的正确答案: {correct_answer}")
                    except Exception as e:
                        print(f"获取选项答案失败: {str(e)}")
                        correct_answer = ""
                
                # 处理简答题和应用计算题的特殊情况：当答案是"见解析"时，使用解析作为正确答案
                if question.question_type in ['short_answer', 'application', 'fill_blank']:
                    # 可能的"见解析"表述列表
                    reference_phrases = ["见解析", "参考解析", "见答案解析", "见详解", "详见解析", "略", "略。", "略"]
                    
                    if not correct_answer or correct_answer.strip() in reference_phrases:
                        # 获取题目解析
                        explanation = question.explanation or ""
                        if explanation and explanation.strip():
                            print(f"使用解析作为正确答案: {explanation[:50]}..." if len(explanation) > 50 else f"使用解析作为正确答案: {explanation}")
                            # 合并解析作为正确答案
                            if correct_answer and correct_answer.strip() not in reference_phrases:
                                correct_answer = f"{correct_answer}\n\n{explanation}"
                            else:
                                correct_answer = explanation
                        else:
                            print(f"警告: 题目ID={question.question_id}的解析为空，无法用作正确答案")
                            # 如果既没有正确答案也没有解析，给出警告
                            if not correct_answer or correct_answer.strip() in reference_phrases:
                                print(f"严重警告: 题目ID={question.question_id}既没有有效的正确答案也没有解析")
                                # 使用题目内容作为提示
                                correct_answer = f"此题没有标准答案。题目内容: {question.content[:100]}..."
                
                student_answer = answer.student_answer or ""
                
                print(f"批改题目ID: {exam_question.eq_id}, 题型: {question.question_type}")
                print(f"正确答案: {correct_answer[:50]}..." if len(correct_answer) > 50 else f"正确答案: {correct_answer}")
                print(f"学生答案: {student_answer[:50]}..." if len(student_answer) > 50 else f"学生答案: {student_answer}")
    
                # 清理和格式化答案
                # 移除多余的空白字符
                correct_answer = re.sub(r'\s+', ' ', correct_answer).strip()
                student_answer = re.sub(r'\s+', ' ', student_answer).strip()
                
                # 确保答案不为空
                if not correct_answer:
                    correct_answer = "无标准答案"
                if not student_answer:
                    student_answer = "学生未作答"
                
                # 对于填空题，特殊处理分隔符
                if question.question_type == 'fill_blank':
                    # 将填空题的分隔符统一为分号
                    correct_answer = correct_answer.replace('|||', '; ')
                    student_answer = student_answer.replace('|||', '; ')
                
                print(f"处理后的正确答案: {correct_answer[:50]}..." if len(correct_answer) > 50 else f"处理后的正确答案: {correct_answer}")
                print(f"处理后的学生答案: {student_answer[:50]}..." if len(student_answer) > 50 else f"处理后的学生答案: {student_answer}")
    
                # AI评分
                ai_score = grader.grade_single_answer(
                    question_type=question.question_type,
                    student_answer=student_answer,
                    correct_answer=correct_answer,
                    max_score=exam_question.assigned_score
                )
    
                # 更新记录
                answer.auto_score = ai_score
                answer.final_score = ai_score
                answer.status = 'auto_graded'
                session.add(answer)
                
                print(f"AI评分结果: {ai_score}/{exam_question.assigned_score}")
                print("-" * 50)
            except Exception as e:
                print(f"处理题目时出错: {str(e)}")
                continue
    
        session.commit()
        print("主观题批改完成")
    except Exception as e:
        print(f"AI批改过程中发生错误: {str(e)}")
        session.rollback()
