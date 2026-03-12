"""
新闻数据获取模块
"""
import sys
import os
import asyncio
import logging
import aiohttp
from typing import List, Optional

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import NewsItem, NewsRequest
from providers import BaseProvider, WechatProvider, ZhihuProvider, WeiboProvider, ThepaperProvider
from providers.base_provider import (
    NewsFetcherError,
    ProviderNotFoundError,
    NetworkError,
    ParseError
)


logger = logging.getLogger(__name__)


class NewsFetcher:
    """新闻数据获取器"""

    def __init__(self, providers: Optional[List[BaseProvider]] = None):
        """
        初始化获取器

        Args:
            providers: 新闻提供者列表，如果为None则使用默认提供者
        """
        self.providers = providers or [
            WechatProvider(),
            ZhihuProvider(),
            WeiboProvider(),
            ThepaperProvider()
        ]
        self._cache = {}
        self._cache_time = {}
        self._cache_duration = 1800  # 30分钟缓存
        self._cache_size_limit = 1000  # 最大缓存条目数
        self._locks = {}  # 为每个源添加锁
        self._fetching = set()  # 跟踪正在获取的源

    async def fetch_all_news(self) -> List[NewsItem]:
        """
        获取所有新闻源数据

        Returns:
            新闻对象列表
        """
        cache_key = 'all_news'
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        all_news = []
        tasks = [provider.fetch() for provider in self.providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for provider, result in zip(self.providers, results):
            if isinstance(result, Exception):
                if isinstance(result, aiohttp.ClientError):
                    logger.error(f"Network error fetching from {provider.name}: {str(result)}")
                else:
                    logger.error(f"Error fetching from {provider.name}: {str(result)}")
                continue

            if not result:
                logger.warning(f"No data returned from {provider.name}")
                continue

            for raw_item in result:
                try:
                    news_item = provider.normalize(raw_item)
                    all_news.append(news_item)
                except Exception as e:
                    logger.error(f"Error normalizing item from {provider.name}: {str(e)}")
                    continue

        self._update_cache(cache_key, all_news)
        return all_news

    async def fetch_news_from_source(self, source: str) -> List[NewsItem]:
        """
        从指定源获取数据，添加并发控制

        Args:
            source: 新闻源名称

        Returns:
            新闻对象列表
        """
        cache_key = f'source_{source}'
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        # 获取或创建锁
        if source not in self._locks:
            self._locks[source] = asyncio.Lock()

        # 检查是否正在获取
        if source in self._fetching:
            # 等待其他请求完成
            while source in self._fetching:
                await asyncio.sleep(0.1)
            # 再次检查缓存
            if self._is_cache_valid(cache_key):
                return self._cache[cache_key]

        # 标记为正在获取
        self._fetching.add(source)

        try:
            async with self._locks[source]:
                # 再次检查缓存（可能在等待期间被其他请求更新）
                if self._is_cache_valid(cache_key):
                    return self._cache[cache_key]

                provider = self._get_provider_by_name(source)
                if not provider:
                    logger.error(f"Provider not found: {source}")
                    return []

                try:
                    raw_data = await provider.fetch()
                    if not raw_data:
                        logger.warning(f"No data returned from {source}")
                        return []

                    news_list = []
                    for item in raw_data:
                        try:
                            news_item = provider.normalize(item)
                            news_list.append(news_item)
                        except Exception as e:
                            logger.error(f"Error normalizing item from {source}: {str(e)}")
                            continue

                    self._update_cache(cache_key, news_list)
                    return news_list
                except aiohttp.ClientError as e:
                    logger.error(f"Network error fetching from {source}: {str(e)}")
                    return []
                except Exception as e:
                    logger.error(f"Unexpected error fetching from {source}: {str(e)}")
                    return []
        finally:
            # 移除获取标记
            self._fetching.discard(source)

    async def fetch_hot_news(self, limit: int = 10) -> List[NewsItem]:
        """
        获取热点新闻

        Args:
            limit: 返回数量限制

        Returns:
            新闻对象列表
        """
        cache_key = f'hot_{limit}'
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key][:limit]

        all_news = await self.fetch_all_news()
        # 按热度排序
        hot_news = sorted(all_news, key=lambda x: x.hot_score, reverse=True)
        self._update_cache(cache_key, hot_news)
        return hot_news[:limit]

    async def search_news(self, request: NewsRequest) -> List[NewsItem]:
        """
        搜索新闻

        Args:
            request: 新闻请求对象

        Returns:
            新闻对象列表
        """
        # 根据请求参数获取新闻
        if request.source:
            news_list = await self.fetch_news_from_source(request.source)
        else:
            news_list = await self.fetch_all_news()

        # 应用过滤条件
        if request.category:
            news_list = [n for n in news_list if n.category == request.category]

        if request.keywords:
            keywords = request.keywords.lower()
            news_list = [
                n for n in news_list
                if keywords in n.title.lower() or
                   keywords in n.content.lower() or
                   any(keywords in tag.lower() for tag in n.tags)
            ]

        # 排序
        news_list = sorted(news_list, key=lambda x: x.hot_score, reverse=True)

        # 应用分页
        start = request.offset
        end = start + request.limit
        return news_list[start:end]

    def _get_provider_by_name(self, name: str) -> Optional[BaseProvider]:
        """
        根据名称获取提供者

        Args:
            name: 提供者名称

        Returns:
            新闻提供者对象
        """
        for provider in self.providers:
            if provider.name == name:
                return provider
        return None

    def _is_cache_valid(self, key: str) -> bool:
        """
        检查缓存是否有效

        Args:
            key: 缓存键

        Returns:
            缓存是否有效
        """
        if key not in self._cache:
            return False
        import time
        return time.time() - self._cache_time[key] < self._cache_duration

    def _update_cache(self, key: str, data: List[NewsItem]):
        """
        更新缓存，并限制缓存大小

        Args:
            key: 缓存键
            data: 要缓存的数据
        """
        import time
        # 如果缓存已满，删除最旧的条目
        if len(self._cache) >= self._cache_size_limit:
            oldest_key = min(self._cache_time, key=self._cache_time.get)
            del self._cache[oldest_key]
            del self._cache_time[oldest_key]

        self._cache[key] = data
        self._cache_time[key] = time.time()

    def clear_cache(self):
        """清除所有缓存"""
        self._cache.clear()
        self._cache_time.clear()
