# 测试文件
from teaching_design import generate_teaching_design
from exercise_generation import generate_exercises
from multimedia_generation import generate_multimedia
from student_analysis import analyze_student_performance
from config import config


def main():
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
        "short_answer_score": 15, "short_answer_count": 2,
        "application_score": 20, "application_count": 1
    }
    degree = input("难易程度：")  # 简单、一般、困难
    exercises, answers_and_explanations = generate_exercises(subject, topic, degree, exercise_config, api_key)
    print("\n练习题:")
    print(exercises)
    print("\n答案和解析:")
    print(answers_and_explanations)

    # # 多媒体资源生成
    # content_points = "示例内容要点"
    # multimedia = generate_multimedia(subject, topic, content_points, api_key)
    # print("\n多媒体资源描述：")
    # print(multimedia)
    #
    # # 学情分析
    # student_records = [{"score": 50}, {"score": 80}]  # 示例数据
    # recommendations = analyze_student_performance(student_records)
    # print("\n学情分析与个性化建议：")
    # print(recommendations)


if __name__ == "__main__":
    main()
