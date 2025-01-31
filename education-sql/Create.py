from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:0128@localhost:3306/education') #root为用户名，0128为密码，education为数据库名
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Subject(Base):
    """学科表"""
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String(50), unique=True, nullable=False)
    parent_id = Column(Integer, default=0)

    # 关系定义
    exams = relationship("Exam", back_populates="subject")
    questions = relationship("Question", back_populates="subject")


class Exam(Base):
    """试卷表"""
    __tablename__ = 'exams'
    exam_id = Column(Integer, primary_key=True)
    exam_name = Column(String(200), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    total_score = Column(Float, nullable=False)
    time_limit = Column(Integer)  # 分钟数
    version = Column(String(20), default='v1.0')

    # 关系定义
    subject = relationship("Subject", back_populates="exams")
    exam_questions = relationship("ExamQuestion", back_populates="exam")
    subject_name = Column(String(50))  # 冗余存储方便查询

class Question(Base):
    """题目表"""
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    question_type = Column(Enum('single_choice', 'multi_choice', 'judgment', 'fill_blank', 'essay'), nullable=False)
    content = Column(Text, nullable=False)
    explanation = Column(Text)
    difficulty = Column(Float, default=0.5)  # 0-1难度系数
    topic = Column(String(50))  # 所属专题
    meta_data = Column(JSON)  # 存储难度、知识点等扩展信息

    # 关系定义
    subject = relationship("Subject", back_populates="questions")
    # options = relationship("QuestionOption", back_populates="question")
    exam_links = relationship("ExamQuestion", back_populates="question")
    # knowledge_points = relationship("KnowledgePoint", secondary="question_points")
    original_type = Column(String(20))  # 存储原始题型名称（如"选择题"

    options = relationship('QuestionOption', back_populates='question', cascade='all, delete-orphan')
    knowledge_points = relationship('KnowledgePoint', back_populates='question', cascade='all, delete-orphan')


class ExamQuestion(Base):
    """试卷-题目关系表"""
    __tablename__ = 'exam_questions'
    eq_id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exams.exam_id',ondelete='CASCADE'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.question_id',ondelete='CASCADE'), nullable=False)
    display_number = Column(String(20))  # 显示编号如"一、"
    assigned_score = Column(Float, nullable=False)  # 本题分值
    sort_order = Column(Integer, default=0)  # 排序序号

    # 关系定义
    exam = relationship("Exam", back_populates="exam_questions")
    question = relationship("Question", back_populates="exam_links")



class QuestionOption(Base):
    """题目选项表"""
    __tablename__ = 'question_options'
    option_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    option_key = Column(String(10), nullable=False)  # 选项标识（A/B/C等）
    option_content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    # 关系定义
    question = relationship("Question", back_populates="options")


class KnowledgePoint(Base):
    """知识点表"""
    __tablename__ = 'knowledge_graph'
    point_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)  # 添加外键关联到题目
    point_name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    parent_point = Column(Integer, default=0)
    level = Column(Integer, default=1)
    # 关系定义
    question = relationship("Question", back_populates="knowledge_points")

# class QuestionPoint(Base):
#     """题目-知识点关联表"""
#     __tablename__ = 'question_points'
#     qp_id = Column(Integer, primary_key=True)
#     question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
#     point_id = Column(Integer, ForeignKey('knowledge_graph.point_id'), nullable=False)


# 创建所有表（仅首次运行需要）
Base.metadata.create_all(engine)
