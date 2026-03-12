"""
数据模型定义
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class NewsItem:
    """新闻数据模型"""
    id: str                    # 新闻唯一标识
    title: str                 # 新闻标题
    content: str               # 新闻内容摘要
    url: str                   # 新闻链接
    source: str                # 新闻源
    category: str              # 新闻分类
    hot_score: int             # 热度分数
    publish_time: str          # 发布时间
    author: str                # 作者/来源
    tags: List[str]            # 标签

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "hot_score": self.hot_score,
            "publish_time": self.publish_time,
            "author": self.author,
            "tags": self.tags
        }


@dataclass
class NewsRequest:
    """新闻请求模型"""
    source: Optional[str] = None       # 新闻源
    category: Optional[str] = None     # 新闻分类
    keywords: Optional[str] = None     # 关键词
    limit: int = 10                    # 数量限制
    offset: int = 0                    # 偏移量


class NewsCategory:
    """新闻分类常量"""
    TECHNOLOGY = "科技"
    ENTERTAINMENT = "娱乐"
    SPORTS = "体育"
    FINANCE = "财经"
    SOCIETY = "社会"
    INTERNATIONAL = "国际"
    OTHER = "其他"

    @classmethod
    def get_all_categories(cls) -> List[str]:
        """获取所有分类"""
        return [
            cls.TECHNOLOGY,
            cls.ENTERTAINMENT,
            cls.SPORTS,
            cls.FINANCE,
            cls.SOCIETY,
            cls.INTERNATIONAL,
            cls.OTHER
        ]
