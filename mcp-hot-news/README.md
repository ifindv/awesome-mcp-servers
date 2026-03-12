# mcp-hot-news

一个基于MCP (Model Context Protocol)的新闻热点服务，为AI Agent提供实时新闻热点数据。

## 功能特性

- 获取今日热点新闻
- 按分类获取新闻（科技、娱乐、体育等）
- 获取新闻详情
- 关键词搜索新闻
- 获取新闻趋势分析

## 支持的新闻源

- 微信热文
- 知乎热榜
- 微博热搜
- 澎湃新闻

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/ifindv/awesome-mcp-servers.git
cd awesome-mcp-servers/mcp-hot-news

# 安装依赖
pip install -r requirements.txt

# 或者使用 setup.py 安装
pip install -e .
```

### 从 PyPI 安装（如果已发布）

```bash
pip install mcp-hot-news
```

## 使用方法

### MCP 客户端配置

在您的 MCP 客户端配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "python",
      "args": ["e:\\YOUR_WORK_PATH\\awesome-mcp-servers\\mcp-hot-news\\src\\server.py"]
    }
  }
}
```

### 可用工具

1. **get_hot_news** - 获取今日热点新闻

   - 参数：limit (可选，默认10)
2. **get_news_by_source** - 从指定新闻源获取新闻

   - 参数：source (必需，可选值：微信、知乎、微博、澎湃)
   - 参数：limit (可选，默认10)
3. **get_news_by_category** - 按分类获取新闻

   - 参数：category (必需，可选值：科技、娱乐、体育、财经、社会、国际、其他)
   - 参数：limit (可选，默认10)
4. **search_news** - 搜索新闻

   - 参数：keywords (必需)
   - 参数：limit (可选，默认10)
   - 参数：offset (可选，默认0)

## 开发

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/
```

## 许可证

MIT
