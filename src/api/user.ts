import axios from "axios";
import type { AxiosResponse } from "axios";

const BASE_URL = "http://localhost:8080";

// 登录接口
export const login = async (username: string, password: string): Promise<string | null> => {
    try {
        const response: AxiosResponse<{ token: string }> = await axios.post(`${BASE_URL}/login`, {
            username,
            password,
        });
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
            `${BASE_URL}/admin/create-user`,
            {
                username,
                password,
                role,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data.message === "用户创建成功";
    } catch (error) {
        console.error("用户创建失败", error);
        return false;
    }
};
