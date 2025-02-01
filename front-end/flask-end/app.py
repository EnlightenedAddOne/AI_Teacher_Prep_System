from flask import Flask, request, render_template, redirect, jsonify

from models import todo
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 解决跨域问题


@app.route('/todo', methods=['GET', 'POST'])
def todo_view():
    if request.method == 'GET':
        return jsonify(todo.todo_list)
    if request.method == 'POST':
        title = request.json.get('title', None)
        item = {
            'id': todo.count,
            'title': title,
            'done': False
        }
        todo.todo_list.append(item)
        return {'status': 'ok'}


@app.route('/todo/<int:_id>', methods=["PUT", "DELETE"])
def todo_item(_id):
    if request.method == 'PUT':
        for item in todo.todo_list:
            if item['id'] == _id:
                item['done'] = not item['done']
                return {'status': 'ok'}
        return {'status': 'error'}
    if request.method == 'DELETE':
        for item in todo.todo_list:
            if item['id'] == _id:
                todo.todo_list.remove(item)
                return {'status': 'ok'}
        return {'status': 'error'}


if __name__ == '__main__':
    app.run(debug=True)
