from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# 初始化数据库连接:
# front-end/sql/todo-sql.sql

# 更改为自己目录下的 todo-sql.sql数据库 路径
sql_path=r'D:/PROJECT/Python/test01/front-end/flask-end/todo_sql/todo-sql.sql'
engine = create_engine(f'sqlite:///{sql_path}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Todo_List(Base):

    __tablename__ = 'todo_list'
    id = Column(Integer, primary_key=True)  # 使用 'id' 作为字段名
    title = Column(String(50), nullable=False)
    done = Column(Boolean, default=False)  # 使用 Boolean 类型，并设置默认值为 False

    # # 关系定义
    # exams = relationship("Exam", back_populates="subject")
    # questions = relationship("Question", back_populates="subject")



# 创建所有表（仅首次运行需要）
Base.metadata.create_all(engine)