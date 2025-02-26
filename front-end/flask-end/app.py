from flask import Flask, request, jsonify
from flask_cors import CORS
from todo_sql.sql_function import ToDo, write_data, Session, turn_state, delete_task_by_id, clear_completed_tasks

session = Session() # 获取数据库链接

app = Flask(__name__)

# ================== 核心配置 ==================
# 增强CORS配置
CORS(app, 
    resources={
        r"/todo*": {
            "origins": ["http://localhost:5173", "https://*.ngrok-free.app"],
            "allow_headers": ["ngrok-skip-browser-warning", "Content-Type"],
            "expose_headers": ["X-Custom-Header"],
            "supports_credentials": True
        }
    }
)

# ================== 安全头配置 ==================
@app.after_request
def set_security_headers(response):
    """设置安全响应头"""
    response.headers.extend({
        'X-Content-Type-Options': 'nosniff',
        'Content-Security-Policy': "default-src 'self'",
        'X-Frame-Options': 'DENY',
        'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload'
    })
    return response

# ================== 全局错误处理 ==================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "资源未找到",
        "status": 404,
        "path": request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "服务器内部错误",
        "status": 500,
        "request_id": request.headers.get('X-Request-ID', '')
    }), 500

# ================== 请求预处理 ==================
@app.before_request
def handle_ngrok_headers():
    """处理ngrok特殊请求头"""
    # 转换ngrok的协议头
    if 'X-Forwarded-Proto' in request.headers:
        request.environ['wsgi.url_scheme'] = request.headers['X-Forwarded-Proto']
    
    # 记录自定义头日志
    if 'ngrok-skip-browser-warning' in request.headers:
        app.logger.debug('接收到ngrok跳过警告头')

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

# ================== 启动配置 ==================
if __name__ == '__main__':
    # 生产环境应关闭debug
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        ssl_context='adhoc'  # 启用HTTPS支持
    )
