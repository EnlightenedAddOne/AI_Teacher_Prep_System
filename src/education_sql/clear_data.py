from Create import Session, Base, engine
from sqlalchemy import text, inspect


def clear_all_tables():
    """清空所有表的数据"""
    session = Session()
    try:
        # 获取数据库中实际存在的表
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        # 禁用外键约束检查
        session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))

        # 按顺序清空表（只清空存在的表）
        tables_to_clear = [
            'exam_questions',  # 先清空关联表
            'question_options',  # 清空选项表
            'questions',  # 清空题目表
            'exams',  # 清空试卷表
            'subjects',  # 最后清空学科表
            'knowledge_graph'  # 知识图谱表
        ]
        
        for table in tables_to_clear:
            if table in existing_tables:
                session.execute(text(f'TRUNCATE TABLE {table}'))
                print(f"已清空表 {table}")
            else:
                print(f"表 {table} 不存在，跳过")

        # 重新启用外键约束检查
        session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))

        session.commit()
        print("所有表数据已清空")

    except Exception as e:
        session.rollback()
        print(f"清空表时出错: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    clear_all_tables()
