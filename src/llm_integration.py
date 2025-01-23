# 大预言模型集成模块
from langchain_community.llms import Tongyi


def initialize_llm(api_key):
    return Tongyi(api_key=api_key, model="qwen-plus")

