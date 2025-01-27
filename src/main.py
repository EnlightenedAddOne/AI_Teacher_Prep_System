# 测试文件
from teaching_design import generate_teaching_design
from exercise_generation import generate_exercises
from multimedia_generation import generate_multimedia
from student_analysis import analyze_student_performance
from config import config
from fpdf import FPDF
import os

class PDF(FPDF):
    # 定义PDF类的构造函数，继承自FPDF类
    def header(self):
        # 定义页眉函数
        self.set_font("SimSun", 'B', 12)
        # 设置字体为SimSun，加粗，字号为12
        self.cell(0, 10, '教学设计与练习题', 0, 1, 'C')

        # 创建一个单元格，宽度为0（自动适应页面宽度），高度为10，内容为'教学设计与练习题'，边框为0，换行，居中对齐

    def chapter_title(self, title):
        # 定义章节标题函数，参数为标题文本
        self.set_font("SimSun", 'B', 12)
        # 设置字体为SimSun，加粗，字号为12
        self.cell(0, 10, title, 0, 1, 'L')
        # 创建一个单元格，宽度为0（自动适应页面宽度），高度为10，内容为传入的标题，边框为0，换行，左对齐
        self.ln(10)

        # 添加10毫米的行间距

    def chapter_body(self, body):
        # 定义章节正文函数，参数为正文文本
        self.set_font("SimSun", '', 12)
        # 设置字体为SimSun，常规，字号为12
        self.multi_cell(0, 10, body)
        # 创建一个多行单元格，宽度为0（自动适应页面宽度），高度为10，内容为传入的正文，自动换行
        self.ln()


def save_to_pdf(teaching_design, exercises, answers_and_explanations, filename="output.pdf"):
    # 创建一个PDF对象
    pdf = PDF()
    font_path = os.path.join(os.path.dirname(__file__), 'ziti', 'simsun.ttc')
    if not os.path.exists(font_path):
        raise RuntimeError(f"TTF Font file not found: {font_path}")

    pdf.add_font('SimSun', '', font_path, uni=True)
    # 添加一个新的页面到PDF文档
    pdf.add_page()

    pdf.set_font('SimSun', '', 12)

    # 添加教学设计章节的标题
    pdf.chapter_title("教学设计：")
    # 添加教学设计章节的内容
    pdf.chapter_body(teaching_design)

    # 添加一个新的页面到PDF文档
    pdf.add_page()
    # 添加练习题章节的标题
    pdf.chapter_title("练习题：")
    # 添加练习题章节的内容
    pdf.chapter_body(exercises)

    # 添加一个新的页面到PDF文档
    pdf.add_page()
    # 添加答案和解析章节的标题
    pdf.chapter_title("答案和解析：")
    # 添加答案和解析章节的内容
    pdf.chapter_body(answers_and_explanations)

    # 将PDF文档输出到指定的文件，'F'表示写入文件
    pdf.output(filename, 'F')


def main():
    try:
        api_key = config['api_keys']['tongyi_api_key']
        # 用户输入
        subject = input("学科名称：")
        topic = input("课程主题：")
        goals = input("教学目标：")
        duration = input("课程时长：")
        grade = input("学生年级：")

        # 教学设计
        teaching_design = generate_teaching_design(subject, topic, goals, duration, grade, api_key)
        print("\n教学设计：")
        print(teaching_design)

        # 练习题配置
        exercise_config = {
            "choice_score": 5, "choice_count": 3,
            "fill_score": 10, "fill_count": 2,
            # "judge_score": 5, "judge_count": 3,
            # "short_answer_score": 15, "short_answer_count": 2,
            "application_score": 20, "application_count": 1
        }
        degree = input("难易程度：")  # 简单、一般、困难
        exercises, answers_and_explanations = generate_exercises(subject, topic, degree, exercise_config, api_key)
        print("\n练习题:")
        print(exercises)
        print("\n答案和解析:")
        print(answers_and_explanations)

        # 保存为 PDF
        save_to_pdf(teaching_design, exercises, answers_and_explanations)
        print("\n输出已保存为 output.pdf")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
