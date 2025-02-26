<script setup>
    import {onMounted, ref, reactive, computed} from 'vue';

    const Local_url = 'http://127.0.0.1:5000/todo';       // 本机运行前后端的url
    const Server_url = 'http://192.168.63.215:5000/todo'; // 同一局域网下的url

    const baseUrl = ref(Server_url); // 直接使用服务器地址

    let url = Server_url;

    let todos = ref([]);
    let form = reactive({
        title: '',
        done: false,
    });

    const undone_count = computed(() => {
    return todos.value.filter(todo => !todo.done).length;
    });

    let currentStatus = ref('all'); // 默认为 'all'

    // 切换状态并加载数据
    const switchStatus = (status) => {
        currentStatus.value = status;
        fetchData();
    };

    // 1. 请求服务器加载数据
    const fetchData = () => {
        // 避免使用同名变量
        const requestUrl = `${baseUrl.value}?key=${currentStatus.value}`;
        console.log('请求URL:', requestUrl); // 添加调试输出
        
        fetch(requestUrl)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP错误: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log('获取数据:', data);
                todos.value = data; // 确保数据正确赋值给todos
            })
            .catch(error => {
                console.error('获取数据失败:', error);
            });
    };


    // 2. 切换任务的完成状态
    const change_todo_status = (item) => {
        console.log(JSON.stringify(item));
        fetch(`${url}/${item.id}`,
            {
                method: 'put',
                body: JSON.stringify(item),
                headers: {
                    'Content-Type': 'application/json',
                },
            },
        ).then(function (response) {
            return response.json();
        }).then(function (data) {
            console.log(data);
        });
    };
    // 3. 添加任务
    const add_todo = () => {
        // 从baseUrl中移除'/todo'路径，因为我们需要访问'/add_todo'
        const apiBase = baseUrl.value.substring(0, baseUrl.value.lastIndexOf('/'));
        const addUrl = `${apiBase}/add_todo`;
        
        console.log('添加任务URL:', addUrl); // 调试输出
        
        fetch(addUrl, {
            method: 'POST',
            body: JSON.stringify(form),
            headers: {'Content-Type': 'application/json'},
        }).then((response) => {
            if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
            return response.json();
        }).then((data) => {
            console.log('添加任务响应:', data);
            form.title = '';
            fetchData(); // 添加后刷新列表
        }).catch(error => {
            console.error('添加任务失败:', error);
        });
    };

    // 4. 删除任务
    const delete_todo = (index) => {
        fetch(`${url}/${index}`, {
            method: 'DELETE',
            body: JSON.stringify({id: index})
        }).then((response) => {
            return response.json();
        }).then((data) => {
            console.log(data);
            fetchData();
        });
    };

    // 5. 清除已完成任务
    const clearCompletedTodos = () => {
        fetch(`${url}/clear_done`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then((response) => {
            return response.json();
        }).then((data) => {
            console.log(data);
            fetchData(); // 刷新任务列表
        });
    };

    onMounted(() => {
        fetchData();
    });
</script>

<template>
    <div class="container mt-3">
        <div class="row ">
            <div class="col-6 m-auto">
                <form action="/add_todo" method="post">
                    <div class="input-group mb-3">
                        <input type="text" class="form-control"
                               placeholder="请输入任务" name="title"
                               v-model="form.title"
                        >
                        <button type="submit" class="btn btn-primary" @click.prevent="add_todo">添加事项</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="row">
            <div class="col-6 m-auto">
                <div class="list-group  mb-3">
                    <label class="list-group-item" v-for="todo in todos">
                        <input class="form-check-input me-1 todo-input"
                               type="checkbox" v-if="todo.done" checked
                               value="{{ todo.id }}"
                               @change="change_todo_status(todo)"
                        >
                        <input class="form-check-input me-1 todo-input"
                               type="checkbox" v-if="!todo.done"
                               value="{{ todo.id }}"
                               @change="change_todo_status(todo)"
                        >
                        <span class="text-muted">{{ todo.title }}</span>
                        <a class="text-decoration-none float-end" @click="delete_todo(todo.id)">删除</a>
                    </label>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-6 m-auto d-flex justify-content-between">
                <button type="button" class="btn text-decoration-none" disabled>{{ undone_count }}条剩余</button>

                <div class="btn-group">
                    <a href="#" class="btn btn-outline-primary " :class="{ 'active': currentStatus === 'all' }" @click.prevent="switchStatus('all')">全部</a>
                    <a href="#" class="btn btn-outline-primary" :class="{ 'active': currentStatus === 'undone' }" @click.prevent="switchStatus('undone')">未完成</a>
                    <a href="#" class="btn btn-outline-primary " :class="{ 'active': currentStatus === 'done' }" @click.prevent="switchStatus('done')">已完成</a>

                </div>


                <a href="#" class="btn btn-link text-decoration-none" @click.prevent="clearCompletedTodos">清除已完成</a>
            </div>
        </div>
    </div>
</template>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
</style>
