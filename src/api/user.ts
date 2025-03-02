import axios from "axios";

const baseURL = "/api"; // 使用 Vite 代理，直接以 /api 开头

// 登录接口
export const login = async (username: string, password: string) => {
  try {
    const response = await axios.post(`${baseURL}/login`, { username, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 管理员创建用户
export const createUser = async (token: string, user: { username: string; password: string; role: string; createdBy?: string }) => {
  try {
    const response = await axios.post(
      `${baseURL}/admin/create-user`,
      user,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 管理员删除用户
export const deleteUser = async (token: string, username: string) => {
  try {
    const response = await axios.delete(`${baseURL}/admin/delete-user/${username}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 管理员更新用户
export const updateUser = async (token: string, user: { username: string; password: string; role: string }) => {
  try {
    const response = await axios.put(
      `${baseURL}/admin/update-user`,
      user,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 管理员获取所有用户
export const getAllUsers = async (token: string) => {
  try {
    const response = await axios.get(`${baseURL}/admin/users`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 管理员分配学生给教师
export const assignStudentToTeacher = async (token: string, studentUsername: string, teacherUsername: string) => {
  try {
    const response = await axios.put(
      `${baseURL}/admin/assign-student`,
      { studentUsername, teacherUsername }, // 将参数放在请求体中
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 教师创建学生
export const createStudent = async (token: string, student: { username: string; password: string }) => {
  try {
    const response = await axios.post(
      `${baseURL}/teacher/create-student`,
      { username: student.username, password: student.password }, // 移除 role 字段
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 教师获取所有学生
export const getStudents = async (token: string) => {
  try {
    const response = await axios.get(`${baseURL}/teacher/students`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 教师删除学生
export const deleteStudent = async (token: string, username: string) => {
  try {
    const response = await axios.delete(`${baseURL}/teacher/delete-student/${username}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
