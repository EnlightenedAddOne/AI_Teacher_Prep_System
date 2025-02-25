import json
import threading
import time
from typing import Dict, Any

from src.configs import config
from src.llm_integration import LLMFactory
from src.utils import integrated_recommendation_prompt


class TokenBucket:
    """令牌桶限流器"""
    def __init__(self, capacity: int, fill_rate: float):
        """
        初始化令牌桶
        :param capacity: 桶的容量（最大令牌数）
        :param fill_rate: 令牌填充速率（每秒添加的令牌数）
        """
        self.capacity = int(capacity)  # 确保容量是整数
        self.fill_rate = float(fill_rate)  # 确保填充速率是浮点数
        
        self.tokens = self.capacity  # 当前令牌数
        self.last_update = time.time()  # 上次更新时间
        
        self._lock = threading.Lock()  # 线程锁

    def _update_tokens(self):
        """更新令牌数量"""
        now = time.time()
        delta = now - self.last_update
        
        # 计算需要添加的令牌数（转换为整数）
        new_tokens = int(delta * self.fill_rate)
        
        # 更新令牌数，不超过容量
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_update = now

    def acquire(self, tokens: int = 1, timeout: float = None) -> bool:
        """
        获取令牌
        :param tokens: 需要的令牌数
        :param timeout: 超时时间（秒）
        :return: 是否成功获取令牌
        """
        start_time = time.time()
        tokens = int(tokens)  # 确保请求的令牌数是整数
        
        while True:
            with self._lock:
                self._update_tokens()
                
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                
                # 计算需要等待的时间（保持为浮点数以获得更精确的等待时间）
                required_time = (tokens - self.tokens) / self.fill_rate
                
                # 如果设置了超时且等待时间超过超时时间，返回False
                if timeout is not None and (time.time() - start_time + required_time) > timeout:
                    return False
                
            # 等待一小段时间后重试
            time.sleep(min(required_time, 1.0))


def extract_json(text: str) -> str:
    """
    从文本中提取第一个完整的JSON对象
    """
    # 找到第一个左花括号的位置
    start = text.find('{')
    if start == -1:
        return ""
    
    # 初始化计数器和位置
    count = 0
    pos = start
    
    # 遍历字符串
    while pos < len(text):
        if text[pos] == '{':
            count += 1
        elif text[pos] == '}':
            count -= 1
            if count == 0:
                # 找到匹配的右花括号，返回完整的JSON字符串
                return text[start:pos+1]
        pos += 1
    
    return ""


class ResourceRecommender:
    def __init__(self):
        # 初始化 Moonshot 客户端
        self.client = LLMFactory.initialize_moonshot(config['api_keys']['moonshot_api_key'])
        # 初始化令牌桶：容量为2个令牌，每秒填充0.2个令牌（平均每5秒一个请求）
        self.rate_limiter = TokenBucket(capacity=2, fill_rate=0.2)

    def _extract_wait_time(self, error_msg: str) -> float:
        """从错误消息中提取需要等待的时间"""
        try:
            # 尝试从错误消息中提取等待时间
            if "after" in error_msg and "seconds" in error_msg:
                wait_str = error_msg.split("after")[1].split("seconds")[0].strip()
                return float(wait_str)
        except Exception:
            pass
        return 2.0  # 默认等待时间

    def _make_request(self, messages, tools):
        """发送请求并处理重试"""
        max_retries = 5  # 增加最大重试次数
        base_wait = 5.0  # 增加基础等待时间
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # 重试前等待
                    wait_time = base_wait * (2 ** attempt)
                    print(f"\n🔄 第 {attempt + 1} 次尝试，等待 {wait_time:.1f} 秒...")
                    time.sleep(wait_time)
                
                # 使用令牌桶限流
                print("⏳ 等待获取令牌...")
                if not self.rate_limiter.acquire(tokens=1, timeout=120):  # 增加超时时间到120秒
                    print("⚠️ 获取令牌超时，继续等待...")
                    continue
                print("✅ 获取令牌成功，发送请求...")
                
                # 使用LLMFactory调用Moonshot API
                return LLMFactory.call_moonshot_with_tools(
                    client=self.client,
                    messages=messages,
                    tools=tools,
                    temperature=0.3
                )
                
            except Exception as e:
                error_msg = str(e)
                print(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {error_msg}")
                
                if "rate_limit" in error_msg.lower():
                    # 从错误消息中提取等待时间
                    wait_time = self._extract_wait_time(error_msg)
                    print(f"⚠️ 触发速率限制，等待 {wait_time} 秒...")
                    time.sleep(wait_time)
                    continue  # 直接进行下一次尝试，不计入重试次数
                
                if attempt == max_retries - 1:
                    raise Exception(f"达到最大重试次数: {error_msg}")

    def recommend_books_and_papers(self, topic: str, book_count: int, paper_count: int) -> Dict[str, Any]:
        """推荐书籍和论文"""
        try:
            # 使用提示词模板
            prompt = integrated_recommendation_prompt.format(
                topic=topic,
                book_count=book_count,
                paper_count=paper_count
            )

            messages = [
                {
                    "role": "system",
                    "content": "你是一个教育资源推荐专家。请使用web搜索工具搜索并推荐高质量的教材和学术论文。请确保返回的是有效的JSON格式，不要包含任何额外的文本。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            tools = [{
                "type": "builtin_function",
                "function": {
                    "name": "$web_search"
                }
            }]

            # 发送请求并处理工具调用
            choice = self._make_request(messages, tools)
            finish_reason = choice.finish_reason

            while finish_reason == "tool_calls":
                messages.append(choice.message)

                for tool_call in choice.message.tool_calls:
                    tool_call_arguments = json.loads(tool_call.function.arguments)
                    if tool_call.function.name == "$web_search":
                        tool_result = LLMFactory.search_impl(tool_call_arguments)
                    else:
                        tool_result = f"Error: unable to find tool by name '{tool_call.function.name}'"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(tool_result)
                    })

                choice = self._make_request(messages, tools)
                finish_reason = choice.finish_reason

            # 解析最终响应
            final_response = ""  # 初始化变量
            try:
                final_response = choice.message.content.strip()
                print(f"\n📝 原始响应:\n{final_response[:500]}...")  # 打印前500个字符用于调试
                
                # 提取JSON
                json_str = extract_json(final_response)
                if not json_str:
                    raise json.JSONDecodeError("No valid JSON found", final_response, 0)
                
                result = json.loads(json_str)
                return result
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析错误: {str(e)}")
                if final_response:
                    print(f"📄 原始响应预览: {final_response[:200]}...")
                return {"books": [], "papers": []}
                
        except Exception as e:
            print(f"❌ 推荐失败: {str(e)}")
            return {"books": [], "papers": []}


# 测试代码
if __name__ == "__main__":
    try:
        # 创建推荐器实例
        recommender = ResourceRecommender()
        
        # 测试参数
        topic = "人工智能"  # 只测试一个主题
        book_count = 3      # 推荐3本书
        paper_count = 4     # 推荐4篇论文
        
        print(f"\n{'='*50}")
        print(f"🔍 正在为主题「{topic}」生成推荐...")
        print(f"{'='*50}")
        
        try:
            # 调用推荐方法
            results = recommender.recommend_books_and_papers(
                topic=topic,
                book_count=book_count,
                paper_count=paper_count
            )
            
            # 打印推荐的书籍
            print("\n📚 推荐书籍:")
            for i, book in enumerate(results.get("books", []), 1):
                print(f"\n{i}. 书名：{book.get('title')}")
                print(f"   作者：{book.get('author')}")
                print(f"   出版社：{book.get('publisher')}")
                print(f"   出版年份：{book.get('year')}")
                print(f"   ISBN：{book.get('isbn', '暂无')}")
            
            # 打印推荐的论文
            print("\n📄 推荐论文:")
            for i, paper in enumerate(results.get("papers", []), 1):
                print(f"\n{i}. 标题：{paper.get('title')}")
                print(f"   作者：{paper.get('author')}")
                print(f"   期刊：{paper.get('journal')}")
                print(f"   发表年份：{paper.get('year')}")
                print(f"   DOI：{paper.get('doi', '暂无')}")
            
        except Exception as e:
            print(f"❌ 处理主题「{topic}」时出错: {str(e)}")
        
    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")

