import json
import logging
import os
import random
from multiprocessing.dummy import Pool
from pathlib import Path
from time import time, sleep
from typing import List, Dict, Optional
from urllib.parse import quote
import re
import hashlib
from threading import Lock  # 新增导入

import requests
from lxml import etree

from configs import config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BingImageSpider')
logger.setLevel(logging.INFO)  # 仅保留必要日志


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

    # 合并所有图片类型关键词
    ALL_IMAGE_KEYWORDS = [
        '示意图', '结构图', '模型图', '流程图',
        '实物图', '实拍图', '图表', '曲线图',
        '教学图', '示例图'
    ]

    # 新增配置参数
    min_image_size = 10 * 1024  # 降低到10KB
    valid_domains = ['zhimg.com', 'csdn.net', 'blogimg.cn', 'githubusercontent.com', 'sinaimg.cn', 'bdstatic.com',
                     'processon.com']

    def __init__(self, keyword: str, amount: int, proxy_list: List[str] = None):
        """
        初始化爬虫（不再需要img_type参数）
        :param keyword: 搜索关键词
        :param amount: 需要图片数量
        :param proxy_list: 代理列表
        """
        self.keyword = self._build_search_keyword(keyword)
        self.amount = max(1, min(amount, 150))
        self.required_amount = max(amount * 5, 100)  # 至少爬取100张候选
        self.proxy_list = proxy_list or []
        self.current_proxy = None
        self.thread_pool = Pool(self.thread_amount)
        self.found_images = set()  # 用于去重的集合
        self.lock = Lock()  # 新增线程锁
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

    def _build_search_keyword(self, base_keyword: str) -> str:
        """构建带所有类型关键词的搜索词"""
        return f'{base_keyword} {" ".join(self.ALL_IMAGE_KEYWORDS)}'

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
        """增强型多维度去重"""
        unique_images = []

        for img in image_list:
            # 生成复合特征值：URL哈希 + 尺寸 + 文件头特征
            url_hash = hashlib.md5(img['url'].encode()).hexdigest()
            size_hash = f"{img.get('width', 0)}x{img.get('height', 0)}"
            file_header = img.get('md5', '')[:6]  # 使用前6位MD5

            identifier = f"{url_hash}_{size_hash}_{file_header}"

            # 使用线程锁保证原子操作
            with self.lock:
                if identifier not in self.found_images:
                    self.found_images.add(identifier)
                    unique_images.append(img)
                    # 实时日志记录
                    logger.debug(f"新增唯一图片：{identifier}")
                else:
                    logger.debug(f"发现重复图片：{identifier}")

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
                    if len(resp.content) < 10 * 1024:  # 10KB最小限制
                        continue

                    return True
            return False

        except Exception as e:
            logger.error(f"图片验证失败：{str(e)}")
            return False

    def _get_file_type(self, url: str) -> Optional[str]:
        """从URL和Content-Type获取文件类型"""
        try:
            # 优先从URL获取扩展名
            if '.' in url:
                ext = url.split('.')[-1].lower()
                if ext in {'jpg', 'jpeg', 'png', 'gif', 'webp'}:
                    return ext

            # 发起HEAD请求获取Content-Type
            with requests.head(url, headers=self.headers, timeout=10) as resp:
                content_type = resp.headers.get('Content-Type', '')
                if 'image/jpeg' in content_type:
                    return 'jpg'
                elif 'image/png' in content_type:
                    return 'png'
                elif 'image/gif' in content_type:
                    return 'gif'
                elif 'image/webp' in content_type:
                    return 'webp'
            return None
        except Exception as e:
            logger.warning(f"获取文件类型失败：{str(e)}")
            return None

    def _is_valid_image(self, file_path: Path) -> bool:
        """验证是否为有效图片文件"""
        try:
            from PIL import Image
            try:
                with Image.open(file_path) as img:
                    img.verify()
                return file_path.stat().st_size > 1024
            except Exception as e:
                logger.warning(f"损坏图片：{file_path} - {str(e)}")
                return False
        except ImportError:
            return file_path.stat().st_size > 1024 * 10

    def save_image(self, url: str, filename: str) -> Optional[Path]:
        temp_file = None  # 显式初始化变量
        try:
            # 获取正确扩展名
            file_type = self._get_file_type(url)
            if not file_type:
                return None

            # 生成临时文件名
            temp_file = self.output_dir / f"temp_{int(time())}.{file_type}"

            # 流式下载并计算MD5
            md5_hash = hashlib.md5()
            with requests.get(url, headers=self._get_custom_headers(url),
                              timeout=15, stream=True) as resp:
                resp.raise_for_status()

                with open(temp_file, 'wb') as f:
                    for chunk in resp.iter_content(4096):
                        if chunk:  # 过滤保持连接的空白块
                            f.write(chunk)
                            md5_hash.update(chunk)

            # 验证文件有效性
            if not self._is_valid_image(temp_file):
                temp_file.unlink()
                return None

            # 生成最终文件名
            final_filename = f"{md5_hash.hexdigest()}.{file_type}"
            final_path = self.output_dir / final_filename

            # 重命名临时文件
            temp_file.rename(final_path)
            logger.info(f"成功保存：{final_path}")
            return final_path

        except Exception as e:
            logger.error(f"保存失败：{str(e)}")
            if temp_file and temp_file.exists():  # 增加空值检查
                temp_file.unlink()
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
                        saved_path = self.save_image(img['url'], filename)
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
        keyword="网络协议",
        amount=7,
        proxy_list=["http://127.0.0.1:8080"]  # 如需代理可取消注释
    )

    start_time = time()
    results = spider.run()
    print(f"获取到 {len(results)} 张图片，耗时 {time() - start_time:.2f} 秒")
    for img in results:
        print(f"标题: {img['title']}\nURL: {img['url']}\n")
