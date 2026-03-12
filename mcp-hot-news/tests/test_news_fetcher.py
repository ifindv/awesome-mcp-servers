
"""
测试新闻获取器
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.news_fetcher import NewsFetcher
from src.models import NewsItem, NewsRequest


class TestNewsFetcher:
    """测试NewsFetcher类"""

    @pytest.mark.asyncio
    async def test_fetch_all_news(self, news_fetcher, sample_news_items):
        """测试获取所有新闻"""
        # 设置mock返回值
        for provider in news_fetcher.providers:
            provider.fetch.return_value = [
                {
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'hot_score': item.hot_score,
                    'author': item.author,
                    'publish_time': item.publish_time,
                    'tags': item.tags
                } for item in [sample_news_items[0]]
            ]

        # 调用方法
        all_news = await news_fetcher.fetch_all_news()

        # 验证结果
        assert len(all_news) == 3  # 3个provider
        assert all(isinstance(news, NewsItem) for news in all_news)

    @pytest.mark.asyncio
    async def test_fetch_all_news_with_exception(self, news_fetcher, sample_news_items):
        """测试获取所有新闻时处理异常"""
        # 设置第一个provider抛出异常
        news_fetcher.providers[0].fetch.side_effect = Exception("Network error")
        
        # 为其他两个provider设置返回值
        for provider in news_fetcher.providers[1:]:
            provider.fetch.return_value = [
                {
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'hot_score': item.hot_score,
                    'author': item.author,
                    'publish_time': item.publish_time,
                    'tags': item.tags
                } for item in [sample_news_items[0]]
            ]

        # 调用方法
        all_news = await news_fetcher.fetch_all_news()

        # 验证结果 - 应该跳过异常的provider
        assert len(all_news) == 2  # 2个成功的provider

    @pytest.mark.asyncio
    async def test_fetch_news_from_source(self, news_fetcher, sample_news_items):
        """测试从指定源获取新闻"""
        source = "知乎"
        provider = news_fetcher._get_provider_by_name(source)

        # 设置mock返回值
        provider.fetch.return_value = [
            {
                'title': item.title,
                'content': item.content,
                'url': item.url,
                'hot_score': item.hot_score,
                'author': item.author,
                'publish_time': item.publish_time,
                'tags': item.tags
            } for item in [sample_news_items[0]]
        ]

        # 调用方法
        news_list = await news_fetcher.fetch_news_from_source(source)

        # 验证结果
        assert len(news_list) == 1
        assert isinstance(news_list[0], NewsItem)
        assert news_list[0].source == source

    @pytest.mark.asyncio
    async def test_fetch_news_from_invalid_source(self, news_fetcher):
        """测试从无效源获取新闻"""
        source = "无效源"

        # 调用方法
        news_list = await news_fetcher.fetch_news_from_source(source)

        # 验证结果
        assert news_list == []

    @pytest.mark.asyncio
    async def test_fetch_hot_news(self, news_fetcher, sample_news_items):
        """测试获取热点新闻"""
        # 设置mock返回值
        for provider in news_fetcher.providers:
            provider.fetch.return_value = [
                {
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'hot_score': item.hot_score,
                    'author': item.author,
                    'publish_time': item.publish_time,
                    'tags': item.tags
                } for item in sample_news_items
            ]

        # 调用方法
        hot_news = await news_fetcher.fetch_hot_news(limit=2)

        # 验证结果
        assert len(hot_news) == 2
        # 验证按热度排序
        assert hot_news[0].hot_score >= hot_news[1].hot_score

    @pytest.mark.asyncio
    async def test_search_news(self, news_fetcher, sample_news_items):
        """测试搜索新闻"""
        # 设置mock返回值 - 只让第一个provider返回包含AI的新闻
        news_fetcher.providers[0].fetch.return_value = [
            {
                'title': item.title,
                'content': item.content,
                'url': item.url,
                'hot_score': item.hot_score,
                'author': item.author,
                'publish_time': item.publish_time,
                'tags': item.tags
            } for item in [sample_news_items[0]]  # 只返回包含AI的新闻
        ]
        # 其他provider返回不包含AI的新闻
        for provider in news_fetcher.providers[1:]:
            provider.fetch.return_value = [
                {
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'hot_score': item.hot_score,
                    'author': item.author,
                    'publish_time': item.publish_time,
                    'tags': item.tags
                } for item in sample_news_items[1:]  # 不包含AI的新闻
            ]

        # 创建搜索请求
        request = NewsRequest(
            keywords="AI",
            limit=10,
            offset=0
        )

        # 调用方法
        results = await news_fetcher.search_news(request)

        # 验证结果
        assert len(results) == 1  # 只有一条包含"AI"的新闻
        assert "AI" in results[0].title or "AI" in results[0].content

    @pytest.mark.asyncio
    async def test_search_news_by_category(self, news_fetcher, sample_news_items):
        """测试按分类搜索新闻"""
        # 设置mock返回值 - 只让第一个provider返回科技新闻
        news_fetcher.providers[0].fetch.return_value = [
            {
                'title': item.title,
                'content': item.content,
                'url': item.url,
                'hot_score': item.hot_score,
                'author': item.author,
                'publish_time': item.publish_time,
                'tags': item.tags,
                'category': item.category  # 添加category字段
            } for item in [sample_news_items[0]]  # 只返回科技新闻
        ]
        # 其他provider返回非科技新闻
        for provider in news_fetcher.providers[1:]:
            provider.fetch.return_value = [
                {
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'hot_score': item.hot_score,
                    'author': item.author,
                    'publish_time': item.publish_time,
                    'tags': item.tags,
                    'category': item.category  # 添加category字段
                } for item in sample_news_items[1:]  # 非科技新闻
            ]

        # 创建搜索请求
        request = NewsRequest(
            category="科技",
            limit=10,
            offset=0
        )

        # 调用方法
        results = await news_fetcher.search_news(request)

        # 验证结果
        assert len(results) == 1  # 只有一条科技新闻
        assert results[0].category == "科技"

    @pytest.mark.asyncio
    async def test_search_news_with_offset(self, news_fetcher, sample_news_items):
        """测试带偏移量的搜索"""
        # 设置mock返回值
        for provider in news_fetcher.providers:
            provider.fetch.return_value = [
                {
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'hot_score': item.hot_score,
                    'author': item.author,
                    'publish_time': item.publish_time,
                    'tags': item.tags
                } for item in sample_news_items
            ]

        # 创建搜索请求
        request = NewsRequest(
            limit=2,
            offset=1
        )

        # 调用方法
        results = await news_fetcher.search_news(request)

        # 验证结果
        assert len(results) == 2
        # 验证偏移量
        assert results[0].hot_score <= sample_news_items[0].hot_score

    def test_get_provider_by_name(self, news_fetcher):
        """测试根据名称获取提供者"""
        # 测试存在的提供者
        provider = news_fetcher._get_provider_by_name("微信")
        assert provider is not None
        assert provider.name == "微信"

        # 测试不存在的提供者
        provider = news_fetcher._get_provider_by_name("无效源")
        assert provider is None

    def test_cache_validity(self, news_fetcher):
        """测试缓存有效性"""
        # 清除缓存
        news_fetcher.clear_cache()

        # 测试空缓存
        assert not news_fetcher._is_cache_valid("test_key")

        # 更新缓存
        news_fetcher._update_cache("test_key", [])

        # 测试有效缓存
        assert news_fetcher._is_cache_valid("test_key")

    def test_clear_cache(self, news_fetcher):
        """测试清除缓存"""
        # 更新缓存
        news_fetcher._update_cache("test_key", [])

        # 清除缓存
        news_fetcher.clear_cache()

        # 验证缓存已清除
        assert not news_fetcher._is_cache_valid("test_key")
