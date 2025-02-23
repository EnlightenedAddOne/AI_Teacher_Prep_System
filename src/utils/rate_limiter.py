import time
from threading import Lock
from typing import Optional


class TokenBucket:
    """令牌桶速率限制器"""

    def __init__(self, capacity: int = 3, fill_rate: float = 1.0, initial_tokens: Optional[int] = None):
        """
        初始化令牌桶
        
        Args:
            capacity: 桶的容量（最大令牌数）
            fill_rate: 令牌填充速率（每秒）
            initial_tokens: 初始令牌数，默认等于容量
        """
        self.capacity = int(capacity)
        self.fill_rate = float(fill_rate)
        self.tokens = float(initial_tokens if initial_tokens is not None else capacity)
        self.last_update = time.time()
        self.lock = Lock()
        self.min_wait_time = 2.0  # 增加最小等待时间到2秒

    def _add_tokens(self):
        """添加令牌"""
        now = time.time()
        time_passed = now - self.last_update
        new_tokens = time_passed * self.fill_rate

        # 确保令牌数是整数
        self.tokens = min(float(self.capacity), self.tokens + new_tokens)
        self.last_update = now

    def get_wait_time(self, tokens: float) -> float:
        """计算需要等待的时间"""
        with self.lock:
            self._add_tokens()
            if self.tokens >= tokens:
                return 0.0
            required_tokens = tokens - self.tokens
            return max(self.min_wait_time, required_tokens / self.fill_rate)

    def consume(self, tokens: int = 1, wait: bool = True) -> bool:
        """
        消耗令牌
        
        Args:
            tokens: 需要消耗的令牌数
            wait: 是否等待令牌可用
            
        Returns:
            是否成功获取令牌
        """
        tokens = float(tokens)  # 转换为浮点数以匹配内部计算
        
        wait_time = self.get_wait_time(tokens)
        
        if wait_time == 0.0:
            with self.lock:
                self.tokens -= tokens
                return True
        
        if not wait:
            return False
        
        time.sleep(wait_time)
        with self.lock:
            self._add_tokens()
            self.tokens -= tokens
            return True


class RateLimiter:
    """API速率限制管理器"""

    def __init__(self):
        # 更保守的速率限制设置
        self.request_limiter = TokenBucket(
            capacity=1,  # 单次请求
            fill_rate=0.2,  # 5秒一个令牌
            initial_tokens=1
        )
        self.minute_limiter = TokenBucket(
            capacity=20,  # 减少容量
            fill_rate=20/60,  # 每分钟20个请求
            initial_tokens=20
        )
        self.backoff_time = 3.0  # 增加初始退避时间
        self.max_backoff = 60.0  # 最大退避时间

    def wait_if_needed(self, tokens: int = 1):
        """等待直到可以发送请求"""
        try:
            wait_time_req = self.request_limiter.get_wait_time(tokens)
            wait_time_min = self.minute_limiter.get_wait_time(tokens)
            
            # 使用较大的等待时间，并确保最小等待时间
            wait_time = max(wait_time_req, wait_time_min, 3.0)
            
            if wait_time > 0:
                print(f"⏳ 等待 {wait_time:.1f} 秒以确保请求稳定...")
                time.sleep(wait_time)
            
            success = (self.request_limiter.consume(tokens, wait=False) and 
                      self.minute_limiter.consume(tokens, wait=False))
            
            if not success:
                print("⚠️ 资源受限，等待更长时间...")
                time.sleep(5.0)  # 更长的等待时间
                return False
            
            return True
            
        except Exception as e:
            print(f"⚠️ 速率限制器异常: {str(e)}")
            time.sleep(5.0)
            return False

    def increase_backoff(self):
        """增加退避时间"""
        self.backoff_time = min(self.backoff_time * 2, self.max_backoff)
        return self.backoff_time

    def reset_backoff(self):
        """重置退避时间"""
        self.backoff_time = 2.0  # 重置为2秒
