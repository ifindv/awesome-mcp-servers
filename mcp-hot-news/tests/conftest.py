
"""
测试配置文件
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.news_fetcher import NewsFetcher
from src.news_processor import NewsProcessor
from src.models import NewsItem, NewsRequest, NewsCategory

# 在模块级别导入，确保所有地方使用同一个类
# 避免在函数内部导入导致类型不一致


@pytest.fixture
def sample_news_items():
    """示例新闻数据"""
    return [
        NewsItem(
            id="1",
            title="AI技术突破：大模型应用前景广阔",
            content="人工智能技术取得重大突破，大模型在各个领域的应用前景广阔。",
            url="https://example.com/news/1",
            source="知乎",
            category=NewsCategory.TECHNOLOGY,
            hot_score=1000,
            publish_time="2024-01-01",
            author="科技日报",
            tags=["AI", "人工智能", "大模型"]
        ),
        NewsItem(
            id="2",
            title="2024年奥运会筹备工作进展顺利",
            content="2024年奥运会各项筹备工作正在有序进行中。",
            url="https://example.com/news/2",
            source="微博",
            category=NewsCategory.SPORTS,
            hot_score=800,
            publish_time="2024-01-02",
            author="体育周刊",
            tags=["奥运会", "体育"]
        ),
        NewsItem(
            id="3",
            title="全球股市波动加剧",
            content="受多重因素影响，全球股市近期波动加剧。",
            url="https://example.com/news/3",
            source="微信",
            category=NewsCategory.FINANCE,
            hot_score=900,
            publish_time="2024-01-03",
            author="财经观察",
            tags=["股市", "金融"]
        )
    ]


@pytest.fixture
def sample_raw_data():
    """示例原始数据"""
    return [
        {
            "id": "1",
            "title": "AI技术突破",
            "content": "人工智能技术取得重大突破",
            "url": "https://example.com/news/1",
            "source": "知乎",
            "category": "科技",
            "hot_score": 1000,
            "publish_time": "2024-01-01",
            "author": "科技日报",
            "tags": ["AI", "人工智能"]
        },
        {
            "id": "2",
            "title": "奥运会筹备",
            "content": "2024年奥运会筹备工作进展顺利",
            "url": "https://example.com/news/2",
            "source": "微博",
            "category": "体育",
            "hot_score": 800,
            "publish_time": "2024-01-02",
            "author": "体育周刊",
            "tags": ["奥运会"]
        }
    ]


@pytest.fixture
def news_processor():
    """新闻处理器实例"""
    return NewsProcessor()


@pytest.fixture
def mock_providers():
    """模拟的提供者"""
    providers = []
    for name in ["微信", "知乎", "微博"]:
        provider = Mock()
        provider.name = name
        provider.fetch = AsyncMock(return_value=[])
        # 修复normalize方法，使其返回NewsItem对象
        # 使用闭包捕获正确的provider名称
        def make_normalize(provider_name):
            def normalize_to_news_item(raw_item):
                return NewsItem(
                    id=raw_item.get('id', ''),
                    title=raw_item.get('title', ''),
                    content=raw_item.get('content', ''),
                    url=raw_item.get('url', ''),
                    source=provider_name,
                    category=raw_item.get('category', '其他'),
                    hot_score=int(raw_item.get('hot_score', 0)),
                    publish_time=raw_item.get('publish_time', ''),
                    author=raw_item.get('author', ''),
                    tags=raw_item.get('tags', [])
                )
            return normalize_to_news_item
        provider.normalize = Mock(side_effect=make_normalize(name))
        providers.append(provider)
    return providers


@pytest.fixture
def news_fetcher(mock_providers):
    """新闻获取器实例"""
    return NewsFetcher(providers=mock_providers)


@pytest.fixture
def event_loop():
    """事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
