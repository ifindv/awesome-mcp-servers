# mcp-hot-news 使用文档

## 1. 安装

### 1.1 环境要求
- Python 3.8+
- pip

### 1.2 安装步骤

```bash
# 克隆项目
git clone https://github.com/yourusername/mcp-hot-news.git
cd mcp-hot-news

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 2. 配置

### 2.1 基本配置

项目默认配置即可运行，无需额外配置。

### 2.2 高级配置

如需自定义配置，可以创建`config.py`文件：

```python
# config.py

# 缓存配置
CACHE_DURATION = 1800  # 缓存时长（秒）

# 请求配置
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）
MAX_CONCURRENT_REQUESTS = 5  # 最大并发请求数

# 日志配置
LOG_LEVEL = "INFO"  # 日志级别
```

## 3. 使用方法

### 3.1 启动服务

```bash
python -m src.server
```

### 3.2 MCP工具使用

#### 3.2.1 获取热点新闻

```python
# 获取前10条热点新闻
get_hot_news(limit=10)
```

#### 3.2.2 按新闻源获取新闻

```python
# 获取微信热文
get_news_by_source(source="微信", limit=10)

# 获取知乎热榜
get_news_by_source(source="知乎", limit=10)

# 获取微博热搜
get_news_by_source(source="微博", limit=10)
```

#### 3.2.3 按分类获取新闻

```python
# 获取科技新闻
get_news_by_category(category="科技", limit=10)

# 获取娱乐新闻
get_news_by_category(category="娱乐", limit=10)
```

#### 3.2.4 搜索新闻

```python
# 搜索关键词
search_news(keywords="人工智能", limit=10)
```

#### 3.2.5 获取新闻分类

```python
# 获取所有可用分类
get_news_categories()
```

#### 3.2.6 获取新闻源

```python
# 获取所有可用新闻源
get_news_sources()
```

## 4. API响应格式

所有API响应都遵循以下格式：

```json
{
  "success": true,
  "data": [...],
  "total": 10
}
```

错误响应格式：

```json
{
  "success": false,
  "error": "错误信息",
  "data": [],
  "total": 0
}
```

## 5. 新闻数据格式

```json
{
  "id": "新闻唯一标识",
  "title": "新闻标题",
  "content": "新闻内容摘要",
  "url": "新闻链接",
  "source": "新闻源",
  "category": "新闻分类",
  "hot_score": 100,
  "publish_time": "发布时间",
  "author": "作者/来源",
  "tags": ["标签1", "标签2"]
}
```

## 6. 示例

### 6.1 Python示例

```python
import asyncio
from src.server import HotNewsServer

async def main():
    server = HotNewsServer()
    # 获取热点新闻
    result = await server.fetcher.fetch_hot_news(limit=10)
    for news in result:
        print(f"{news.title} - {news.hot_score}")

asyncio.run(main())
```

### 6.2 MCP客户端示例

```python
from mcp.client import Client

async def main():
    client = Client()
    await client.connect()
    
    # 获取热点新闻
    result = await client.call_tool("get_hot_news", {"limit": 10})
    print(result)
    
    # 搜索新闻
    result = await client.call_tool("search_news", {"keywords": "人工智能"})
    print(result)

asyncio.run(main())
```

## 7. 故障排除

### 7.1 常见问题

#### 问题1：无法连接到新闻源

**解决方案：**
- 检查网络连接
- 确认新闻源URL是否正确
- 检查防火墙设置

#### 问题2：数据获取失败

**解决方案：**
- 查看日志文件
- 检查新闻源是否正常
- 尝试清除缓存

#### 问题3：性能问题

**解决方案：**
- 调整缓存时长
- 减少并发请求数
- 优化过滤条件

## 8. 最佳实践

### 8.1 性能优化

1. 合理使用缓存
2. 限制返回数量
3. 使用精确的搜索关键词

### 8.2 错误处理

1. 检查响应中的success字段
2. 处理错误响应
3. 记录错误日志

### 8.3 安全建议

1. 不要暴露敏感信息
2. 实现访问控制
3. 定期更新依赖

## 9. 更新日志

### v0.1.0 (2024-01-01)

- 初始版本发布
- 支持微信、知乎、微博三个新闻源
- 实现基本的热点新闻获取功能
- 实现新闻搜索功能
