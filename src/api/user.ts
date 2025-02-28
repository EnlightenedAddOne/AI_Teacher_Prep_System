import axios from "axios";
import type { AxiosResponse } from "axios";

const baseURL1 = "http://localhost:8080"; // 修改后的基础 URL
const TIMEOUT = 200000; // 超时时间设置为 200秒

// 登录接口
export const login = async (username: string, password: string): Promise<string | null> => {
    try {
        const response: AxiosResponse<{ token: string }> = await axios.post(`${baseURL1}/login`, {
            username,
            password,
        }, { timeout: TIMEOUT });
        return response.data.token;
    } catch (error) {
        console.error("登录失败", error);
        return null;
    }
};

// 创建用户接口
export const createUser = async (token: string, username: string, password: string, role: string): Promise<boolean> => {
    try {
        const response: AxiosResponse<{ message: string }> = await axios.post(
            `${baseURL1}/admin/create-user`,
            {
                username,
                password,
                role,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                timeout: TIMEOUT
            }
        );
        return response.data.message === "用户创建成功";
    } catch (error) {
        console.error("用户创建失败", error);
        return false;
    }
};

// 修改用户接口
export const updateUser = async (token: string, username: string, password: string, role: string): Promise<boolean> => {
    try {
        const response: AxiosResponse<{ message: string }> = await axios.put(
            `${baseURL1}/admin/update-user`,
            {
                username,
                password,
                role,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                timeout: TIMEOUT
            }
        );
        return response.data.message === "用户信息更新成功";
    } catch (error) {
        console.error("用户信息更新失败", error);
        return false;
    }
};

// 删除用户接口
export const deleteUser = async (token: string, username: string): Promise<boolean> => {
    try {
        const response: AxiosResponse<{ message: string }> = await axios.delete(
            `${baseURL1}/admin/delete-user/${username}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                timeout: TIMEOUT
            }
        );
        return response.data.message === "用户删除成功";
    } catch (error) {
        console.error("用户删除失败", error);
        return false;
    }
};
