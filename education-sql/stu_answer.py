# 导入必要模块
from write_data import *
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:0128@localhost:3306/education') #root为用户名，0128为密码，education为数据库名
Session = sessionmaker(bind=engine)
session = Session()

text_answer='''
{
      "exam_id": 1,
      "student_id": "1",
      "answers": [
        {
          "exam_question_id": 1,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "A"
          }
        },
        {
          "exam_question_id": 2,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "C"
          }
        },
        {
          "exam_question_id": 3,
          "question_type": "single_choice",
          "answer_data": {
            "selected_option": "B"
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
            "selected_option": "C"
          }
        },
        {
          "exam_question_id": 6,
          "question_type": "fill_blank",
          "answer_data": {
            "filled_answers": ["3x^2 - 6x + 2"]
          }
        },
        {
          "exam_question_id": 7,
          "question_type": "fill_blank",
          "answer_data": {
            "filled_answers": ["-e^(-x)"]
          }
        },
        {
          "exam_question_id": 8,
          "question_type": "fill_blank",
          "answer_data": {
            "filled_answers": ["2x / (1 + x^2)"]
          }
        },
        {
          "exam_question_id": 9,
          "question_type": "true_false",
          "answer_data": {
            "selected_option": "F"
          }
        },
        {
          "exam_question_id": 10,
          "question_type": "true_false",
          "answer_data": {
            "selected_option": "T"
          }
        },
        {
          "exam_question_id": 11,
          "question_type": "true_false",
          "answer_data": {
            "selected_option": "T"
          }
        },
        {
          "exam_question_id": 12,
          "question_type": "true_false",
          "answer_data": {
            "selected_option": "T"
          }
        },
        {
          "exam_question_id": 13,
          "question_type": "essay",
          "answer_data": {
            "content": "f'(x) = 3x^2 - 6x + 2。令f'(x) = 0，解得x = 1 ± √(1/3)。通过二阶导数测试或单调性分析可得x = 1 - √(1/3)为极大值点，x = 1 + √(1/3)为极小值点。"
          }
        },
        {
          "exam_question_id": 14,
          "question_type": "essay",
          "answer_data": {
            "content": "f''(x) = (4x^2 - 2)e^(-x^2)。令f''(x) = 0，解得x = ±√(1/2)。通过符号变化分析可得x = ±√(1/2)为拐点。"
          }
        },
        {
          "exam_question_id": 15,
          "question_type": "application_calculation",
          "answer_data": {
            "content": "f'(x) = 3x^2 - 12x + 9。令f'(x) = 0，解得x = 1, 3。通过二阶导数测试或单调性分析可得x = 1为极大值点，极大值为5；x = 3为极小值点，极小值为1。单调增区间为(-∞, 1]和[3, +∞)，单调减区间为[1, 3]。"
          }
        },
        {
          "exam_question_id": 16,
          "question_type": "application_calculation",
          "answer_data": {
            "content": "f''(x) = (-2x^2 + 2) / (x^2 + 1)^2。令f''(x) = 0，解得x = ±1。通过符号变化分析可得x = -1和x = 1为拐点。当x < -1或x > 1时，f''(x) < 0，函数为凸；当-1 < x < 1时，f''(x) > 0，函数为凹。"
          }
        }
      ]
}

'''

# 步骤1：存储作答数据
record_id = None  # 初始化变量

try:
    answer_data = json.loads(text_answer)
    record_id = save_student_answers(session, answer_data)
    print(f"作答记录已保存，记录ID：{record_id}")

except Exception as e:
    print(f"存储失败：{str(e)}")
    session.rollback()
    exit()  # 存储失败时直接退出

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

# 步骤3：人工批改主观题
try:
    # 获取需要人工批改的题目
    subjective_answers = session.query(QuestionAnswerDetail).join(ExamQuestion).join(Question).filter(
        QuestionAnswerDetail.record_id == record_id,
        Question.question_category == 'subjective'
    ).all()

    # 模拟教师批改
    for answer in subjective_answers:
        # 根据exam_question_id获取题目分值
        exam_question = session.get(ExamQuestion, answer.exam_question_id)
        
        # 人工评分逻辑（这里简化为直接赋值）
        answer.teacher_score = 8.5  # 实际应根据评分标准计算
        answer.final_score = answer.teacher_score
        answer.status = 'manually_graded'
        answer.feedback = "解答过程完整，但缺少图示说明"
        
        session.add(answer)

    session.commit()
    print("主观题人工批改完成")

except Exception as e:
    print(f"人工批改失败：{str(e)}")
    session.rollback()

# 步骤4：更新总分
try:
    # 重新计算总分
    total_score = session.query(
        func.sum(QuestionAnswerDetail.final_score)
    ).filter_by(record_id=record_id).scalar()

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
details = session.query(
    QuestionAnswerDetail.exam_question_id,
    QuestionAnswerDetail.final_score,
    QuestionAnswerDetail.status
).filter_by(record_id=record_id).all()

for detail in details:
    print(f"题目ID：{detail.exam_question_id} | 得分：{detail.final_score} | 状态：{detail.status}")

# 关闭会话
session.close()













