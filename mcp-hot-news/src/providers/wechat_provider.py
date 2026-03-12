"""
微信热文提供者
"""
import sys
import os
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_provider import BaseProvider


logger = logging.getLogger(__name__)


class WechatProvider(BaseProvider):
    """微信热文提供者"""

    def __init__(self):
        """初始化微信提供者"""
        super().__init__(
            name="微信",
            url="https://weixin.sogou.com"
        )
        self.hot_url = "https://weixin.sogou.com/hot?r=hot"

    async def fetch(self) -> List[Dict]:
        """
        获取微信热文数据

        Returns:
            原始新闻数据列表
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                async with session.get(self.hot_url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self.parse(html)
                    else:
                        logger.error(f"Failed to fetch from Wechat, status code: {response.status}")
                        return []
        except Exception as e:
            self._log_fetch_error(e)
            return []

    def parse(self, html: str) -> List[Dict]:
        """
        解析微信热文数据

        Args:
            html: HTML内容

        Returns:
            解析后的新闻数据列表
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            news_list = []

            # 查找热文列表
            hot_list = soup.find('div', class_='hot-list')
            if not hot_list:
                return []

            items = hot_list.find_all('li')
            for item in items:
                try:
                    news_item = self._parse_item(item)
                    if news_item:
                        news_list.append(news_item)
                except Exception as e:
                    logger.error(f"Error parsing Wechat item: {str(e)}")
                    continue

            return news_list
        except Exception as e:
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

    def _parse_item(self, item) -> Dict:
        """
        解析单个新闻项

        Args:
            item: BeautifulSoup元素

        Returns:
            新闻数据字典
        """
        title_elem = item.find('a', class_='title')
        if not title_elem:
            return None

        title = title_elem.get_text(strip=True)
        url = title_elem.get('href', '')

        # 获取热度
        hot_score_elem = item.find('span', class_='hot')
        hot_score = 0
        if hot_score_elem:
            hot_text = hot_score_elem.get_text(strip=True)
            hot_score = self._parse_hot_score(hot_text)

        # 获取摘要
        content_elem = item.find('p', class_='desc')
        content = content_elem.get_text(strip=True) if content_elem else ''

        # 获取来源
        author_elem = item.find('span', class_='author')
        author = author_elem.get_text(strip=True) if author_elem else ''

        return {
            'title': title,
            'content': content,
            'url': url,
            'hot_score': hot_score,
            'author': author,
            'publish_time': '',
            'tags': []
        }
