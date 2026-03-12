
"""
测试新闻处理器
"""
import pytest
from src.news_processor import NewsProcessor
from src.models import NewsItem, NewsCategory


class TestNewsProcessor:
    """测试NewsProcessor类"""

    def test_process_raw_data(self, news_processor, sample_raw_data):
        """测试处理原始数据"""
        processed_news = news_processor.process_raw_data(sample_raw_data)

        assert len(processed_news) == 2
        assert isinstance(processed_news[0], NewsItem)
        assert processed_news[0].id == "1"
        assert processed_news[0].title == "AI技术突破"
        assert processed_news[0].category == "科技"

    def test_process_raw_data_with_missing_fields(self, news_processor):
        """测试处理缺少字段的原始数据"""
        raw_data = [
            {
                "id": "1",
                "title": "测试新闻"
            },
            {
                "title": "无ID新闻"
            }
        ]

        processed_news = news_processor.process_raw_data(raw_data)

        assert len(processed_news) == 2
        assert processed_news[0].id == "1"
        assert processed_news[1].id == ""

    def test_deduplicate_news(self, news_processor):
        """测试新闻去重"""
        news_list = [
            NewsItem(
                id="1",
                title="测试新闻",
                content="内容",
                url="url1",
                source="source1",
                category="科技",
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=[]
            ),
            NewsItem(
                id="2",
                title="测试新闻",  # 相同标题
                content="不同内容",
                url="url2",
                source="source2",
                category="科技",
                hot_score=200,
                publish_time="2024-01-02",
                author="author2",
                tags=[]
            ),
            NewsItem(
                id="3",
                title="测试新闻  ",  # 带空格的相同标题
                content="另一内容",
                url="url3",
                source="source3",
                category="科技",
                hot_score=300,
                publish_time="2024-01-03",
                author="author3",
                tags=[]
            ),
            NewsItem(
                id="4",
                title="不同新闻",
                content="内容4",
                url="url4",
                source="source4",
                category="科技",
                hot_score=400,
                publish_time="2024-01-04",
                author="author4",
                tags=[]
            )
        ]

        unique_news = news_processor.deduplicate_news(news_list)

        assert len(unique_news) == 2
        assert unique_news[0].title == "测试新闻"
        assert unique_news[1].title == "不同新闻"

    def test_categorize_news_with_existing_category(self, news_processor):
        """测试已有分类的新闻"""
        news = NewsItem(
            id="1",
            title="科技新闻",
            content="内容",
            url="url",
            source="source",
            category=NewsCategory.TECHNOLOGY,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.TECHNOLOGY

    def test_categorize_news_tech(self, news_processor):
        """测试科技分类"""
        news = NewsItem(
            id="1",
            title="AI技术突破：大模型应用前景广阔",
            content="人工智能技术取得重大突破",
            url="url",
            source="source",
            category=NewsCategory.OTHER,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.TECHNOLOGY

    def test_categorize_news_entertainment(self, news_processor):
        """测试娱乐分类"""
        news = NewsItem(
            id="1",
            title="最新电影票房排行榜",
            content="本周电影票房数据出炉",
            url="url",
            source="source",
            category=NewsCategory.OTHER,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.ENTERTAINMENT

    def test_categorize_news_sports(self, news_processor):
        """测试体育分类"""
        news = NewsItem(
            id="1",
            title="NBA总决赛今日开赛",
            content="NBA总决赛将在今日正式拉开帷幕",
            url="url",
            source="source",
            category=NewsCategory.OTHER,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.SPORTS

    def test_categorize_news_finance(self, news_processor):
        """测试财经分类"""
        news = NewsItem(
            id="1",
            title="股市今日大涨",
            content="受多重利好因素影响，股市今日大幅上涨",
            url="url",
            source="source",
            category=NewsCategory.OTHER,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.FINANCE

    def test_categorize_news_international(self, news_processor):
        """测试国际分类"""
        news = NewsItem(
            id="1",
            title="联合国召开紧急会议",
            content="联合国就国际局势召开紧急会议",
            url="url",
            source="source",
            category=NewsCategory.OTHER,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.INTERNATIONAL

    def test_categorize_news_default(self, news_processor):
        """测试默认分类"""
        news = NewsItem(
            id="1",
            title="本地新闻",
            content="这是一条本地新闻",
            url="url",
            source="source",
            category=NewsCategory.OTHER,
            hot_score=100,
            publish_time="2024-01-01",
            author="author",
            tags=[]
        )

        category = news_processor.categorize_news(news)

        assert category == NewsCategory.SOCIETY

    def test_batch_categorize_news(self, news_processor):
        """测试批量分类新闻"""
        news_list = [
            NewsItem(
                id="1",
                title="AI技术突破",
                content="人工智能技术取得重大突破",
                url="url1",
                source="source1",
                category=NewsCategory.OTHER,
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=[]
            ),
            NewsItem(
                id="2",
                title="NBA总决赛",
                content="NBA总决赛今日开赛",
                url="url2",
                source="source2",
                category=NewsCategory.OTHER,
                hot_score=200,
                publish_time="2024-01-02",
                author="author2",
                tags=[]
            )
        ]

        categorized_news = news_processor.batch_categorize_news(news_list)

        assert len(categorized_news) == 2
        assert categorized_news[0].category == NewsCategory.TECHNOLOGY
        assert categorized_news[1].category == NewsCategory.SPORTS

    def test_sort_news_by_hot_descending(self, news_processor):
        """测试按热度降序排序"""
        news_list = [
            NewsItem(
                id="1",
                title="新闻1",
                content="内容1",
                url="url1",
                source="source1",
                category="科技",
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=[]
            ),
            NewsItem(
                id="2",
                title="新闻2",
                content="内容2",
                url="url2",
                source="source2",
                category="科技",
                hot_score=300,
                publish_time="2024-01-02",
                author="author2",
                tags=[]
            ),
            NewsItem(
                id="3",
                title="新闻3",
                content="内容3",
                url="url3",
                source="source3",
                category="科技",
                hot_score=200,
                publish_time="2024-01-03",
                author="author3",
                tags=[]
            )
        ]

        sorted_news = news_processor.sort_news_by_hot(news_list, reverse=True)

        assert sorted_news[0].hot_score == 300
        assert sorted_news[1].hot_score == 200
        assert sorted_news[2].hot_score == 100

    def test_sort_news_by_hot_ascending(self, news_processor):
        """测试按热度升序排序"""
        news_list = [
            NewsItem(
                id="1",
                title="新闻1",
                content="内容1",
                url="url1",
                source="source1",
                category="科技",
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=[]
            ),
            NewsItem(
                id="2",
                title="新闻2",
                content="内容2",
                url="url2",
                source="source2",
                category="科技",
                hot_score=300,
                publish_time="2024-01-02",
                author="author2",
                tags=[]
            ),
            NewsItem(
                id="3",
                title="新闻3",
                content="内容3",
                url="url3",
                source="source3",
                category="科技",
                hot_score=200,
                publish_time="2024-01-03",
                author="author3",
                tags=[]
            )
        ]

        sorted_news = news_processor.sort_news_by_hot(news_list, reverse=False)

        assert sorted_news[0].hot_score == 100
        assert sorted_news[1].hot_score == 200
        assert sorted_news[2].hot_score == 300

    def test_filter_by_category(self, news_processor):
        """测试按分类过滤新闻"""
        news_list = [
            NewsItem(
                id="1",
                title="科技新闻",
                content="内容1",
                url="url1",
                source="source1",
                category=NewsCategory.TECHNOLOGY,
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=[]
            ),
            NewsItem(
                id="2",
                title="体育新闻",
                content="内容2",
                url="url2",
                source="source2",
                category=NewsCategory.SPORTS,
                hot_score=200,
                publish_time="2024-01-02",
                author="author2",
                tags=[]
            ),
            NewsItem(
                id="3",
                title="另一科技新闻",
                content="内容3",
                url="url3",
                source="source3",
                category=NewsCategory.TECHNOLOGY,
                hot_score=300,
                publish_time="2024-01-03",
                author="author3",
                tags=[]
            )
        ]

        tech_news = news_processor.filter_by_category(news_list, NewsCategory.TECHNOLOGY)

        assert len(tech_news) == 2
        assert all(news.category == NewsCategory.TECHNOLOGY for news in tech_news)

    def test_filter_by_keywords_single(self, news_processor):
        """测试按单个关键词过滤"""
        news_list = [
            NewsItem(
                id="1",
                title="AI技术突破",
                content="人工智能技术取得重大突破",
                url="url1",
                source="source1",
                category=NewsCategory.TECHNOLOGY,
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=["AI"]
            ),
            NewsItem(
                id="2",
                title="体育新闻",
                content="NBA总决赛今日开赛",
                url="url2",
                source="source2",
                category=NewsCategory.SPORTS,
                hot_score=200,
                publish_time="2024-01-02",
                author="author2",
                tags=["体育"]
            )
        ]

        filtered_news = news_processor.filter_by_keywords(news_list, "AI")

        assert len(filtered_news) == 1
        assert filtered_news[0].title == "AI技术突破"

    def test_filter_by_keywords_multiple(self, news_processor):
        """测试按多个关键词过滤"""
        news_list = [
            NewsItem(
                id="1",
                title="AI技术突破",
                content="人工智能技术取得重大突破",
                url="url1",
                source="source1",
                category=NewsCategory.TECHNOLOGY,
                hot_score=100,
                publish_time="2024-01-01",
                author="author1",
                tags=["AI"]
            ),
            NewsItem(
                id="2",
                title="AI在体育领域的应用",
                content="人工智能技术在体育领域的应用",
                url="url2",
                source="source2",
                category=NewsCategory.SPORTS,
                hot_score=200,
                publish_time="2024-01-02",
                author="author2",
                tags=["AI", "体育"]
            ),
            NewsItem(
                id="3",
                title="体育新闻",
                content="NBA总决赛今日开赛",
                url="url3",
                source="source3",
                category=NewsCategory.SPORTS,
                hot_score=300,
                publish_time="2024-01-03",
                author="author3",
                tags=["体育"]
            )
        ]

        filtered_news = news_processor.filter_by_keywords(news_list, "AI 体育")

        assert len(filtered_news) == 1
        assert filtered_news[0].title == "AI在体育领域的应用"

    def test_format_news(self, news_processor, sample_news_items):
        """测试格式化新闻"""
        news = sample_news_items[0]
        formatted = news_processor.format_news(news)

        assert isinstance(formatted, dict)
        assert formatted["id"] == "1"
        assert formatted["title"] == "AI技术突破：大模型应用前景广阔"
        assert formatted["category"] == NewsCategory.TECHNOLOGY
