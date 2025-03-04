from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, Boolean, ForeignKey, Enum, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from src.configs import config  # 直接导入，因为现在是一个包
from datetime import datetime
# 创建数据库引擎
db_config = config['database']
engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Subject(Base):
    """学科表"""
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(50), unique=True, nullable=False)
    parent_id = Column(Integer, default=0)

    # 关系定义
    exams = relationship("Exam", back_populates="subject")
    questions = relationship("Question", back_populates="subject")
    knowledge_points = relationship("KnowledgePoint", back_populates="subject")


class Exam(Base):
    """试卷表"""
    __tablename__ = 'exams'
    exam_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    subject_name = Column(String(50))  # 添加学科名称字段，方便查询
    total_score = Column(Integer, nullable=False)
    time_limit = Column(Integer, nullable=False)  # 考试时长(分钟)
    version = Column(String(20), default='v1.0')

    # 关系定义
    subject = relationship("Subject", back_populates="exams")
    exam_questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan")


class Question(Base):
    """题目表"""
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    question_type = Column(String(20), nullable=False)
    original_type = Column(String(20))
    content = Column(String(1000), nullable=False)
    explanation = Column(String(1000))
    difficulty = Column(Float, default=0.5)
    topic = Column(String(50))
    meta_data = Column(JSON)
    question_category = Column(String(20), default='objective')  # 题目类别：客观题/主观题

    # 关系定义
    subject = relationship("Subject", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    exam_questions = relationship("ExamQuestion", back_populates="question")
    knowledge_points = relationship("KnowledgePoint", back_populates="question")


class ExamQuestion(Base):
    """试卷-题目关系表"""
    __tablename__ = 'exam_questions'
    eq_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey('exams.exam_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    display_number = Column(String(10))  # 题号显示(一、二、三等)
    assigned_score = Column(Integer, nullable=False)  # 分值
    sort_order = Column(Integer, default=0)  # 排序

    # 关系定义
    exam = relationship("Exam", back_populates="exam_questions")
    question = relationship("Question", back_populates="exam_questions")


class QuestionOption(Base):
    """题目选项表"""
    __tablename__ = 'question_options'
    option_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    option_key = Column(String(10), nullable=False)  # A, B, C, D 或 answer
    option_content = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    # 关系定义
    question = relationship("Question", back_populates="options")


class KnowledgePoint(Base):
    """知识点表"""
    __tablename__ = 'knowledge_graph'
    point_id = Column(Integer, primary_key=True, autoincrement=True)
    point_name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    parent_point = Column(Integer, default=0)  # 父知识点ID
    level = Column(Integer, default=1)  # 知识点层级

    # 关系定义
    subject = relationship("Subject", back_populates="knowledge_points")
    question = relationship("Question", back_populates="knowledge_points")


class Student(Base):
    """学生表"""
    __tablename__ = 'students'
    id = Column(String(20), primary_key=True, comment='学号')
    name = Column(String(50), nullable=False, comment='姓名')
    class_name = Column(String(50), comment='班级')
    # ... 其他字段 ...
    answer_records = relationship("StudentAnswerRecord", backref="student")


class StudentAnswerRecord(Base):
    """学生答卷记录表"""
    __tablename__ = 'student_answer_records'
    id = Column(Integer, primary_key=True)
    student_id = Column(String(20), ForeignKey('students.id'), index=True)
    exam_id = Column(Integer, ForeignKey('exams.exam_id'), index=True)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime)
    total_score = Column(Float)
    status = Column(Enum('in_progress', 'submitted', 'graded', 'pending_manual'), default='in_progress')
    answer_details = relationship("QuestionAnswerDetail", backref="answer_record")


class QuestionAnswerDetail(Base):
    """题目作答详情表"""
    __tablename__ = 'question_answer_details'
    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey('student_answer_records.id'), index=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), index=True)
    exam_question_id = Column(Integer, ForeignKey('exam_questions.eq_id'), comment='原试卷题目关联')
    student_answer = Column(Text, comment='学生作答内容')
    auto_score = Column(Float, comment='系统自动评分')
    teacher_score = Column(Float, comment='教师手动评分')
    final_score = Column(Float, comment='最终得分')
    status = Column(Enum('pending', 'auto_graded', 'manually_graded'), default='pending')
    feedback = Column(Text, comment='教师评语')
    exam_question = relationship("ExamQuestion", backref="answer_details")


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
