# 获取推荐视频
import time
from typing import Dict, List
from urllib.parse import quote
import re

import requests
from bs4 import BeautifulSoup


def format_duration(duration_str: str) -> str:
    """
    格式化视频时长字符串
    :param duration_str: 原始时长字符串（如"12:34"或"1:23:45"）
    :return: 格式化后的时长字符串（如"12分34秒"或"1小时23分45秒"）
    """
    try:
        parts = duration_str.strip().split(':')
        if len(parts) == 2:  # MM:SS
            return f"{int(parts[0])}分{int(parts[1])}秒"
        elif len(parts) == 3:  # HH:MM:SS
            return f"{int(parts[0])}小时{int(parts[1])}分{int(parts[2])}秒"
        return duration_str
    except Exception:
        return duration_str


def format_view_count(view_str: str) -> str:
    """
    格式化播放量字符串
    :param view_str: 原始播放量字符串（如"1.2万"）
    :return: 格式化后的播放量字符串
    """
    try:
        view_str = view_str.strip()
        # 首先尝试处理带单位的数字
        if '万' in view_str:
            num = float(view_str.replace('万', '')) * 10000
        elif '亿' in view_str:
            num = float(view_str.replace('亿', '')) * 100000000
        else:
            # 移除非数字字符
            num = float(re.sub(r'[^\d.]', '', view_str))

        # 根据数值大小决定显示格式
        if num >= 10000:
            # 转换为万为单位，保留两位小数
            wan = num / 10000
            return f"{wan:.2f}万播放"
        else:
            # 小于1万的数字显示完整数值
            return f"{int(num)}播放"
    except Exception:
        return "未知播放量"


def get_bilibili_videos(course_name: str, video_count: int = 5) -> List[Dict[str, str]]:
    """
    从B站搜索页面获取视频链接，按播放量排序
    :param course_name: 课程名称（如"网络协议"、"Python"等）
    :param video_count: 需要获取的视频数量，默认为5
    :return: 视频信息列表，包含标题、链接、时长和播放量
    """
    # 固定最大重试次数
    MAX_RETRIES = 3

    # 固定的搜索关键词后缀列表
    SEARCH_SUFFIXES = [
        "详解",
        "视频教程"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bilibili.com/'
    }

    for attempt in range(MAX_RETRIES):
        try:
            # 构建搜索关键词（课程名称 + 所有后缀）
            # 使用空格连接所有关键词，这样B站会对所有关键词进行匹配
            keyword = f"{course_name}{' '.join(SEARCH_SUFFIXES)}"
            print(f"使用搜索关键词: {keyword}")
            
            encoded_keyword = quote(keyword)
            url = f"https://search.bilibili.com/video?keyword={encoded_keyword}&order=click&duration=0&tids_1=0"

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找视频卡片元素
            video_cards = soup.find_all('div', class_='bili-video-card')

            if not video_cards:
                # 尝试其他可能的选择器
                video_cards = soup.find_all('div', class_='video-item')

            videos = []
            for card in video_cards[:video_count]:  # 获取指定数量的视频
                try:
                    # 获取链接和标题
                    link_elem = card.find('a', href=True)
                    if not link_elem:
                        continue

                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = 'https:' + link

                    title = link_elem.get('title', '')
                    if not title:
                        title_elem = card.find('h3') or card.find('p', class_='title')
                        if title_elem:
                            title = title_elem.text.strip()

                    # 获取视频时长
                    duration = None
                    duration_elem = card.find('span', class_='bili-video-card__stats__duration') or \
                                 card.find('span', class_='duration')
                    if duration_elem:
                        duration = format_duration(duration_elem.text.strip())

                    # 获取播放量
                    view_count = None
                    # 尝试多个可能的选择器
                    view_elem = (
                        card.find('span', class_='bili-video-card__stats__view') or
                        card.find('span', class_='view') or
                        card.find('span', string=re.compile(r'观看|播放')) or
                        card.find('span', class_='bili-video-card__stats--item') or
                        card.find('span', class_='play-text')
                    )
                    
                    if view_elem:
                        view_text = view_elem.text.strip()
                        # 如果文本包含"观看"或"播放"，提取数字部分
                        if '观看' in view_text or '播放' in view_text:
                            view_text = re.sub(r'[观看播放]', '', view_text)
                        view_count = format_view_count(view_text)

                    if link and 'bilibili.com/video' in link:
                        video_info = {
                            'title': title,
                            'url': link,
                            'duration': duration,
                            'view_count': view_count
                        }
                        # 打印调试信息
                        print(f"\n解析到视频信息:")
                        print(f"标题: {title}")
                        print(f"时长: {duration}")
                        print(f"播放量: {view_count}")
                        videos.append(video_info)
                except Exception as e:
                    print(f"解析视频卡片时出错: {str(e)}")
                    continue

            if videos:
                return videos  # 直接返回指定数量的视频

            print(f"未找到相关视频，等待重试...")
            time.sleep(2)

        except Exception as e:
            print(f"第 {attempt + 1} 次请求失败: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                print("获取视频链接失败，已达到最大重试次数")
                return []
            time.sleep(2)

    return []


def main():
    print("=== 开始搜索B站视频 ===")

    # 搜索课程名称
    course_name = "网络协议"
    print(f"\n课程名称: {course_name}")

    # 获取视频列表，指定获取3个视频
    videos = get_bilibili_videos(course_name, video_count=5)

    # 输出结果
    if videos:
        print("\n找到以下视频（按播放量排序）：")
        for i, video in enumerate(videos, 1):
            print(f"\n{i}. 标题: {video['title']}")
            print(f"   链接: {video['url']}")
            print(f"   时长: {video['duration'] or '未知'}")
            print(f"   播放量: {video['view_count'] or '未知'}")
    else:
        print("\n未找到相关视频")


if __name__ == "__main__":
    main()
