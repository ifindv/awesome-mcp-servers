"""
微博热搜提供者
"""
import sys
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_provider import BaseProvider


logger = logging.getLogger(__name__)


class WeiboProvider(BaseProvider):
    """微博热搜提供者"""

    def __init__(self):
        """初始化微博提供者"""
        super().__init__(
            name="微博",
            url="https://weibo.com"
        )
        # 使用微博API获取热搜数据
        self.hot_url = "https://weibo.com/ajax/side/hotSearch"

    async def fetch(self) -> List[Dict]:
        """
        获取微博热搜数据

        Returns:
            原始新闻数据列表
        """
        try:
            logger.info(f"开始获取微博热搜数据, URL: {self.hot_url}")
            async with aiohttp.ClientSession() as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": "https://weibo.com",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
                }
                logger.debug(f"请求头: {headers}")

                async with session.get(self.hot_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    logger.info(f"微博响应状态码: {response.status}")
                    if response.status == 200:
                        try:
                            data = await response.json()
                            logger.debug(f"成功获取JSON数据")
                            result = self.parse(data)
                            logger.info(f"成功解析到 {len(result)} 条微博热搜")
                            return result
                        except Exception as e:
                            logger.error(f"解析JSON数据失败: {str(e)}", exc_info=True)
                            return []
                    else:
                        logger.error(f"Failed to fetch from Weibo, status code: {response.status}")
                        return []
        except asyncio.TimeoutError:
            logger.error(f"获取微博热搜超时")
            return []
        except Exception as e:
            logger.error(f"获取微博热搜时发生异常: {str(e)}", exc_info=True)
            self._log_fetch_error(e)
            return []

    def parse(self, data: Dict) -> List[Dict]:
        """
        解析微博热搜数据

        Args:
            data: JSON数据

        Returns:
            解析后的新闻数据列表
        """
        try:
            logger.debug("开始解析微博热搜JSON数据")
            news_list = []

            # 检查数据结构
            if "error" in data:
                logger.error(f"微博API返回错误: {data['error']}")
                return []

            # 获取热搜列表
            if "data" in data and "realtime" in data["data"]:
                logger.debug("找到realtime热搜列表")
                hot_items = data["data"]["realtime"]
                logger.debug(f"热搜条目数量: {len(hot_items)}")

                for idx, item in enumerate(hot_items):
                    try:
                        logger.debug(f"开始解析第 {idx + 1} 个热搜项")
                        news_item = self._parse_item(item)
                        if news_item:
                            logger.debug(f"成功解析热搜项: {news_item.get('title', 'N/A')}")
                            news_list.append(news_item)
                    except Exception as e:
                        logger.error(f"Error parsing Weibo item at index {idx}: {str(e)}", exc_info=True)
                        continue

                logger.info(f"共解析到 {len(news_list)} 条微博热搜")
                return news_list
            else:
                logger.warning("未找到预期的数据结构")
                logger.debug(f"完整数据结构: {list(data.keys())}")
                return []
        except Exception as e:
            logger.error(f"解析微博热搜时发生异常: {str(e)}", exc_info=True)
            self._log_parse_error(e)
            return []

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

    def _parse_item(self, item: Dict) -> Dict:
        """
        解析单个新闻项

        Args:
            item: JSON数据项

        Returns:
            新闻数据字典
        """
        # 获取标题
        title = item.get("word", "")
        if not title:
            return None

        # 构建URL
        url = f"https://s.weibo.com/weibo?q={title}"

        # 获取热度
        hot_score = self._parse_hot_score(item.get("num", 0))
        logger.debug(f"热搜标题: {title}, 热度: {hot_score}")

        # 获取分类
        category = item.get("category", "")

        # 获取摘要（微博热搜通常没有摘要）
        content = title

        # 获取作者/来源
        author = "微博热搜"

        return {
            'title': title,
            'content': content,
            'url': url,
            'hot_score': hot_score,
            'author': author,
            'publish_time': '',
            'tags': [category] if category else []
        }

    def _parse_alternative(self, soup: BeautifulSoup) -> List[Dict]:
        """
        尝试使用替代方式解析微博热搜数据

        Args:
            soup: BeautifulSoup对象

        Returns:
            解析后的新闻数据列表
        """
        logger.debug("尝试使用替代方式解析微博热搜")
        news_list = []

        try:
            # 尝试查找新的热搜列表结构
            # 微博可能使用了不同的容器类名
            possible_containers = [
                {'tag': 'div', 'class_': 'card-wrap'},
                {'tag': 'div', 'class_': 'card-wrap-a'},
                {'tag': 'div', 'class_': 'list'},
                {'tag': 'div', 'class_': 'list-wrap'},
                {'tag': 'ul', 'class_': 'list'},
                {'tag': 'div', 'class_': 'm-c-list'},
            ]

            items = []
            for container in possible_containers:
                container_elem = soup.find(container['tag'], class_=container['class_'])
                if container_elem:
                    logger.debug(f"找到容器: {container}")
                    # 尝试获取列表项
                    items = container_elem.find_all('li')
                    if not items:
                        items = container_elem.find_all('div', class_='m-c-item')
                    if items:
                        break

            if not items:
                logger.warning("未找到任何热搜列表容器")
                # 尝试直接查找所有链接
                all_links = soup.find_all('a')
                logger.debug(f"找到 {len(all_links)} 个链接")

                # 过滤出可能是热搜的链接
                for link in all_links:
                    href = link.get('href', '')
                    if '/weibo?q=' in href or 'weibo.com/search?q=' in href:
                        title = link.get_text(strip=True)
                        if title and len(title) > 2:  # 过滤掉太短的文本
                            news_list.append({
                                'title': title,
                                'content': title,
                                'url': href if href.startswith('http') else f"https://s.weibo.com{href}",
                                'hot_score': 0,
                                'author': '微博热搜',
                                'publish_time': '',
                                'tags': []
                            })

                logger.info(f"通过链接解析到 {len(news_list)} 条热搜")
                return news_list[:50]  # 限制返回数量

            logger.debug(f"找到 {len(items)} 个列表项")

            for idx, item in enumerate(items):
                try:
                    logger.debug(f"开始解析第 {idx + 1} 个热搜项")

                    # 尝试获取标题和链接
                    link_elem = item.find('a')
                    if not link_elem:
                        continue

                    title = link_elem.get_text(strip=True)
                    url = link_elem.get('href', '')

                    if not title or not url:
                        continue

                    # 处理相对URL
                    if not url.startswith('http'):
                        url = f"https://s.weibo.com{url}"

                    # 尝试获取热度
                    hot_score = 0
                    hot_elem = item.find('span', class_='hot')
                    if not hot_elem:
                        hot_elem = item.find('span', class_='num')
                    if not hot_elem:
                        hot_elem = item.find('em')

                    if hot_elem:
                        hot_text = hot_elem.get_text(strip=True)
                        hot_score = self._parse_hot_score(hot_text)

                    news_item = {
                        'title': title,
                        'content': title,
                        'url': url,
                        'hot_score': hot_score,
                        'author': '微博热搜',
                        'publish_time': '',
                        'tags': []
                    }

                    logger.debug(f"成功解析热搜项: {title}")
                    news_list.append(news_item)

                except Exception as e:
                    logger.error(f"解析第 {idx + 1} 个热搜项时出错: {str(e)}", exc_info=True)
                    continue

            logger.info(f"通过替代方式解析到 {len(news_list)} 条微博热搜")
            return news_list

        except Exception as e:
            logger.error(f"使用替代方式解析微博热搜时发生异常: {str(e)}", exc_info=True)
            return []
