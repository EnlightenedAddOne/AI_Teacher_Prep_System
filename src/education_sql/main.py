from sqlalchemy.orm import Session
from src.education_sql.read import verify_question_types
from src.education_sql.write_data import fix_question_types


def main():
    session = Session()

    try:
        # 验证当前题型
        print("当前数据库中的题型：")
        verify_question_types(session)

        # 修复题型
        print("\n开始修复题型...")
        fix_question_types(session)

        # 再次验证
        print("\n修复后的题型：")
        verify_question_types(session)

        # ... 其他代码 ...

    finally:
        session.close()
