import request from '@/utils/request'

//用户登录-参数类型
type LoginInfo = {
    phone: string
    password: string
}
//用户登录-返回数据类型
type LoginResult = {
    //...
    /*类似
    sucess: boolean
    state: number
    message: string
    content: string
    */
}
//用户请求登录
export const login = (loginInfo: LoginInfo) => {
    return request<LoginResult>({
        //测试用
        method: 'GET',
        url: '/users',
        data: 'phone=${loginInfo.phone}&password={loginInfo.username}'
    })
}

//用户退出
export const logout = () => {
    return request({
        //测试用
        method: 'GET',
        url: '/users',
    })
}