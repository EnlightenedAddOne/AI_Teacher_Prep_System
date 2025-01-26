# 学情分析模块
def analyze_student_performance(student_records):
    # 示例：分析学生历史学习记录，生成个性化建议
    recommendations = []
    for record in student_records:
        if record["score"] < 60:
            recommendations.append("需要加强基础知识复习")
        else:
            recommendations.append("可以尝试更高难度的学习内容")
    return recommendations
