# 导入必要模块
from src.education_sql.write_data import *
from src.Online_Test import ai_grade_subjective
from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.configs import config
import json
import re

# 初始化数据库连接:
db_config = config['database']
engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# 首先确保学生记录存在
def ensure_student_exists(session, student_id: str, student_name: str = "测试学生"):
    """确保学生记录存在，如果不存在则创建"""
    student = session.query(Student).filter_by(id=student_id).first()
    if not student:
        student = Student(
            id=student_id,
            name=student_name,
            class_name="测试班级"
        )
        session.add(student)
        session.commit()
        print(f"创建学生记录：{student_id}")
    return student


# 确保考试记录存在
def ensure_exam_exists(session, exam_id: int):
    """确保考试记录存在"""
    exam = session.get(Exam, exam_id)
    if not exam:
        print(f"错误：考试ID {exam_id} 不存在")
        return False
    return True


text_answer = '''
{
      "exam_id": 2,
      "student_id": "1",
      "answers": [
        {
          "exam_question_id": 1,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "D"
          }
        },
        {
          "exam_question_id": 2,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "A"
          }
        },
        {
          "exam_question_id": 3,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "A"
          }
        },
        {
          "exam_question_id": 4,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "B"
          }
        },
        {
          "exam_question_id": 5,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "B"
          }
        },
        {
          "exam_question_id": 6,
          "question_type": "fill_blank",
          "answer_data": {
            "filled_answers": ["ln(x / (1-x))"]
          }
        },
        {
          "exam_question_id": 7,
          "question_type": "fill_blank",
          "answer_data": {
            "filled_answers": ["√2"]
          }
        },
        {
          "exam_question_id": 8,
          "question_type": "fill_blank",
          "answer_data": {
            "filled_answers": ["(2, 3)"]
          }
        },
        {
          "exam_question_id": 9,
          "question_type": "judgment",
          "answer_data": {
            "selected_option": "A"
          }
        },
        {
          "exam_question_id": 10,
          "question_type": "judgment",
          "answer_data": {
            "selected_option": "B"
          }
        },
        {
          "exam_question_id": 11,
          "question_type": "judgment",
          "answer_data": {
            "selected_option": "A"
          }
        },
        {
          "exam_question_id": 12,
          "question_type": "judgment",
          "answer_data": {
            "selected_option": "B"
          }
        },
        {
          "exam_question_id": 13,
          "question_type": "short_answer",
          "answer_data": {
            "content": "设f(x)是偶函数，则f(-x) = f(x)。对等式两边求导数，得到：f'(-x)·(-1) = f'(x)，即f'(-x) = -f'(x)。这表明f'(x)是奇函数，因为奇函数的定义就是g(-x) = -g(x)。因此，偶函数的导数是奇函数。"
          }
        },
        {
          "exam_question_id": 14,
          "question_type": "short_answer",
          "answer_data": {
            "content": "f(x) = x^3 - 3x^2 + 2x，可以因式分解为f(x) = x(x^2 - 3x + 2) = x(x-1)(x-2)。因此，f(x)的零点有：x=0（单根）、x=1（单根）和x=2（单根）。"
          }
        },
        {
          "exam_question_id": 15,
          "question_type": "application",
          "answer_data": {
            "content": "求导得f'(x) = 3x^2 - 12x + 9，令f'(x) = 0，得3(x^2 - 4x + 3) = 0，解得x = 1或x = 3。计算二阶导数f''(x) = 6x - 12，当x = 1时，f''(1) = -6 < 0，所以x = 1是极大值点；当x = 3时，f''(3) = 6 > 0，所以x = 3是极小值点。由于题目要求f(x)在x = 1处取得极小值，所以C的值应使得f''(1) > 0。但是f''(x) = 6x - 12只与x有关，与C无关。如果假设x = 1是极小值点，则C = -4，此时f(1) = 0，f(3) = 4。"
          }
        },
        {
          "exam_question_id": 16,
          "question_type": "application",
          "answer_data": {
            "content": "求导得f'(x) = e^x - 2x。对于任意x > 0，我们有e^x > 1 + x（泰勒展开的性质）。当x > 0时，1 + x > 2x仅在0 < x < 1时成立。但即使在0 < x < 1区间，我们仍有e^x > 1 + x > 2x，所以f'(x) = e^x - 2x > 0。当x ≥ 1时，e^x增长速度远大于2x，所以f'(x) > 0仍然成立。因此，在整个区间(0, +∞)上，f'(x) > 0，函数f(x)单调递增。函数的最小值出现在区间的左端点x = 0处，f(0) = e^0 - 0^2 = 1。"
          }
        }
      ]
}
'''

try:
    # 清理可能存在的无效控制字符
    cleaned_text = re.sub(r'[\x00-\x1F\x7F]', '', text_answer)

    # 处理转义字符问题
    cleaned_text = cleaned_text.replace('\\', '\\\\')

    # 尝试解析JSON
    try:
        answer_data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {str(e)}")
        print("尝试使用更严格的清理方法...")

        # 更严格的清理
        import ast

        # 移除JSON字符串中的注释和多余的换行符
        cleaned_text = re.sub(r'//.*?\n', '\n', cleaned_text)
        cleaned_text = re.sub(r'/\*.*?\*/', '', cleaned_text, flags=re.DOTALL)

        # 尝试使用ast.literal_eval作为备选方案
        try:
            # 确保是有效的JSON格式
            if not cleaned_text.strip().startswith('{'):
                cleaned_text = '{' + cleaned_text.split('{', 1)[1]
            if not cleaned_text.strip().endswith('}'):
                cleaned_text = cleaned_text.rsplit('}', 1)[0] + '}'

            answer_data = json.loads(cleaned_text)
        except:
            print("JSON解析失败，退出程序")
            session.close()
            exit()

    # 先检查并确保学生和考试记录存在
    student_id = answer_data['student_id']
    exam_id = answer_data['exam_id']
    
    print(f"处理试卷ID: {exam_id}的学生作答")

    ensure_student_exists(session, student_id)
    if not ensure_exam_exists(session, exam_id):
        print("考试记录不存在，请先创建考试")
        session.close()
        exit()

    # 获取试卷中的所有题目，按照sort_order排序
    exam_questions = session.query(ExamQuestion).filter(
        ExamQuestion.exam_id == exam_id
    ).order_by(ExamQuestion.sort_order).all()
    
    # 创建学生答案中的题目ID到实际数据库题目ID的映射
    student_eq_id_to_actual_eq_id = {}
    for i, eq in enumerate(exam_questions, start=1):
        student_eq_id_to_actual_eq_id[i] = eq.eq_id
        print(f"学生题目ID映射: 学生题目ID={i} -> 实际exam_question_id={eq.eq_id}")
    
    # 更新学生答案中的exam_question_id为实际数据库中的ID
    for answer in answer_data['answers']:
        student_eq_id = answer['exam_question_id']
        if student_eq_id in student_eq_id_to_actual_eq_id:
            actual_eq_id = student_eq_id_to_actual_eq_id[student_eq_id]
            print(f"映射题目ID: 学生题目ID={student_eq_id} -> 实际exam_question_id={actual_eq_id}")
            answer['exam_question_id'] = actual_eq_id
        else:
            print(f"警告: 未找到学生题目ID={student_eq_id}的映射")

    # 处理不同题型的答案格式
    for answer in answer_data['answers']:
        # 标准化题型
        question_type = answer['question_type'].lower().strip()

        # 判断题处理
        if question_type in ['judgment', 'true_false']:
            if 'selected_option' in answer['answer_data']:
                if answer['answer_data']['selected_option'] == 'A':
                    answer['answer_data']['selected_option'] = 'T'
                elif answer['answer_data']['selected_option'] == 'B':
                    answer['answer_data']['selected_option'] = 'F'
            answer['question_type'] = 'judgment'  # 统一为judgment类型

        # 填空题处理
        elif question_type == 'fill_blank':
            if 'filled_answers' in answer['answer_data']:
                # 将填空题答案转换为字符串格式
                filled_answers = answer['answer_data']['filled_answers']
                if isinstance(filled_answers, list):
                    answer['answer_data']['content'] = '; '.join(filled_answers)
                else:
                    answer['answer_data']['content'] = str(filled_answers)
            answer['question_type'] = 'fill_blank'  # 保持fill_blank类型

        # 简答题处理
        elif question_type == 'short_answer':
            if 'content' not in answer['answer_data']:
                answer['answer_data']['content'] = ""
            answer['question_type'] = 'short_answer'  # 保持short_answer类型

        # 应用题处理
        elif question_type == 'application':
            if 'content' not in answer['answer_data']:
                answer['answer_data']['content'] = ""
            answer['question_type'] = 'application'  # 保持application类型

        # 处理可能的essay类型，转换为short_answer
        elif question_type == 'essay':
            if 'content' not in answer['answer_data']:
                answer['answer_data']['content'] = ""
            answer['question_type'] = 'short_answer'  # 转换为short_answer类型

        # 选择题处理
        elif question_type in ['single_choice', 'multi_choice']:
            if 'selected_option' not in answer['answer_data'] and 'selected_options' in answer['answer_data']:
                # 处理多选题格式
                answer['answer_data']['selected_option'] = ','.join(answer['answer_data']['selected_options'])

    # 存储答题记录
    record_id = save_student_answers(session, answer_data)
    print(f"作答记录已保存，记录ID：{record_id}")

except Exception as e:
    print(f"存储失败：{str(e)}")
    import traceback

    traceback.print_exc()  # 打印详细错误信息
    session.rollback()
    exit()

# 后续步骤需要检查record_id是否存在
if not record_id:
    print("未获取到有效记录ID")
    exit()

# 步骤2：自动批改客观题
try:
    grade_objective_questions(session, record_id)
    session.commit()  # 确保分数更新被保存
    print("客观题自动批改完成")

    # 查询当前总分
    record = session.get(StudentAnswerRecord, record_id)
    print(f"当前总分（客观题）：{record.total_score}")

except Exception as e:
    session.rollback()
    print(f"自动批改失败：{str(e)}")

# 步骤3：AI批改主观题
try:
    # 设置API密钥（实际使用时应从配置文件或环境变量获取）
    api_key = config['api_keys']['deepseek_api_key']

    # 确保主观题的question_category正确设置
    print("检查并更新主观题的类别...")
    subjective_types = ['short_answer', 'application', 'fill_blank']
    
    # 获取当前试卷的所有题目
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
            print(f"试卷题目映射: exam_question_id={eq.eq_id}, question_id={question.question_id}, 类型={question.question_type}")
    
    updated_count = 0
    for eq in exam_questions:
        question = session.query(Question).filter(
            and_(Question.question_id == eq.question_id)
        ).first()
        
        if question and question.question_type in subjective_types:
            if question.question_category != 'subjective':
                question.question_category = 'subjective'
                session.add(question)
                updated_count += 1
    
    if updated_count > 0:
        session.commit()
        print(f"已更新{updated_count}道主观题的类别")
    else:
        print("所有主观题类别已正确设置")

    # 调用AI批改
    ai_grade_subjective(session, record_id, api_key)
    print("主观题AI批改完成")

    # 查询当前总分（包含主观题）
    subjective_score = session.query(
        func.sum(QuestionAnswerDetail.final_score)
    ).join(
        ExamQuestion, and_(QuestionAnswerDetail.exam_question_id == ExamQuestion.eq_id)
    ).join(
        Question, and_(ExamQuestion.question_id == Question.question_id)
    ).filter(
        and_(
            QuestionAnswerDetail.record_id == record_id,
            Question.question_category == 'subjective'
        )
    ).scalar() or 0

    print(f"主观题得分：{subjective_score}")

except Exception as e:
    print(f"AI批改失败：{str(e)}")
    session.rollback()

# 步骤4：更新总分
try:
    # 重新计算总分
    total_score = session.query(
        func.sum(QuestionAnswerDetail.final_score)
    ).filter(
        QuestionAnswerDetail.record_id == record_id
    ).scalar() or 0

    # 更新记录状态
    record = session.get(StudentAnswerRecord, record_id)
    record.total_score = total_score
    record.status = 'graded'
    record.end_time = datetime.now()

    session.commit()
    print(f"最终总分已更新：{total_score}")

except Exception as e:
    print(f"更新总分失败：{str(e)}")
    session.rollback()

# 验证结果
print("\n最终作答记录详情：")
record = session.get(StudentAnswerRecord, record_id)
print(f"学生：{record.student_id} 试卷：{record.exam_id}")
print(f"状态：{record.status} 总分：{record.total_score}")

print("\n各题得分详情：")
# 修复查询，使用and_函数
details = session.query(
    QuestionAnswerDetail.exam_question_id,
    QuestionAnswerDetail.final_score,
    QuestionAnswerDetail.status,
    Question.question_type,
    Question.content,
    ExamQuestion.assigned_score
).join(
    ExamQuestion, and_(QuestionAnswerDetail.exam_question_id == ExamQuestion.eq_id)
).join(
    Question, and_(ExamQuestion.question_id == Question.question_id)
).filter(
    QuestionAnswerDetail.record_id == record_id
).all()

# 按题型分类统计
objective_score = 0
subjective_score = 0
objective_total = 0
subjective_total = 0

for detail in details:
    question_type_display = {
        'single_choice': '选择题',
        'multi_choice': '多选题',
        'judgment': '判断题',
        'fill_blank': '填空题',
        'short_answer': '简答题',
        'application': '应用计算题'
    }.get(detail.question_type, detail.question_type)

    # 确保final_score不为None
    final_score = detail.final_score or 0
    
    print(
        f"题目ID：{detail.exam_question_id} | 类型：{question_type_display} | 得分：{final_score}/{detail.assigned_score} | 状态：{detail.status}")
    print(f"题目内容：{detail.content[:50]}..." if len(detail.content) > 50 else f"题目内容：{detail.content}")
    print("-" * 50)

    # 统计客观题和主观题得分，处理None值
    if detail.question_type in ['single_choice', 'multi_choice', 'judgment']:
        objective_score += final_score
        objective_total += detail.assigned_score
    else:
        subjective_score += final_score
        subjective_total += detail.assigned_score

print("\n得分统计：")
print(
    f"客观题得分：{objective_score}/{objective_total} ({round(objective_score / objective_total * 100 if objective_total else 0, 2)}%)")
print(
    f"主观题得分：{subjective_score}/{subjective_total} ({round(subjective_score / subjective_total * 100 if subjective_total else 0, 2)}%)")
print(
    f"总分：{record.total_score}/{objective_total + subjective_total} ({round(record.total_score / (objective_total + subjective_total) * 100 if (objective_total + subjective_total) else 0, 2)}%)")
# 关闭会话
session.close()
