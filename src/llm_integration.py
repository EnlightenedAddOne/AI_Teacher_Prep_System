# 大语言模型集成模块

from langchain_community.llms import Tongyi
from langchain_community.llms import ChatGLM
from openai import OpenAI


class LLMFactory:

    @staticmethod
    def initialize_tongyi(api_key: str):
        """
        初始化通义千问模型
        :param api_key: 通义千问API密钥
        :return: Tongyi LLM实例
        """
        return Tongyi(api_key=api_key)

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




