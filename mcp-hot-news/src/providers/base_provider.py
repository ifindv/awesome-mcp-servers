"""
新闻提供者基类
"""
import sys
import os
from abc import ABC, abstractmethod
from typing import List, Dict
import logging

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import NewsItem


logger = logging.getLogger(__name__)


# 自定义异常类
class NewsFetcherError(Exception):
    """新闻获取器基础异常"""
    pass


class ProviderNotFoundError(NewsFetcherError):
    """提供者未找到异常"""
    pass


class NetworkError(NewsFetcherError):
    """网络请求异常"""
    pass


class ParseError(NewsFetcherError):
    """数据解析异常"""
    pass


class BaseProvider(ABC):
    """新闻提供者基类"""

    def __init__(self, name: str, url: str):
        """
        初始化提供者

        Args:
            name: 提供者名称
            url: 数据源URL
        """
        self.name = name
        self.url = url

    @abstractmethod
    async def fetch(self) -> List[Dict]:
        """
        获取新闻数据

        Returns:
            原始新闻数据列表
        """
        pass

    @abstractmethod
    def parse(self, html: str) -> List[Dict]:
        """
        解析新闻数据

        Args:
            html: HTML内容

        Returns:
            解析后的新闻数据列表
        """
        pass

    def normalize(self, raw_item: Dict) -> NewsItem:
        """
        标准化新闻数据格式

        Args:
            raw_item: 原始新闻数据

        Returns:
            标准化的新闻对象
        """
        return NewsItem(
            id=self._generate_id(raw_item),
            title=raw_item.get('title', ''),
            content=raw_item.get('content', ''),
            url=raw_item.get('url', ''),
            source=self.name,
            category=raw_item.get('category', '其他'),
            hot_score=int(raw_item.get('hot_score', 0)),
            publish_time=raw_item.get('publish_time', ''),
            author=raw_item.get('author', ''),
            tags=raw_item.get('tags', [])
        )

    def _generate_id(self, raw_item: Dict) -> str:
        """
        生成新闻唯一标识

        Args:
            raw_item: 原始新闻数据

        Returns:
            新闻唯一标识
        """
        # 使用URL作为ID，如果没有URL则使用标题
        url = raw_item.get('url', '')
        if url:
            return f"{self.name}_{hash(url)}"
        return f"{self.name}_{hash(raw_item.get('title', ''))}"

    def _log_fetch_error(self, error: Exception):
        """
        记录获取错误

        Args:
            error: 异常对象
        """
        logger.error(f"Error fetching from {self.name}: {str(error)}")

    def _log_parse_error(self, error: Exception):
        """
        记录解析错误

        Args:
            error: 异常对象
        """
        logger.error(f"Error parsing from {self.name}: {str(error)}")
