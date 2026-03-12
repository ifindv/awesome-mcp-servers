
"""
测试数据模型
"""
import pytest
from src.models import NewsItem, NewsRequest, NewsCategory


class TestNewsItem:
    """测试NewsItem类"""

    def test_news_item_creation(self):
        """测试创建新闻项"""
        news = NewsItem(
            id="1",
            title="测试新闻",
            content="这是一条测试新闻",
            url="https://example.com/news/1",
            source="测试源",
            category="科技",
            hot_score=100,
            publish_time="2024-01-01",
            author="测试作者",
            tags=["测试", "新闻"]
        )

        assert news.id == "1"
        assert news.title == "测试新闻"
        assert news.content == "这是一条测试新闻"
        assert news.url == "https://example.com/news/1"
        assert news.source == "测试源"
        assert news.category == "科技"
        assert news.hot_score == 100
        assert news.publish_time == "2024-01-01"
        assert news.author == "测试作者"
        assert news.tags == ["测试", "新闻"]

    def test_news_item_to_dict(self):
        """测试将新闻项转换为字典"""
        news = NewsItem(
            id="1",
            title="测试新闻",
            content="这是一条测试新闻",
            url="https://example.com/news/1",
            source="测试源",
            category="科技",
            hot_score=100,
            publish_time="2024-01-01",
            author="测试作者",
            tags=["测试", "新闻"]
        )

        news_dict = news.to_dict()

        assert isinstance(news_dict, dict)
        assert news_dict["id"] == "1"
        assert news_dict["title"] == "测试新闻"
        assert news_dict["content"] == "这是一条测试新闻"
        assert news_dict["url"] == "https://example.com/news/1"
        assert news_dict["source"] == "测试源"
        assert news_dict["category"] == "科技"
        assert news_dict["hot_score"] == 100
        assert news_dict["publish_time"] == "2024-01-01"
        assert news_dict["author"] == "测试作者"
        assert news_dict["tags"] == ["测试", "新闻"]


class TestNewsRequest:
    """测试NewsRequest类"""

    def test_news_request_defaults(self):
        """测试新闻请求的默认值"""
        request = NewsRequest()

        assert request.source is None
        assert request.category is None
        assert request.keywords is None
        assert request.limit == 10
        assert request.offset == 0

    def test_news_request_with_params(self):
        """测试带参数的新闻请求"""
        request = NewsRequest(
            source="知乎",
            category="科技",
            keywords="AI",
            limit=20,
            offset=5
        )

        assert request.source == "知乎"
        assert request.category == "科技"
        assert request.keywords == "AI"
        assert request.limit == 20
        assert request.offset == 5


class TestNewsCategory:
    """测试NewsCategory类"""

    def test_category_constants(self):
        """测试分类常量"""
        assert NewsCategory.TECHNOLOGY == "科技"
        assert NewsCategory.ENTERTAINMENT == "娱乐"
        assert NewsCategory.SPORTS == "体育"
        assert NewsCategory.FINANCE == "财经"
        assert NewsCategory.SOCIETY == "社会"
        assert NewsCategory.INTERNATIONAL == "国际"
        assert NewsCategory.OTHER == "其他"

    def test_get_all_categories(self):
        """测试获取所有分类"""
        categories = NewsCategory.get_all_categories()

        assert isinstance(categories, list)
        assert len(categories) == 7
        assert "科技" in categories
        assert "娱乐" in categories
        assert "体育" in categories
        assert "财经" in categories
        assert "社会" in categories
        assert "国际" in categories
        assert "其他" in categories
