# mcp-hot-news 测试文档

## 1. 测试概述

### 1.1 测试目标
- 确保代码功能正确性
- 验证系统稳定性
- 保证代码质量

### 1.2 测试范围
- 单元测试
- 集成测试
- 性能测试

## 2. 测试环境

### 2.1 环境要求
- Python 3.8+
- pytest
- pytest-cov
- pytest-asyncio

### 2.2 环境搭建

```bash
# 安装测试依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/
```

## 3. 测试用例

### 3.1 单元测试

#### 3.1.1 数据模型测试

测试目标：
- 验证NewsItem数据模型的正确性
- 验证NewsRequest数据模型的正确性
- 验证NewsCategory常量的正确性

测试方法：
```python
def test_news_item():
    news = NewsItem(
        id="1",
        title="测试新闻",
        content="测试内容",
        url="https://example.com",
        source="测试源",
        category="科技",
        hot_score=100,
        publish_time="2024-01-01",
        author="测试作者",
        tags=["测试", "新闻"]
    )
    assert news.title == "测试新闻"
    assert news.hot_score == 100
```

#### 3.1.2 新闻提供者测试

测试目标：
- 验证BaseProvider接口的正确性
- 验证各Provider实现的功能

测试方法：
```python
@pytest.mark.asyncio
async def test_wechat_provider():
    provider = WechatProvider()
    data = await provider.fetch()
    assert isinstance(data, list)
    for item in data:
        assert "title" in item
        assert "url" in item
```

#### 3.1.3 新闻获取器测试

测试目标：
- 验证NewsFetcher的功能
- 验证缓存机制

测试方法：
```python
@pytest.mark.asyncio
async def test_news_fetcher():
    fetcher = NewsFetcher()
    news = await fetcher.fetch_hot_news(limit=10)
    assert len(news) <= 10
    assert all(isinstance(n, NewsItem) for n in news)
```

#### 3.1.4 新闻处理器测试

测试目标：
- 验证NewsProcessor的功能
- 验证数据处理逻辑

测试方法：
```python
def test_news_processor():
    processor = NewsProcessor()
    news_list = [
        NewsItem(
            id="1",
            title="AI技术突破",
            content="人工智能技术取得重大突破",
            url="https://example.com",
            source="测试源",
            category="科技",
            hot_score=100,
            publish_time="2024-01-01",
            author="测试作者",
            tags=["AI", "科技"]
        )
    ]
    filtered = processor.filter_by_category(news_list, "科技")
    assert len(filtered) == 1
    assert filtered[0].category == "科技"
```

### 3.2 集成测试

#### 3.2.1 完整流程测试

测试目标：
- 验证从获取到处理的完整流程
- 验证各模块间的协作

测试方法：
```python
@pytest.mark.asyncio
async def test_full_workflow():
    fetcher = NewsFetcher()
    processor = NewsProcessor()
    
    # 获取新闻
    news = await fetcher.fetch_hot_news(limit=10)
    
    # 处理新闻
    deduplicated = processor.deduplicate_news(news)
    categorized = processor.batch_categorize_news(deduplicated)
    
    assert len(categorized) > 0
    assert all(n.category != NewsCategory.OTHER for n in categorized)
```

### 3.3 性能测试

#### 3.3.1 响应时间测试

测试目标：
- 验证API响应时间
- 验证缓存效果

测试方法：
```python
@pytest.mark.asyncio
async def test_performance():
    fetcher = NewsFetcher()
    
    # 测试首次请求
    start = time.time()
    news1 = await fetcher.fetch_hot_news(limit=10)
    first_time = time.time() - start
    
    # 测试缓存请求
    start = time.time()
    news2 = await fetcher.fetch_hot_news(limit=10)
    cached_time = time.time() - start
    
    # 缓存请求应该更快
    assert cached_time < first_time
```

## 4. 测试覆盖率

### 4.1 覆盖率目标
- 语句覆盖率：>= 80%
- 分支覆盖率：>= 70%

### 4.2 生成覆盖率报告

```bash
# 生成覆盖率报告
pytest --cov=src tests/

# 生成HTML报告
pytest --cov=src --cov-report=html tests/
```

## 5. 测试策略

### 5.1 测试优先级
1. 核心功能测试
2. 边界条件测试
3. 异常处理测试
4. 性能测试

### 5.2 测试数据

使用测试数据而非真实数据：
- 模拟HTTP响应
- 使用固定测试数据
- 避免依赖外部服务

## 6. 持续集成

### 6.1 CI配置

在CI环境中运行测试：
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/ --cov=src
```

## 7. 测试最佳实践

### 7.1 编写测试

1. 每个测试只验证一个功能
2. 使用描述性的测试名称
3. 保持测试简洁
4. 使用fixtures共享测试数据

### 7.2 运行测试

1. 定期运行测试
2. 在提交前运行测试
3. 在CI中运行测试

### 7.3 维护测试

1. 及时更新测试
2. 保持测试代码质量
3. 删除过时的测试

## 8. 常见问题

### 8.1 测试失败

问题：测试失败

解决方案：
1. 查看错误信息
2. 检查测试代码
3. 检查被测代码
4. 修复问题

### 8.2 测试超时

问题：测试超时

解决方案：
1. 增加超时时间
2. 优化测试代码
3. 使用模拟数据

## 9. 测试报告

### 9.1 报告内容
- 测试结果摘要
- 覆盖率报告
- 失败测试详情
- 性能指标

### 9.2 报告生成

```bash
# 生成测试报告
pytest tests/ --html=test_report.html

# 生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```
