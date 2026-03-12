
"""
澎湃新闻提供者
"""
import sys
import os
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
import re

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_provider import BaseProvider


logger = logging.getLogger(__name__)


class ThepaperProvider(BaseProvider):
    """澎湃新闻提供者"""

    def __init__(self):
        """初始化澎湃新闻提供者"""
        super().__init__(
            name="澎湃",
            url="https://www.thepaper.cn"
        )
        # 澎湃新闻热点URL
        self.hot_url = "https://www.thepaper.cn/"

    async def fetch(self) -> List[Dict]:
        """
        获取澎湃新闻热点数据

        Returns:
            原始新闻数据列表
        """
        try:
            logger.info(f"开始获取澎湃新闻热点数据, URL: {self.hot_url}")
            async with aiohttp.ClientSession() as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Referer": "https://www.thepaper.cn/"
                }
                logger.debug(f"请求头: {headers}")

                async with session.get(self.hot_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    logger.info(f"澎湃新闻响应状态码: {response.status}")
                    if response.status == 200:
                        html = await response.text()
                        logger.debug(f"成功获取HTML数据")
                        result = self.parse(html)
                        logger.info(f"成功解析到 {len(result)} 条澎湃新闻")
                        return result
                    else:
                        logger.error(f"Failed to fetch from Thepaper, status code: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"获取澎湃新闻时发生异常: {str(e)}", exc_info=True)
            self._log_fetch_error(e)
            return []

    def parse(self, html: str) -> List[Dict]:
        """
        解析澎湃新闻热点数据

        Args:
            html: HTML内容

        Returns:
            解析后的新闻数据列表
        """
        try:
            logger.debug("开始解析澎湃新闻HTML数据")
            soup = BeautifulSoup(html, 'html.parser')
            news_list = []

            # 尝试多种方式查找新闻列表
            # 方式1: 查找带有特定类名的新闻列表
            possible_containers = [
                {'tag': 'div', 'class_': 'news_li'},
                {'tag': 'div', 'class_': 'listitem'},
                {'tag': 'div', 'class_': 'newslist'},
                {'tag': 'div', 'class_': 'list'},
                {'tag': 'ul', 'class_': 'newslist'},
                {'tag': 'div', 'class_': 'hotnews'},
                {'tag': 'div', 'class_': 'hot_news'},
                {'tag': 'div', 'class_': 'newslist_v2'},
                {'tag': 'div', 'class_': 'newslist_v3'},
            ]

            items = []
            for container in possible_containers:
                container_elem = soup.find(container['tag'], class_=container['class_'])
                if container_elem:
                    logger.debug(f"找到容器: {container}")
                    # 尝试获取列表项
                    items = container_elem.find_all('div', class_='news_li')
                    if not items:
                        items = container_elem.find_all('div', class_='listitem')
                    if not items:
                        items = container_elem.find_all('li')
                    if items:
                        break

            # 如果没有找到标准列表，尝试查找所有新闻链接
            if not items:
                logger.warning("未找到标准新闻列表容器，尝试查找所有新闻链接")
                all_links = soup.find_all('a', href=re.compile(r'/newsDetail_forward_\d+'))
                logger.debug(f"找到 {len(all_links)} 个新闻链接")

                # 处理找到的链接
                for idx, link in enumerate(all_links):
                    try:
                        if idx >= 50:  # 限制数量
                            break
                        title = link.get_text(strip=True)
                        href = link.get('href', '')

                        if not title or len(title) < 5:  # 过滤掉太短的标题
                            continue

                        # 处理URL
                        if href.startswith('/'):
                            url = f"{self.url}{href}"
                        elif not href.startswith('http'):
                            url = f"{self.url}/{href}"
                        else:
                            url = href

                        news_item = {
                            'title': title,
                            'content': title,
                            'url': url,
                            'hot_score': 0,
                            'author': '澎湃新闻',
                            'publish_time': '',
                            'tags': []
                        }
                        news_list.append(news_item)
                    except Exception as e:
                        logger.error(f"Error parsing link at index {idx}: {str(e)}")
                        continue

                logger.info(f"通过链接解析到 {len(news_list)} 条新闻")
                return news_list[:50]  # 限制返回数量

            # 处理找到的标准列表项
            logger.debug(f"找到 {len(items)} 个列表项")
            for idx, item in enumerate(items):
                try:
                    logger.debug(f"开始解析第 {idx + 1} 个新闻项")
                    news_item = self._parse_item(item)
                    if news_item:
                        logger.debug(f"成功解析新闻项: {news_item.get('title', 'N/A')}")
                        news_list.append(news_item)
                except Exception as e:
                    logger.error(f"Error parsing Thepaper item at index {idx}: {str(e)}", exc_info=True)
                    continue

            logger.info(f"共解析到 {len(news_list)} 条澎湃新闻")
            return news_list[:50]  # 限制返回数量
        except Exception as e:
            logger.error(f"解析澎湃新闻时发生异常: {str(e)}", exc_info=True)
            self._log_parse_error(e)
            return []

    def _parse_item(self, item) -> Dict:
        """
        解析单个新闻项

        Args:
            item: BeautifulSoup元素

        Returns:
            新闻数据字典
        """
        # 获取标题和链接
        title_elem = item.find('a')
        if not title_elem:
            # 尝试其他方式查找标题
            title_elem = item.find('h3')
        if not title_elem:
            # 尝试查找带有特定类名的元素
            title_elem = item.find(class_='title')
        if not title_elem:
            # 尝试查找带有特定类名的元素
            title_elem = item.find(class_='tit')

        if not title_elem:
            return None

        title = title_elem.get_text(strip=True)
        href = title_elem.get('href', '')

        if not title or len(title) < 5:  # 过滤掉太短的标题
            return None

        # 处理URL
        if href.startswith('/'):
            url = f"{self.url}{href}"
        elif not href.startswith('http'):
            url = f"{self.url}/{href}"
        else:
            url = href

        # 获取摘要/内容
        content_elem = item.find('p')
        if not content_elem:
            content_elem = item.find(class_='desc')
        if not content_elem:
            content_elem = item.find(class_='summary')

        content = content_elem.get_text(strip=True) if content_elem else title

        # 获取作者/来源
        author_elem = item.find(class_='author')
        if not author_elem:
            author_elem = item.find(class_='source')

        author = author_elem.get_text(strip=True) if author_elem else '澎湃新闻'

        # 获取发布时间
        time_elem = item.find(class_='time')
        if not time_elem:
            time_elem = item.find(class_='date')

        publish_time = time_elem.get_text(strip=True) if time_elem else ''

        # 获取热度
        hot_score = 0
        hot_elem = item.find(class_='hot')
        if not hot_elem:
            hot_elem = item.find(class_='read')
        if not hot_elem:
            hot_elem = item.find(class_='view')

        if hot_elem:
            hot_text = hot_elem.get_text(strip=True)
            hot_score = self._parse_hot_score(hot_text)

        return {
            'title': title,
            'content': content,
            'url': url,
            'hot_score': hot_score,
            'author': author,
            'publish_time': publish_time,
            'tags': []
        }

    def _parse_hot_score(self, hot_text: str) -> int:
        """
        解析热度分数

        Args:
            hot_text: 热度文本

        Returns:
            热度分数
        """
        if not hot_text:
            return 0

        try:
            # 尝试直接转换为整数
            return int(hot_text)
        except ValueError:
            try:
                # 提取数字部分
                digits = ''.join(filter(str.isdigit, hot_text))
                if digits:
                    return int(digits)
            except ValueError:
                pass

        # 尝试处理"万"等单位
        if '万' in hot_text:
            try:
                num = float(hot_text.replace('万', '').strip())
                return int(num * 10000)
            except ValueError:
                pass

        return 0
