from flask import Flask, request, jsonify


from flask_cors import CORS

from todo_sql.sql_function import ToDo, write_data, Session, turn_state, delete_task_by_id


session = Session()

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 解决跨域问题


@app.route('/todo', methods=['GET', 'POST'])
def todo_view():
    if request.method == 'GET':
        return jsonify(ToDo.all_tasks(session))
    if request.method == 'POST':
        title = request.json.get('title', None)
        write_data(session,title)
        return {'status': 'ok'}


@app.route('/todo/<int:_id>', methods=["PUT", "DELETE"])
def todo_item(_id):
    if request.method == 'PUT':
        status=turn_state(session,_id)
        if status==True:
            return {'status': 'ok'}
        else:
            return {'status': 'error'}
    if request.method == 'DELETE':
        status=delete_task_by_id(session,_id)
        if status==True:
            return {'status': 'ok'}
        else:
            return {'status': 'error'}


if __name__ == '__main__':
    app.run(debug=True)
