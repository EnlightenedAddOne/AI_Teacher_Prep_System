import json
import logging
import os
import random
from multiprocessing.dummy import Pool
from pathlib import Path
from time import time, sleep
from typing import List, Dict
from urllib.parse import quote
import re
import hashlib

import requests
from lxml import etree

from configs import config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BingImageSpider')


# 作用：按关键字、图片数量爬取必应图片，并打印每张图片的名称及其链接。
def deduplication(info_list):
    result = []

    # 用图片的 md5 做为唯一标识符
    md5_set = set()
    for info in info_list:
        if info['image_md5'] not in md5_set:
            result.append(info)
            md5_set.add(info['image_md5'])
    return result


def parse_image_data(response: requests.Response) -> List[Dict]:
    """解析必应返回的图片数据"""
    try:
        tree = etree.HTML(response.text)
        m_list = tree.xpath('//a[@class="iusc"]/@m') or tree.xpath('//div[@class="imgpt"]/a/@m')

        results = []
        for m in m_list:
            try:
                data = json.loads(m)
                # 优先获取高清图片
                image_url = data.get('murl') or data.get('turl')

                img_info = {
                    'title': data.get('t', '').strip(),
                    'type': (image_url.split('.')[-1].lower() if '.' in image_url else 'jpg'),
                    'md5': data.get('md5', ''),
                    'url': image_url,
                    'width': data.get('w', 0),
                    'height': data.get('h', 0)
                }

                # 有效性检查
                if img_info['url'] and img_info['type'] in ['jpeg', 'jpg', 'png', 'webp', 'gif', 'bmp']:
                    logger.debug(f"有效图片: {img_info}")
                    results.append(img_info)
                else:
                    logger.warning(f"无效图片被过滤: {img_info}")

            except Exception as e:
                logger.error(f"解析图片数据失败: {str(e)}")
        return results

    except Exception as e:
        logger.error(f"解析页面失败: {str(e)}")
        return []


def _is_valid_image(chunk: bytes, img_type: str) -> bool:
    """通过文件头验证图片有效性"""
    file_headers = {
        'jpg': b'\xFF\xD8\xFF',
        'png': b'\x89PNG',
        'webp': b'RIFF....WEBP',
        'gif': b'GIF8'
    }
    return chunk.startswith(file_headers.get(img_type, b''))


class BingImagesSpider:
    # 配置参数
    thread_amount = 20  # 调整为更合理的线程数
    per_page_images = 35  # 必应每页最大图片数
    max_retries = 3  # 请求重试次数
    request_delay = 1  # 请求延迟（秒）

    # 请求头配置（更新为现代浏览器头）
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    # 图片类型映射
    IMAGE_TYPES = {
        'diagram': ['示意图', '结构图', '模型图', '流程图'],
        'real': ['实物图', '实拍图'],
        'chart': ['图表', '曲线图'],
        'default': ['教学图', '示例图']
    }

    # 新增配置参数
    min_image_size = 10 * 1024  # 降低到10KB
    valid_domains = ['zhimg.com', 'csdn.net', 'blogimg.cn', 'githubusercontent.com', 'sinaimg.cn', 'bdstatic.com', 'processon.com']

    def __init__(self, keyword: str, amount: int, img_type: str = 'diagram', proxy_list: List[str] = None):
        """
        初始化爬虫
        :param keyword: 搜索关键词
        :param amount: 需要图片数量
        :param img_type: 图片类型（diagram/real/chart/default）
        :param proxy_list: 代理列表
        """
        self.keyword = self._build_search_keyword(keyword, img_type)
        self.amount = max(1, min(amount, 150))
        self.required_amount = max(amount * 5, 100)  # 至少爬取100张候选
        self.proxy_list = proxy_list or []
        self.current_proxy = None
        self.thread_pool = Pool(self.thread_amount)
        self.found_images = set()  # 用于去重的集合
        # 增加常见图片网站白名单
        self.domain_headers = {
            'zhimg.com': {'Referer': 'https://www.zhihu.com/'},
            'csdnimg.cn': {'Referer': 'https://blog.csdn.net/'},
            'github.io': {'Referer': 'https://github.com/'}
        }
        # 修正为正确的三级父目录（src -> Langchain -> 项目根目录）
        current_dir = Path(__file__).parent  # src目录
        self.output_dir = current_dir.parent / "output" / "Images"  # Langchain/output/Images
        
        # 强制创建目录（与PDF生成逻辑一致）
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 添加路径验证日志
        logger.info(f"绝对存储路径：{self.output_dir.absolute()}")
        logger.info(f"目录可写：{os.access(str(self.output_dir), os.W_OK)}")

    def _build_search_keyword(self, base_keyword: str, img_type: str) -> str:
        """构建带图片类型的关键词"""
        modifiers = self.IMAGE_TYPES.get(img_type, self.IMAGE_TYPES['default'])
        return f'{base_keyword} {" ".join(modifiers)}'

    def _rotate_proxy(self):
        """轮换代理IP"""
        if self.proxy_list:
            self.current_proxy = {'https': random.choice(self.proxy_list)}

    def _request_with_retry(self, url: str) -> requests.Response:
        for _ in range(self.max_retries):
            try:
                # 添加随机延迟
                sleep(random.uniform(0.5, 1.5))

                resp = requests.get(
                    url,
                    headers=self.headers,
                    proxies=self.current_proxy,
                    timeout=15
                )

                # 增强反爬检测
                if "验证" in resp.text or "captcha" in resp.url:
                    raise Exception("触发反爬机制")

                return resp
            except Exception as e:
                logger.warning(f"请求失败: {str(e)}, 重试中...")
                sleep(self.request_delay)
        raise Exception(f"请求失败: {url}")

    def _get_custom_headers(self, url: str) -> dict:
        """根据域名获取特定请求头"""
        for domain in self.domain_headers:
            if domain in url:
                return {**self.headers, **self.domain_headers[domain]}
        return self.headers

    def _deduplicate(self, image_list: List[Dict]) -> List[Dict]:
        """多维度去重"""
        seen = set()
        unique_images = []

        for img in image_list:
            # 使用更严格的特征值
            identifier = hashlib.md5(img['url'].encode()).hexdigest()
            
            # 添加尺寸去重
            size_hash = f"{img.get('width',0)}x{img.get('height',0)}"
            identifier = f"{identifier}_{size_hash}"

            if identifier not in seen and identifier not in self.found_images:
                seen.add(identifier)
                self.found_images.add(identifier)
                unique_images.append(img)

        return unique_images

    def _validate_image(self, img_info: Dict) -> bool:
        """增强版图片验证"""
        try:
            # 域名白名单检查
            if not any(domain in img_info['url'] for domain in self.valid_domains):
                logger.debug(f"非常用域名图片: {img_info['url']}")
                return False

            # 添加动态Referer
            headers = {
                **self.headers,
                'Referer': 'https://www.bing.com/images/search?q=' + quote(self.keyword),
                'Accept-Encoding': 'identity'  # 避免压缩内容
            }

            # 使用流式请求获取部分数据
            for attempt in range(3):
                with requests.get(
                    img_info['url'],
                    headers=headers,
                    proxies=self.current_proxy,
                    stream=True,
                    timeout=8
                ) as resp:
                    resp.raise_for_status()

                    # 读取前512字节验证文件头
                    chunk = resp.raw.read(512)
                    if not _is_valid_image(chunk, img_info['type']):
                        logger.warning(f"无效文件头: {img_info['url']}")
                        continue

                    # 检查Content-Length
                    content_length = int(resp.headers.get('Content-Length', 0))
                    if content_length < self.min_image_size:
                        logger.warning(f"图片过小: {content_length} bytes")
                        continue

                    # 添加内容长度验证（与PDF生成时的验证类似）
                    if len(resp.content) < 10*1024:  # 10KB最小限制
                        continue

                    return True
            return False

        except Exception as e:
            logger.error(f"图片验证失败：{str(e)}")
            return False

    def save_image(self, url, filename, file_type):
        """保存图片到指定目录"""
        for i in range(5):  # 重试5次
            try:
                response = requests.get(url, headers=self.headers, timeout=20)
                response.raise_for_status()
                
                # 添加尺寸验证豁免
                if len(response.content) < 512:  # 允许更小的图片
                    logger.warning(f"图片过小被过滤：{url}")
                    return None
                    
                # 从URL生成唯一文件名
                file_md5 = hashlib.md5(url.encode()).hexdigest()
                base_name = f"{file_md5}_{int(time())}"
                filename = f"{base_name}.{file_type}"
                counter = 1
                while (self.output_dir / filename).exists():
                    filename = f"{base_name}_{counter}.{file_type}"
                    counter += 1
                
                filepath = self.output_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                logger.info(f"成功保存：{filepath}")
                return filepath.name
            except Exception as e:
                logger.error(f"下载失败（尝试{i+1}/5）: {str(e)}")
                sleep(2)
        return None

    def run(self) -> List[Dict]:
        """执行爬取"""
        try:
            logger.info(f"开始爬取 {self.amount} 张图片，关键词: {self.keyword}")

            # 生成请求URL列表
            base_url = "https://www.bing.com/images/async?q={}&first={}&count={}&mmasync=1"
            encoded_keyword = quote(self.keyword)

            # 计算需要请求的页数
            pages_needed = (self.required_amount // self.per_page_images) * 2
            urls = [
                base_url.format(encoded_keyword, page * self.per_page_images, self.per_page_images)
                for page in range(pages_needed)
            ]

            # 多线程请求
            responses = []
            for resp in self.thread_pool.imap(self._request_with_retry, urls):
                responses.append(resp)
                sleep(self.request_delay)  # 控制请求频率

            # 解析结果
            image_list = []
            for resp in responses:
                image_list.extend(parse_image_data(resp))

            # 去重处理
            unique_images = self._deduplicate(image_list)

            # 验证图片有效性
            validated_images = []
            retry_count = 0
            while len(validated_images) < self.amount and retry_count < 5:
                # 在添加图片时立即检查数量
                for img in unique_images:
                    if len(validated_images) >= self.amount:
                        break  # 达到数量立即终止
                    if self._validate_image(img):
                        # 生成唯一文件名
                        filename = f"{img['md5']}_{int(time())}.{img['type']}"
                        saved_path = self.save_image(img['url'], filename, img['type'])
                        if saved_path:
                            img['local_path'] = str(saved_path)
                            validated_images.append(img)
            
            # 添加结果验证
            logger.info(f"实际保存文件列表：{list(self.output_dir.glob('*'))}")
            
            # 在最后添加详细日志
            logger.info(f"请求数量: {len(responses)}页")
            logger.info(f"原始结果: {len(image_list)}张")
            logger.info(f"去重后: {len(unique_images)}张")
            logger.info(f"验证通过: {len(validated_images)}张")
            logger.info(f"最终保存: {len(list(self.output_dir.glob('*')))}张")
            
            # 在返回前添加数量控制
            # 精确截断结果
            final_results = validated_images[:self.amount]
            
            # 添加最终数量验证
            logger.info(f"最终返回数量: {len(final_results)}/{self.amount}")
            return final_results

        except Exception as e:
            logger.error(f"爬取过程发生错误: {str(e)}")
            return []
        finally:
            self.thread_pool.close()
            self.thread_pool.join()


if __name__ == '__main__':
    # 使用示例
    spider = BingImagesSpider(
        keyword="OSI七层模型",
        amount=7,
        img_type="diagram",
        proxy_list=["http://127.0.0.1:8080"]  # 如需代理可取消注释
    )

    start_time = time()
    results = spider.run()
    print(f"获取到 {len(results)} 张图片，耗时 {time() - start_time:.2f} 秒")
    for img in results:
        print(f"标题: {img['title']}\nURL: {img['url']}\n")
