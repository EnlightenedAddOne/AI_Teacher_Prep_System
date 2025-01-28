# 大语言模型集成模块
from langchain_community.llms import Tongyi
from langchain_community.llms import ChatGLM


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


