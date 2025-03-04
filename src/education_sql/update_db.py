from sqlalchemy import create_engine, text
from src.configs import config

# 创建数据库引擎
db_config = config['database']
engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

def update_database():
    """更新数据库表结构，添加新字段"""
    try:
        with engine.connect() as conn:
            # 1. 检查并添加 subject_name 字段到 exams 表
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.columns "
                "WHERE table_name = 'exams' AND column_name = 'subject_name'"
            ))
            if result.scalar() == 0:
                conn.execute(text(
                    "ALTER TABLE exams ADD COLUMN subject_name VARCHAR(50)"
                ))
                
                # 更新现有记录的subject_name
                conn.execute(text(
                    "UPDATE exams e JOIN subjects s ON e.subject_id = s.subject_id "
                    "SET e.subject_name = s.subject_name"
                ))
                print("已添加 subject_name 字段到 exams 表并更新现有记录")
            else:
                print("exams 表中 subject_name 字段已存在")
            
            # 2. 检查并添加 question_category 字段到 questions 表
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.columns "
                "WHERE table_name = 'questions' AND column_name = 'question_category'"
            ))
            if result.scalar() == 0:
                conn.execute(text(
                    "ALTER TABLE questions ADD COLUMN question_category VARCHAR(20) DEFAULT 'objective'"
                ))
                
                # 更新现有记录的question_category
                conn.execute(text(
                    "UPDATE questions SET question_category = "
                    "CASE WHEN question_type IN ('single_choice', 'multi_choice', 'judgment') "
                    "THEN 'objective' ELSE 'subjective' END"
                ))
                print("已添加 question_category 字段到 questions 表并更新现有记录")
            else:
                print("questions 表中 question_category 字段已存在")
            
            # 3. 更新 student_answer_records 表的 status 字段，支持 'pending_manual' 状态
            try:
                conn.execute(text(
                    "ALTER TABLE student_answer_records MODIFY COLUMN status "
                    "ENUM('in_progress', 'submitted', 'graded', 'pending_manual') DEFAULT 'in_progress'"
                ))
                print("已更新 student_answer_records 表的 status 字段，支持 'pending_manual' 状态")
            except Exception as e:
                print(f"更新 status 字段失败，可能已经包含所需状态：{str(e)}")
            
            conn.commit()
            print("数据库更新成功")
    except Exception as e:
        print(f"数据库更新失败：{str(e)}")

if __name__ == "__main__":
    update_database() 