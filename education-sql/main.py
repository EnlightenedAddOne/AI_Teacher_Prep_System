from write_data import *
from read import *
from updatedelete import *
import json

test_questions = '''
    {
    "questions": [
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 1,
            "content": "设函数f(x) = x^3 - 3x + 2，求f'(x)的值为：",
            "options": [
                {
                    "key": "A",
                    "value": "3x^2 - 3"
                },
                {
                    "key": "B",
                    "value": "3x^2 + 3"
                },
                {
                    "key": "C",
                    "value": "3x^2 - 6x"
                },
                {
                    "key": "D",
                    "value": "3x^2 - 6"
                }
            ],
            "correct_answer": "A",
            "explanation": "根据导数的定义和幂函数的求导法则，f'(x) = 3x^2 - 3。",
            "knowledge_points": ["导数", "幂函数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 2,
            "content": "若函数f(x) = ln(x)，则f'(e)的值为：",
            "options": [
                {
                    "key": "A",
                    "value": "1/e"
                },
                {
                    "key": "B",
                    "value": "e"
                },
                {
                    "key": "C",
                    "value": "1"
                },
                {
                    "key": "D",
                    "value": "-1/e"
                }
            ],
            "correct_answer": "C",
            "explanation": "根据对数函数的导数公式，f'(x) = 1/x。因此，f'(e) = 1/e = 1。",
            "knowledge_points": ["对数函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 3,
            "content": "设函数f(x) = sin(2x)，则f'(π/4)的值为：",
            "options": [
                {
                    "key": "A",
                    "value": "0"
                },
                {
                    "key": "B",
                    "value": "2"
                },
                {
                    "key": "C",
                    "value": "-2"
                },
                {
                    "key": "D",
                    "value": "1"
                }
            ],
            "correct_answer": "B",
            "explanation": "根据三角函数的导数公式，f'(x) = 2cos(2x)。因此，f'(π/4) = 2cos(π/2) = 2。",
            "knowledge_points": ["三角函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 4,
            "content": "设函数f(x) = e^(2x)，则f''(0)的值为：",
            "options": [
                {
                    "key": "A",
                    "value": "2"
                },
                {
                    "key": "B",
                    "value": "4"
                },
                {
                    "key": "C",
                    "value": "8"
                },
                {
                    "key": "D",
                    "value": "16"
                }
            ],
            "correct_answer": "B",
            "explanation": "根据指数函数的导数公式，f'(x) = 2e^(2x)，f''(x) = 4e^(2x)。因此，f''(0) = 4e^0 = 4。",
            "knowledge_points": ["指数函数", "二阶导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "一",
            "type": "选择题",
            "score": 2,
            "id": 5,
            "content": "设函数f(x) = (x^2 + 1)/(x - 1)，则f'(2)的值为：",
            "options": [
                {
                    "key": "A",
                    "value": "3"
                },
                {
                    "key": "B",
                    "value": "4"
                },
                {
                    "key": "C",
                    "value": "5"
                },
                {
                    "key": "D",
                    "value": "6"
                }
            ],
            "correct_answer": "C",
            "explanation": "使用商规则求导，f'(x) = ((2x)(x-1) - (x^2+1)) / (x-1)^2。因此，f'(2) = (4*1 - 5) / 1 = 3。",
            "knowledge_points": ["商规则", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "二",
            "type": "填空题",
            "score": 3,
            "id": 6,
            "content": "设函数f(x) = x^3 - 3x^2 + 2x，则f'(x) = ________。",
            "options": [],
            "correct_answer": "3x^2 - 6x + 2",
            "explanation": "根据多项式求导法则，f'(x) = 3x^2 - 6x + 2。",
            "knowledge_points": ["多项式", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "二",
            "type": "填空题",
            "score": 3,
            "id": 7,
            "content": "设函数f(x) = e^(-x)，则f'(x) = ________。",
            "options": [],
            "correct_answer": "-e^(-x)",
            "explanation": "根据指数函数的导数公式，f'(x) = -e^(-x)。",
            "knowledge_points": ["指数函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "二",
            "type": "填空题",
            "score": 3,
            "id": 8,
            "content": "设函数f(x) = ln(1 + x^2)，则f'(x) = ________。",
            "options": [],
            "correct_answer": "2x / (1 + x^2)",
            "explanation": "根据链式法则和对数函数的导数公式，f'(x) = 2x / (1 + x^2)。",
            "knowledge_points": ["链式法则", "对数函数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 9,
            "content": "若函数f(x) = |x|，则f'(0)存在。",
            "options": [
                {
                    "key": "T",
                    "value": "正确"
                },
                {
                    "key": "F",
                    "value": "错误"
                }
            ],
            "correct_answer": "F",
            "explanation": "绝对值函数在x=0处不可导，因为左右导数不相等。",
            "knowledge_points": ["绝对值函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 10,
            "content": "若函数f(x) = e^x，则f'(x) = e^x。",
            "options": [
                {
                    "key": "T",
                    "value": "正确"
                },
                {
                    "key": "F",
                    "value": "错误"
                }
            ],
            "correct_answer": "T",
            "explanation": "根据指数函数的导数公式，f'(x) = e^x。",
            "knowledge_points": ["指数函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 11,
            "content": "若函数f(x) = sin(x)，则f'(x) = cos(x)。",
            "options": [
                {
                    "key": "T",
                    "value": "正确"
                },
                {
                    "key": "F",
                    "value": "错误"
                }
            ],
            "correct_answer": "T",
            "explanation": "根据三角函数的导数公式，f'(x) = cos(x)。",
            "knowledge_points": ["三角函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "三",
            "type": "判断题",
            "score": 1,
            "id": 12,
            "content": "若函数f(x) = ln(x)，则f'(x) = 1/x。",
            "options": [
                {
                    "key": "T",
                    "value": "正确"
                },
                {
                    "key": "F",
                    "value": "错误"
                }
            ],
            "correct_answer": "T",
            "explanation": "根据对数函数的导数公式，f'(x) = 1/x。",
            "knowledge_points": ["对数函数", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "四",
            "type": "简答题",
            "score": 5,
            "id": 13,
            "content": "设函数f(x) = x^3 - 3x^2 + 2x，求f(x)的极值点，并判断其是极大值还是极小值。",
            "options": [],
            "correct_answer": "f'(x) = 3x^2 - 6x + 2。令f'(x) = 0，解得x = 1 ± √(1/3)。通过二阶导数测试或单调性分析可得x = 1 - √(1/3)为极大值点，x = 1 + √(1/3)为极小值点。",
            "explanation": "首先求导得到f'(x) = 3x^2 - 6x + 2。然后令f'(x) = 0解出临界点。再通过二阶导数或单调性分析确定极值类型。",
            "knowledge_points": ["极值", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "四",
            "type": "简答题",
            "score": 5,
            "id": 14,
            "content": "设函数f(x) = e^(-x^2)，求f(x)的拐点。",
            "options": [],
            "correct_answer": "f''(x) = (4x^2 - 2)e^(-x^2)。令f''(x) = 0，解得x = ±√(1/2)。通过符号变化分析可得x = ±√(1/2)为拐点。",
            "explanation": "首先求二阶导数f''(x) = (4x^2 - 2)e^(-x^2)。然后令f''(x) = 0解出拐点位置。再通过符号变化确认拐点。",
            "knowledge_points": ["拐点", "二阶导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "五",
            "type": "应用计算题",
            "score": 10,
            "id": 15,
            "content": "设函数f(x) = x^3 - 6x^2 + 9x + 1，求该函数的单调区间、极值点及其对应的极值。",
            "options": [],
            "correct_answer": "f'(x) = 3x^2 - 12x + 9。令f'(x) = 0，解得x = 1, 3。通过二阶导数测试或单调性分析可得x = 1为极大值点，极大值为5；x = 3为极小值点，极小值为1。单调增区间为(-∞, 1]和[3, +∞)，单调减区间为[1, 3]。",
            "explanation": "首先求导得到f'(x) = 3x^2 - 12x + 9。然后令f'(x) = 0解出临界点。再通过二阶导数或单调性分析确定极值类型及单调区间。",
            "knowledge_points": ["单调性", "极值", "导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        },
        {
            "number": "五",
            "type": "应用计算题",
            "score": 10,
            "id": 16,
            "content": "设函数f(x) = ln(x^2 + 1)，求该函数的凹凸性和拐点。",
            "options": [],
            "correct_answer": "f''(x) = (-2x^2 + 2) / (x^2 + 1)^2。令f''(x) = 0，解得x = ±1。通过符号变化分析可得x = -1和x = 1为拐点。当x < -1或x > 1时，f''(x) < 0，函数为凸；当-1 < x < 1时，f''(x) > 0，函数为凹。",
            "explanation": "首先求二阶导数f''(x) = (-2x^2 + 2) / (x^2 + 1)^2。然后令f''(x) = 0解出拐点位置。再通过符号变化确认凹凸性和拐点。",
            "knowledge_points": ["凹凸性", "拐点", "二阶导数"],
            "subject": "数学",
            "topic": "函数",
            "degree": "困难"
        }
    ],
    "test_info": {
        "total_score": 53,
        "time_limit": 45
    }
}
    '''


def main():
    session = Session()

    # delete_question(session, 1)
    # delete_question(session,2)
    # delete_exam_with_others(session,1)

    # # 存入数据库后测试打印
    # exported = export_exam_to_json(session, 1)
    # print(type(exported))
    # print(exported)
    # verify_exam_import(session,1)

    # 将JSON字符串转换为Python字典
    data_dict = json.loads(test_questions)
    # 执行导入
    exam_id = import_exam_paper(session, data_dict,'测试试卷')

    # 导出试卷（假设已知试卷ID为1）
    exam_data = export_exam_to_json(session, exam_id)
    print(exam_data)

    #
    # if exam_id:
    #     # 验证导入结果
    #     verify_exam_import(session, exam_id)
    #     exported = export_exam_to_json(session, exam_id)
    #     print(exported)




    session.close()


if __name__ == "__main__":
    main()