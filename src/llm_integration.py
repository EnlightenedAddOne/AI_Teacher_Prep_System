# 大语言模型集成模块

import dashscope
from langchain_community.llms import ChatGLM
from openai import OpenAI
from typing import List, Dict, Any


class LLMFactory:

    @staticmethod
    def initialize_tongyi(api_key: str):
        """
        初始化通义千问模型（使用官方API）
        :param api_key: 通义千问API密钥
        :return: None (API key会被全局设置)
        """
        dashscope.api_key = api_key

    @staticmethod
    def call_tongyi(messages, model_name: str = "qwen-plus-2025-01-25"):
        """
        调用通义千问API
        :param messages: 消息列表，格式为[{"role": "user", "content": "xxx"}]
        :param model_name: 模型名称，可选值：
            - qwen-turbo: 通义千问基础版（默认）
            - qwen-plus: 通义千问专业版
            - qwen-max: 通义千问旗舰版
            - qwen-plus-2025-01-25
        :return: API响应
        """
        try:
            response = dashscope.Generation.call(
                model=model_name,
                messages=messages,
                result_format='message',  # 或 'text'
                temperature=0.7,
                top_p=0.9,
            )
            
            if response.status_code == 200:
                return response.output.choices[0].message
            else:
                print(f"通义千问API调用失败: {response.code} - {response.message}")
                return None
        except Exception as e:
            print(f"通义千问API调用出错: {str(e)}")
            return None

    @staticmethod
    def initialize_zhipu(api_key: str, model_name: str = "chatglm_turbo"):
        """
        初始化智谱清言模型
        :param api_key: 智谱API密钥
        :param model_name: 模型名称,默认为"chatglm_turbo"
        :return: ChatGLM LLM实例
        """
        return ChatGLM(
            api_key=api_key,
            model_name=model_name,  # 可选: "chatglm_turbo", "chatglm_pro", "chatglm_std", "chatglm_lite"
            temperature=0.7,
            top_p=0.7,
            max_tokens=4096
        )

    @staticmethod
    def initialize_deepseek(api_key: str):
        """
        初始化 DeepSeek 模型
        :param api_key: DeepSeek API密钥
        :return: OpenAI客户端实例（用于DeepSeek）
        """
        return OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
        )

    @staticmethod
    def call_deepseek(client, system_prompt: str, user_prompt: str, model: str = "deepseek-reasoner", temperature: float = 0.3):
        """
        调用 DeepSeek API
        :param client: DeepSeek客户端实例
        :param system_prompt: 系统角色提示词
        :param user_prompt: 用户提示词
        :param model:模型参数
        :param temperature: 温度参数，控制输出的随机性
        :return: 响应文本
        """
        try:
            if model == "deepseek-chat":
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            elif model == "deepseek-reasoner":
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature
                )
                return response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek API调用失败: {str(e)}")
            return None

    @staticmethod
    def initialize_moonshot(api_key: str):
        """
        初始化 Moonshot 模型
        :param api_key: Moonshot API密钥
        :return: OpenAI客户端实例（用于Moonshot）
        """
        return OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )

    @staticmethod
    def call_moonshot_with_tools(client, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]], 
                                model: str = "moonshot-v1-128k", temperature: float = 0.3) -> Dict[str, Any]:
        """
        调用 Moonshot API（带工具调用功能）
        :param client: Moonshot客户端实例
        :param messages: 消息列表
        :param tools: 工具列表
        :param model: 模型名称
        :param temperature: 温度参数
        :return: API响应
        """
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                tools=tools
            )
            return completion.choices[0]  # 返回第一个选择
        except Exception as e:
            print(f"Moonshot API调用失败: {str(e)}")
            raise  # 重新抛出异常，让调用者处理

    @staticmethod
    def search_impl(arguments: Dict[str, Any]) -> Any:
        """
        处理web搜索工具的调用
        在使用 Moonshot AI 提供的搜索工具时，直接返回参数即可
        """
        return arguments




