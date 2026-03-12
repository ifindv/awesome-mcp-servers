"""
新闻数据处理模块
"""
import sys
import os
import logging
from typing import List, Dict

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入，确保与测试文件中的导入一致
try:
    from src.models import NewsItem, NewsCategory
except ImportError:
    from models import NewsItem, NewsCategory


logger = logging.getLogger(__name__)


class NewsProcessor:
    """新闻数据处理器"""

    def __init__(self):
        """初始化处理器，添加关键词权重和索引"""
        # 定义各分类的关键词及其权重
        self.category_weights = {
            NewsCategory.TECHNOLOGY: {
                "科技": 3, "AI": 3, "人工智能": 3,
                "芯片": 2, "5G": 2, "互联网": 2,
                "软件": 1, "硬件": 1, "编程": 1, "技术": 1
            },
            NewsCategory.ENTERTAINMENT: {
                "娱乐": 3, "电影": 2, "音乐": 2,
                "明星": 2, "演员": 1, "歌手": 1,
                "综艺": 1, "电视剧": 1, "游戏": 1
            },
            NewsCategory.SPORTS: {
                "体育": 3, "足球": 2, "篮球": 2,
                "NBA": 2, "奥运": 2, "世界杯": 2,
                "比赛": 1, "运动": 1, "冠军": 1, "总决赛": 2
            },
            NewsCategory.FINANCE: {
                "财经": 3, "股市": 2, "股票": 2,
                "经济": 2, "金融": 2, "投资": 1,
                "基金": 1, "银行": 1, "汇率": 1
            },
            NewsCategory.INTERNATIONAL: {
                "国际": 3, "美国": 2, "欧洲": 2,
                "日本": 1, "韩国": 1, "全球": 2,
                "联合国": 2, "外交": 2
            }
        }
        self._inverted_index = {}
        self._index_built = False

    def process_raw_data(self, raw_data: List[Dict]) -> List[NewsItem]:
        """
        处理原始数据

        Args:
            raw_data: 原始新闻数据列表

        Returns:
            处理后的新闻对象列表
        """
        processed_news = []
        for raw_item in raw_data:
            try:
                news_item = NewsItem(
                    id=raw_item.get('id', ''),
                    title=raw_item.get('title', ''),
                    content=raw_item.get('content', ''),
                    url=raw_item.get('url', ''),
                    source=raw_item.get('source', ''),
                    category=raw_item.get('category', NewsCategory.OTHER),
                    hot_score=int(raw_item.get('hot_score', 0)),
                    publish_time=raw_item.get('publish_time', ''),
                    author=raw_item.get('author', ''),
                    tags=raw_item.get('tags', [])
                )
                processed_news.append(news_item)
            except Exception as e:
                logger.error(f"Error processing raw item: {str(e)}")
                continue

        return processed_news

    def deduplicate_news(self, news_list: List[NewsItem]) -> List[NewsItem]:
        """
        新闻去重

        Args:
            news_list: 新闻对象列表

        Returns:
            去重后的新闻对象列表
        """
        seen = set()
        unique_news = []

        for news in news_list:
            # 使用标题作为去重依据
            title_key = news.title.lower().strip()
            if title_key not in seen:
                seen.add(title_key)
                unique_news.append(news)

        return unique_news

    def categorize_news(self, news: NewsItem) -> str:
        """
        新闻分类，使用权重机制

        Args:
            news: 新闻对象

        Returns:
            新闻分类
        """
        # 如果已经有分类，直接返回
        if news.category and news.category != NewsCategory.OTHER:
            return news.category

        # 基于关键词的加权分类
        text = f"{news.title} {news.content}".lower()
        scores = {}

        for category, keywords in self.category_weights.items():
            score = 0
            for keyword, weight in keywords.items():
                if keyword in text:
                    score += weight
            scores[category] = score

        # 返回得分最高的分类，如果没有匹配则返回社会新闻
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=scores.get)
        return NewsCategory.SOCIETY

    def format_news(self, news: NewsItem) -> Dict:
        """
        格式化新闻输出

        Args:
            news: 新闻对象

        Returns:
            格式化的新闻字典
        """
        return news.to_dict()

    def batch_categorize_news(self, news_list: List[NewsItem]) -> List[NewsItem]:
        """
        批量分类新闻

        Args:
            news_list: 新闻对象列表

        Returns:
            分类后的新闻对象列表
        """
        for news in news_list:
            news.category = self.categorize_news(news)
        return news_list

    def sort_news_by_hot(self, news_list: List[NewsItem], reverse: bool = True) -> List[NewsItem]:
        """
        按热度排序新闻

        Args:
            news_list: 新闻对象列表
            reverse: 是否降序排序

        Returns:
            排序后的新闻对象列表
        """
        return sorted(news_list, key=lambda x: x.hot_score, reverse=reverse)

    def filter_by_category(self, news_list: List[NewsItem], category: str) -> List[NewsItem]:
        """
        按分类过滤新闻

        Args:
            news_list: 新闻对象列表
            category: 新闻分类

        Returns:
            过滤后的新闻对象列表
        """
        return [news for news in news_list if news.category == category]

    def _build_inverted_index(self, news_list: List[NewsItem]):
        """
        构建倒排索引

        Args:
            news_list: 新闻对象列表
        """
        self._inverted_index = {}
        for idx, news in enumerate(news_list):
            # 处理标题
            for word in news.title.lower().split():
                if word not in self._inverted_index:
                    self._inverted_index[word] = set()
                self._inverted_index[word].add(idx)

            # 处理内容
            for word in news.content.lower().split():
                if word not in self._inverted_index:
                    self._inverted_index[word] = set()
                self._inverted_index[word].add(idx)

            # 处理标签
            for tag in news.tags:
                word = tag.lower()
                if word not in self._inverted_index:
                    self._inverted_index[word] = set()
                self._inverted_index[word].add(idx)

        self._index_built = True

    def filter_by_keywords(self, news_list: List[NewsItem], keywords: str) -> List[NewsItem]:
        """
        按关键词过滤新闻，使用倒排索引

        Args:
            news_list: 新闻对象列表
            keywords: 关键词

        Returns:
            过滤后的新闻对象列表
        """
        # 如果索引未构建，先构建索引
        if not self._index_built:
            self._build_inverted_index(news_list)

        keyword_list = keywords.lower().split()

        # 如果没有关键词，返回空列表
        if not keyword_list:
            return []

        # 获取第一个关键词的匹配项
        if keyword_list[0] not in self._inverted_index:
            return []

        matched_indices = self._inverted_index[keyword_list[0]].copy()

        # 对其余关键词取交集
        for keyword in keyword_list[1:]:
            if keyword not in self._inverted_index:
                return []
            matched_indices = matched_indices.intersection(self._inverted_index[keyword])

        # 返回匹配的新闻
        return [news_list[idx] for idx in matched_indices]
