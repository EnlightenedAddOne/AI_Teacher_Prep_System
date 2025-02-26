<script setup>
    import {onMounted, ref, reactive, computed} from 'vue';

    const Local_url = 'http://127.0.0.1:5000';       // 本机运行前后端的url
    const Server_url = 'http://192.168.63.215:5000'; // 同一局域网下的url

    const far_url = 'https://8c97-218-28-159-7.ngrok-free.app'; // 非同一局域网下的url
    
    const baseUrl = ref(Local_url); // 直接使用服务器地址


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
        const requestUrl = `${baseUrl.value}/todo?key=${currentStatus.value}`;
        
        fetch(requestUrl, {
            headers: {
                'ngrok-skip-browser-warning': 'any-value', // 跳过ngrok警告
                'User-Agent': 'MyCustomClient/1.0',        // 自定义UA头
                'Content-Type': 'application/json'         // 明确请求类型
            }
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP错误 ${res.status}`);
            return res.json();
        })
        .then(data => {
            todos.value = data;
        })
        .catch(error => {
            console.error('请求失败:', error);
        });
    };


    // 2. 切换任务的完成状态
    const change_todo_status = (item) => {
        // 修正：使用正确的baseUrl
        fetch(`${baseUrl.value}/todo/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({ done: !item.done }), // 明确发送状态
            headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true'
            }
        }).then(res => {
            if (!res.ok) throw new Error(`HTTP错误 ${res.status}`);
            return res.json();
        }).then(data => {
            console.log('状态更新:', data);
            fetchData(); // 刷新列表
        }).catch(error => {
            console.error('状态更新失败:', error);
        });
    };
    // 3. 添加任务
    const add_todo = () => {
        // 修正：直接使用baseUrl不需要路径处理
        const addUrl = `${baseUrl.value}/todo/add_todo`;
        
        fetch(addUrl, {
            method: 'POST',
            body: JSON.stringify(form),
            headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true' // 添加ngrok头
            }
        }).then((response) => {
            if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
            return response.json();
        }).then((data) => {
            console.log('添加响应:', data);
            form.title = '';
            fetchData();
        }).catch(error => {
            console.error('添加失败:', error);
        });
    };

    // 4. 删除任务
    const delete_todo = (index) => {
        fetch(`${baseUrl.value}/todo/${index}`, {
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
        fetch(`${baseUrl.value}/todo/clear_done`, {
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
