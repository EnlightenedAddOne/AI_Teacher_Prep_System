from flask import Flask, request, jsonify
from flask_cors import CORS
from todo_sql.sql_function import ToDo, write_data, Session, turn_state, delete_task_by_id, clear_completed_tasks

session = Session() # 获取数据库链接

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 解决跨域问题


@app.route('/todo', methods=['GET', 'POST'])
def todo_view():
    key = request.args.get('key', 'all')  # 获取查询参数 'key'，默认为 'all'
    if request.method == 'GET':
        if key == 'all':
            tasks = ToDo.all_tasks(session)  # 假设这个方法返回所有任务
        elif key == 'undone':
            tasks = ToDo.undone_list(session)  # 假设这个方法返回未完成的任务
        elif key == 'done':
            tasks = ToDo.done_list(session)  # 假设这个方法返回已完成的任务
        else:
            return jsonify({'error': 'Invalid key parameter'}), 400  # 错误的参数返回 400 错误

        return jsonify(tasks)
    # if request.method == 'POST':
    #     title = request.json.get('title', None)
    #     write_data(session,title)
    #     return {'status': 'ok'}

@app.route('/add_todo', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.json.get('title', None)
        write_data(session,title)
        return {'status': 'ok'}

@app.route('/todo/clear_done', methods=['DELETE'])
def clear_completed_tasks_view():
    try:
        # 调用清除已完成任务的方法
        result = clear_completed_tasks(session)
        if result:
            return jsonify({'status': 'ok'}), 200
        else:
            return jsonify({'error': 'Failed to clear completed tasks'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todo/<int:_id>', methods=["PUT", "DELETE"])
def todo_item(_id):
    '''增加任务'''
    if request.method == 'PUT':
        status=turn_state(session,_id)
        if status==True:
            return {'status': 'ok'}
        else:
            return {'status': 'error'}
    if request.method == 'DELETE':
        '''删除任务'''
        status=delete_task_by_id(session,_id)
        if status==True:
            return {'status': 'ok'}
        else:
            return {'status': 'error'}


if __name__ == '__main__':
    app.run(debug=True)
