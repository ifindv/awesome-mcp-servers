# mcp-hot-news 模块设计文档

## 1. 模块概述

mcp-hot-news项目采用模块化设计，将系统划分为多个独立的功能模块，每个模块负责特定的功能。这种设计提高了代码的可维护性、可测试性和可扩展性。

## 2. 模块结构

```
src/
├── server.py              # MCP服务器主模块
├── news_fetcher.py        # 新闻数据获取模块
├── news_processor.py      # 新闻数据处理模块
├── news_provider.py       # 新闻提供者接口
└── providers/             # 具体新闻源实现
    ├── base_provider.py   # 基础提供者
    ├── wechat_provider.py # 微信热文提供者
    ├── zhihu_provider.py  # 知乎热榜提供者
    └── weibo_provider.py  # 微博热搜提供者
```

## 3. 核心模块设计

### 3.1 server.py - MCP服务器主模块

#### 3.1.1 模块职责
- 初始化MCP服务器
- 注册新闻相关工具
- 处理客户端请求
- 管理服务器生命周期

#### 3.1.2 类设计

```python
class HotNewsServer:
    """MCP服务器主类"""
    
    def __init__(self):
        """初始化服务器"""
        
    def start(self):
        """启动服务器"""
        
    def stop(self):
        """停止服务器"""
        
    def register_tools(self):
        """注册所有新闻工具"""
        
    def handle_request(self, request):
        """处理客户端请求"""
```

#### 3.1.3 主要接口

| 接口名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| start() | 无 | None | 启动MCP服务器 |
| stop() | 无 | None | 停止MCP服务器 |
| register_tools() | 无 | None | 注册所有新闻工具 |
| handle_request() | request: Request | Response | 处理客户端请求 |

### 3.2 news_fetcher.py - 新闻数据获取模块

#### 3.2.1 模块职责
- 从各新闻源获取原始数据
- 管理数据获取任务队列
- 处理获取异常和重试逻辑

#### 3.2.2 类设计

```python
class NewsFetcher:
    """新闻数据获取器"""
    
    def __init__(self, providers: List[BaseProvider]):
        """初始化获取器"""
        
    async def fetch_all_news(self) -> List[NewsItem]:
        """获取所有新闻源数据"""
        
    async def fetch_news_from_source(self, source: str) -> List[NewsItem]:
        """从指定源获取数据"""
        
    async def fetch_hot_news(self, limit: int = 10) -> List[NewsItem]:
        """获取热点新闻"""
```

#### 3.2.3 主要接口

| 接口名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| fetch_all_news() | 无 | List[NewsItem] | 获取所有新闻源数据 |
| fetch_news_from_source() | source: str | List[NewsItem] | 从指定源获取数据 |
| fetch_hot_news() | limit: int | List[NewsItem] | 获取热点新闻 |

### 3.3 news_processor.py - 新闻数据处理模块

#### 3.3.1 模块职责
- 清洗原始新闻数据
- 去重和过滤
- 分类和排序
- 格式化输出

#### 3.3.2 类设计

```python
class NewsProcessor:
    """新闻数据处理器"""
    
    def __init__(self):
        """初始化处理器"""
        
    def process_raw_data(self, raw_data: List[Dict]) -> List[NewsItem]:
        """处理原始数据"""
        
    def deduplicate_news(self, news_list: List[NewsItem]) -> List[NewsItem]:
        """新闻去重"""
        
    def categorize_news(self, news: NewsItem) -> str:
        """新闻分类"""
        
    def format_news(self, news: NewsItem) -> Dict:
        """格式化新闻输出"""
```

#### 3.3.3 主要接口

| 接口名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| process_raw_data() | raw_data: List[Dict] | List[NewsItem] | 处理原始数据 |
| deduplicate_news() | news_list: List[NewsItem] | List[NewsItem] | 新闻去重 |
| categorize_news() | news: NewsItem | str | 新闻分类 |
| format_news() | news: NewsItem | Dict | 格式化新闻输出 |

### 3.4 news_provider.py - 新闻提供者接口

#### 3.4.1 模块职责
- 定义新闻提供者接口规范
- 实现通用的数据处理逻辑

#### 3.4.2 类设计

```python
class BaseProvider(ABC):
    """新闻提供者基类"""
    
    @abstractmethod
    async def fetch(self) -> List[Dict]:
        """获取新闻数据"""
        
    @abstractmethod
    def parse(self, html: str) -> List[Dict]:
        """解析新闻数据"""
        
    def normalize(self, raw_item: Dict) -> NewsItem:
        """标准化新闻数据格式"""
```

#### 3.4.3 主要接口

| 接口名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| fetch() | 无 | List[Dict] | 获取新闻数据 |
| parse() | html: str | List[Dict] | 解析新闻数据 |
| normalize() | raw_item: Dict | NewsItem | 标准化新闻数据格式 |

### 3.5 providers/ - 具体新闻源实现

#### 3.5.1 base_provider.py

##### 模块职责
- 实现基础提供者类
- 提供通用功能

##### 类设计

```python
class BaseProvider(ABC):
    """新闻提供者基类"""
    
    def __init__(self, name: str, url: str):
        """初始化提供者"""
        
    async def fetch(self) -> List[Dict]:
        """获取新闻数据"""
        
    def parse(self, html: str) -> List[Dict]:
        """解析新闻数据"""
        
    def normalize(self, raw_item: Dict) -> NewsItem:
        """标准化新闻数据格式"""
```

#### 3.5.2 wechat_provider.py

##### 模块职责
- 实现微信热文数据获取
- 处理微信特有格式

##### 类设计

```python
class WechatProvider(BaseProvider):
    """微信热文提供者"""
    
    def __init__(self):
        """初始化微信提供者"""
        
    async def fetch(self) -> List[Dict]:
        """获取微信热文数据"""
        
    def parse(self, html: str) -> List[Dict]:
        """解析微信热文数据"""
        
    def normalize(self, raw_item: Dict) -> NewsItem:
        """标准化微信热文数据格式"""
```

#### 3.5.3 zhihu_provider.py

##### 模块职责
- 实现知乎热榜数据获取
- 处理知乎特有格式

##### 类设计

```python
class ZhihuProvider(BaseProvider):
    """知乎热榜提供者"""
    
    def __init__(self):
        """初始化知乎提供者"""
        
    async def fetch(self) -> List[Dict]:
        """获取知乎热榜数据"""
        
    def parse(self, html: str) -> List[Dict]:
        """解析知乎热榜数据"""
        
    def normalize(self, raw_item: Dict) -> NewsItem:
        """标准化知乎热榜数据格式"""
```

#### 3.5.4 weibo_provider.py

##### 模块职责
- 实现微博热搜数据获取
- 处理微博特有格式

##### 类设计

```python
class WeiboProvider(BaseProvider):
    """微博热搜提供者"""
    
    def __init__(self):
        """初始化微博提供者"""
        
    async def fetch(self) -> List[Dict]:
        """获取微博热搜数据"""
        
    def parse(self, html: str) -> List[Dict]:
        """解析微博热搜数据"""
        
    def normalize(self, raw_item: Dict) -> NewsItem:
        """标准化微博热搜数据格式"""
```

## 4. 数据模型

### 4.1 NewsItem

```python
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
```

### 4.2 NewsRequest

```python
@dataclass
class NewsRequest:
    """新闻请求模型"""
    source: Optional[str]       # 新闻源
    category: Optional[str]     # 新闻分类
    keywords: Optional[str]     # 关键词
    limit: int                  # 数量限制
    offset: int                 # 偏移量
```

## 5. 模块交互

### 5.1 获取热点新闻流程

```
AI Agent
    ↓
HotNewsServer.handle_request()
    ↓
NewsFetcher.fetch_hot_news()
    ↓
WechatProvider.fetch()
ZhihuProvider.fetch()
WeiboProvider.fetch()
    ↓
NewsProcessor.process_raw_data()
    ↓
NewsProcessor.deduplicate_news()
    ↓
NewsProcessor.format_news()
    ↓
HotNewsServer返回结果
```

### 5.2 搜索新闻流程

```
AI Agent
    ↓
HotNewsServer.handle_request()
    ↓
NewsFetcher.fetch_all_news()
    ↓
NewsProcessor.process_raw_data()
    ↓
NewsProcessor.filter_by_keywords()
    ↓
NewsProcessor.format_news()
    ↓
HotNewsServer返回结果
```

## 6. 异常处理

### 6.1 异常类型

```python
class NewsFetchError(Exception):
    """新闻获取异常"""
    
class NewsParseError(Exception):
    """新闻解析异常"""
    
class NewsProcessError(Exception):
    """新闻处理异常"""
```

### 6.2 异常处理策略

- 获取失败时记录日志并返回空列表
- 解析失败时跳过该条新闻
- 处理失败时返回错误信息

## 7. 性能优化

### 7.1 缓存策略

- 使用内存缓存新闻数据
- 缓存时间30分钟
- 支持手动刷新

### 7.2 并发控制

- 使用异步IO获取数据
- 限制并发数量
- 实现超时机制

## 8. 扩展性设计

### 8.1 新增新闻源

1. 继承BaseProvider类
2. 实现fetch()方法
3. 实现parse()方法
4. 重写normalize()方法（可选）
5. 注册到NewsFetcher

### 8.2 新增功能

1. 在HotNewsServer中注册新工具
2. 实现工具处理函数
3. 添加必要的模型类
4. 更新文档

## 9. 测试策略

### 9.1 单元测试

- 测试每个模块的核心功能
- 模拟外部依赖
- 覆盖边界情况

### 9.2 集成测试

- 测试模块间交互
- 测试完整流程
- 验证数据一致性

## 10. 文档维护

### 10.1 代码文档

- 使用docstring记录类和方法
- 说明参数和返回值
- 提供使用示例

### 10.2 设计文档

- 及时更新设计文档
- 记录重要变更
- 维护架构图
