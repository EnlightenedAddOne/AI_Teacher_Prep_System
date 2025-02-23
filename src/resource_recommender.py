import json
import time
from openai import OpenAI
from models import ResourceRecommendationRequest
from configs import config
from typing import Dict, Any, List
from utils.rate_limiter import RateLimiter


class ResourceRecommender:
    def __init__(self):
        self.client = OpenAI(
            api_key=config['api_keys']['moonshot_api_key'],
            base_url="https://api.moonshot.cn/v1"
        )
        self.rate_limiter = RateLimiter()
        self.search_queries = []

    def _make_request(self, messages, tools, force_wait=False):
        """发送请求并处理重试"""
        max_retries = 5  # 增加最大重试次数
        base_wait = 2.0  # 基础等待时间
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # 强制等待一段时间后再重试
                    wait_time = base_wait * (1.5 ** attempt)
                    print(f"\n🔄 第 {attempt + 1} 次尝试，先等待 {wait_time:.1f} 秒...")
                    time.sleep(wait_time)
                
                # 使用速率限制器
                if not self.rate_limiter.wait_if_needed():
                    continue  # 如果无法获取令牌，重试
                
                completion = self.client.chat.completions.create(
                    model="moonshot-v1-128k",
                    messages=messages,
                    temperature=0.3,
                    tools=tools
                )
                
                # 成功后重置退避时间
                self.rate_limiter.reset_backoff()
                return completion
                
            except Exception as e:
                if "429" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = self.rate_limiter.increase_backoff()
                        print(f"\n⚠️ 速率限制 (429)，等待 {wait_time:.1f} 秒后重试...")
                        continue
                    else:
                        raise Exception("已达到最大重试次数，建议稍后再试")
                else:
                    raise Exception(f"请求失败: {str(e)}")

    def _record_tool_calls(self, message) -> List[Dict]:
        """记录并返回工具调用中的搜索查询及其结果"""
        search_records = []
        try:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "web_search":
                        try:
                            args = json.loads(tool_call.function.arguments)
                            query = args.get("query", "")
                            # 根据搜索内容类型添加特定关键词
                            if "书籍" in query or "教材" in query:
                                query = f"中国 {query}"
                            elif "论文" in query:
                                query = f"CNKI {query}"
                            elif "视频" in query:
                                query = f"bilibili {query}"
                            
                            if query:
                                search_records.append({
                                    "query": query,
                                    "success": True,
                                    "timestamp": time.time()
                                })
                        except json.JSONDecodeError:
                            search_records.append({
                                "error": "Failed to parse search query",
                                "success": False,
                                "timestamp": time.time()
                            })
        except AttributeError:
            pass
        return search_records

    def recommend_all_resources(self, topic: str, request: ResourceRecommendationRequest) -> Dict[str, Any]:
        """推荐所有类型的资源"""
        final_response = None
        try:
            self.search_queries = []
            print(f"\n🔍 开始为主题「{topic}」搜索资源...")
            
            messages = [
                {
                    "role": "system",
                    "content": "你是一个教育资源推荐专家。你需要使用联网搜索功能，为教师推荐优质的教学资源。"
                },
                {
                    "role": "user",
                    "content": self._build_prompt(topic, request)
                }
            ]

            tools = [{
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }]

            # 使用速率限制器处理对话
            completion = self._make_request(messages, tools)
            search_results = self._record_tool_calls(completion.choices[0].message)
            if search_results:
                self.search_queries.extend(search_results)

            finish_reason = completion.choices[0].finish_reason
            while finish_reason == "tool_calls":
                messages.append(completion.choices[0].message)
                
                for tool_call in completion.choices[0].message.tool_calls:
                    tool_call_args = json.loads(tool_call.function.arguments)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(tool_call_args)
                    })
                
                # 使用速率限制器继续对话
                completion = self._make_request(messages, tools)
                search_results = self._record_tool_calls(completion.choices[0].message)
                if search_results:
                    self.search_queries.extend(search_results)
                finish_reason = completion.choices[0].finish_reason

            # 解析最终响应
            try:
                final_response = completion.choices[0].message.content
                result = json.loads(final_response)
                
                # 分析搜索结果
                successful_searches = sum(1 for q in self.search_queries if q.get("success", False))
                failed_searches = len(self.search_queries) - successful_searches
                
                # 添加详细的搜索信息到结果中
                result["_debug"] = {
                    "search_info": {
                        "total_searches": len(self.search_queries),
                        "successful_searches": successful_searches,
                        "failed_searches": failed_searches,
                        "search_records": self.search_queries
                    }
                }
                
                # 验证搜索覆盖率
                min_expected_searches = sum([
                    request.book_count if request.require_books else 0,
                    request.paper_count if request.require_papers else 0,
                    request.video_count if request.require_videos else 0
                ])
                
                if successful_searches < min_expected_searches:
                    result["_debug"]["warnings"] = [
                        "模型可能没有为每个推荐资源进行搜索验证",
                        f"预期至少 {min_expected_searches} 次搜索，实际成功 {successful_searches} 次"
                    ]
                
                if failed_searches > 0:
                    result["_debug"]["warnings"] = result["_debug"].get("warnings", [])
                    result["_debug"]["warnings"].append(f"有 {failed_searches} 次搜索失败")
                
                return result
                
            except (json.JSONDecodeError, AttributeError) as e:
                return {
                    "error": f"Failed to parse model response: {str(e)}",
                    "raw_response": final_response if 'final_response' in locals() else None,
                    "_debug": {
                        "search_info": {
                            "total_searches": len(self.search_queries),
                            "search_records": self.search_queries
                        }
                    }
                }

        except Exception as e:
            return {
                "error": f"推荐失败: {str(e)}",
                "_debug": {
                    "search_info": {
                        "total_searches": len(self.search_queries),
                        "search_records": self.search_queries
                    }
                }
            }

    def _build_prompt(self, topic: str, request: ResourceRecommendationRequest) -> str:
        """构建模型提示词"""
        prompt = f"""请根据主题"{topic}"推荐相关的教学资源。你必须使用web_search工具搜索并验证每个推荐的资源。

对于每个资源：
1. 先使用web_search搜索该类型资源
2. 从搜索结果中选择最相关的资源
3. 再次使用web_search验证具体资源的详细信息
4. 确保所有信息准确可靠

资源推荐要求：

1. 书籍 ({request.require_books})，需要 {request.book_count} 本：
   - 必须使用web_search搜索"中国 {topic} 教材 出版社"
   - 优先推荐：
     * 国内知名出版社（如高等教育出版社、人民教育出版社等）
     * 使用广泛的经典教材
     * 近五年出版的新版本
   - 返回格式：
     * 书名（必须完整准确）
     * 作者（必须完整准确）
     * 出版社（必须是实际出版社）
     * 简短介绍（包含版本信息）

2. 论文 ({request.require_papers})，需要 {request.paper_count} 篇：
   - 必须使用web_search搜索"CNKI {topic} 核心期刊"
   - 优先推荐：
     * 中国核心期刊论文
     * 近三年发表的研究
     * 引用率较高的论文
   - 返回格式：
     * 论文标题（必须是CNKI可查）
     * 作者（必须完整准确）
     * 发表年份（必须准确）
     * 期刊名称（必须是核心期刊）
     * 摘要（从CNKI获取）

3. 视频 ({request.require_videos})，需要 {request.video_count} 个：
   - 必须使用web_search搜索"bilibili {topic} 教学视频 播放量"
   - 强制要求：
     * 必须是B站（bilibili.com）视频
     * 视频链接格式必须是 "https://www.bilibili.com/video/BV..."
     * UP主必须是教育领域的优质创作者
   - 优先推荐：
     * 播放量高的视频
     * 评分高的视频
     * 最近一年更新的视频
   - 返回格式：
     * 视频标题（必须与B站一致）
     * UP主名字（必须与B站一致）
     * B站视频链接（必须完整有效）
     * 视频时长（必须准确）
     * 视频简介（包含播放量和评分）

请确保返回的JSON格式如下：
{{
    "books": [
        {{"title": "书名", "author": "作者", "publisher": "出版社", "description": "简介"}}
    ],
    "papers": [
        {{"title": "标题", "author": "作者", "year": "年份", "journal": "期刊", "abstract": "摘要"}}
    ],
    "videos": [
        {{"title": "标题", "creator": "UP主", "url": "B站链接", "duration": "时长", "description": "简介"}}
    ]
}}

重要提示：
1. 每个资源都必须单独验证
2. 所有信息必须来自搜索结果
3. 不要生成虚假信息
4. 视频必须是有效的B站链接
5. 宁可推荐少也不要推荐虚假信息
6. 如果搜索失败，返回空数组而不是虚构数据"""

        return prompt

    def recommend_resources(self, topic, resource_recommendation):
        pass
