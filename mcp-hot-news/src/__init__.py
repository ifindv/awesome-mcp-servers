"""
mcp-hot-news - MCP新闻热点服务
"""
from .server import HotNewsServer
from .news_fetcher import NewsFetcher
from .news_processor import NewsProcessor
from .models import NewsItem, NewsRequest, NewsCategory


__version__ = "0.1.0"
__all__ = [
    "HotNewsServer",
    "NewsFetcher",
    "NewsProcessor",
    "NewsItem",
    "NewsRequest",
    "NewsCategory"
]


__all_server__ = ["HotNewsServer"]
