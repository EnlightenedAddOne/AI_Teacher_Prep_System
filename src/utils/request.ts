//导入axios
import axios from 'axios'
//创建一个请求实例
const request = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})
//导出
export default request