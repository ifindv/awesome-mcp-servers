"""MCP服务器主模块"""
import sys
import os
import asyncio
import logging
from typing import Dict, Any, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_fetcher import NewsFetcher
from news_processor import NewsProcessor
from models import NewsRequest, NewsCategory


# 配置日志
# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 设置日志文件路径
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'mcp-hot-news.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class HotNewsServer:
    """MCP服务器主类"""

    def __init__(self):
        """初始化服务器"""
        self.server = Server("mcp-hot-news", "0.1.0")
        self.fetcher = NewsFetcher()
        self.processor = NewsProcessor()
        self._register_tools()

    def _register_tools(self):
        """注册所有新闻工具"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """列出可用工具"""
            return [
                Tool(
                    name="get_hot_news",
                    description="获取今日热点新闻",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "number",
                                "description": "返回数量限制，默认为10",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="get_news_by_source",
                    description="从指定新闻源获取新闻",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source": {
                                "type": "string",
                                "description": "新闻源名称（微信、知乎、微博、澎湃）",
                                "enum": ["微信", "知乎", "微博", "澎湃"]
                            },
                            "limit": {
                                "type": "number",
                                "description": "返回数量限制，默认为10",
                                "default": 10
                            }
                        },
                        "required": ["source"]
                    }
                ),
                Tool(
                    name="get_news_by_category",
                    description="按分类获取新闻",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "新闻分类",
                                "enum": ["科技", "娱乐", "体育", "财经", "社会", "国际", "其他"]
                            },
                            "limit": {
                                "type": "number",
                                "description": "返回数量限制，默认为10",
                                "default": 10
                            }
                        },
                        "required": ["category"]
                    }
                ),
                Tool(
                    name="search_news",
                    description="搜索新闻",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "string",
                                "description": "搜索关键词"
                            },
                            "limit": {
                                "type": "number",
                                "description": "返回数量限制，默认为10",
                                "default": 10
                            },
                            "offset": {
                                "type": "number",
                                "description": "偏移量，默认为0",
                                "default": 0
                            }
                        },
                        "required": ["keywords"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """调用工具"""
            try:
                if name == "get_hot_news":
                    limit = arguments.get("limit", 10)
                    if not isinstance(limit, int) or limit <= 0:
                        return [TextContent(type="text", text="Error: limit must be a positive integer")]

                    news_list = await self.fetcher.fetch_hot_news(limit=limit)
                    result = [self.processor.format_news(news) for news in news_list]
                    return [TextContent(type="text", text=str(result))]

                elif name == "get_news_by_source":
                    source = arguments.get("source")
                    if not source:
                        return [TextContent(type="text", text="Error: source is required")]

                    limit = arguments.get("limit", 10)
                    if not isinstance(limit, int) or limit <= 0:
                        return [TextContent(type="text", text="Error: limit must be a positive integer")]

                    try:
                        news_list = await self.fetcher.fetch_news_from_source(source)
                    except Exception as e:
                        logger.error(f"Error fetching from source {source}: {str(e)}")
                        return [TextContent(type="text", text=f"Error: 获取新闻失败 - {str(e)}")]

                    sorted_news = self.processor.sort_news_by_hot(news_list)
                    result = [self.processor.format_news(news) for news in sorted_news[:limit]]
                    return [TextContent(type="text", text=str(result))]

                elif name == "get_news_by_category":
                    category = arguments.get("category")
                    if not category:
                        return [TextContent(type="text", text="Error: category is required")]

                    limit = arguments.get("limit", 10)
                    if not isinstance(limit, int) or limit <= 0:
                        return [TextContent(type="text", text="Error: limit must be a positive integer")]

                    all_news = await self.fetcher.fetch_all_news()
                    categorized_news = self.processor.filter_by_category(all_news, category)
                    sorted_news = self.processor.sort_news_by_hot(categorized_news)
                    result = [self.processor.format_news(news) for news in sorted_news[:limit]]
                    return [TextContent(type="text", text=str(result))]

                elif name == "search_news":
                    keywords = arguments.get("keywords")
                    if not keywords:
                        return [TextContent(type="text", text="Error: keywords is required")]

                    limit = arguments.get("limit", 10)
                    if not isinstance(limit, int) or limit <= 0:
                        return [TextContent(type="text", text="Error: limit must be a positive integer")]

                    offset = arguments.get("offset", 0)
                    if not isinstance(offset, int) or offset < 0:
                        return [TextContent(type="text", text="Error: offset must be a non-negative integer")]

                    request = NewsRequest(
                        keywords=keywords,
                        limit=limit,
                        offset=offset
                    )
                    news_list = await self.fetcher.search_news(request)
                    result = [self.processor.format_news(news) for news in news_list]
                    return [TextContent(type="text", text=str(result))]

                else:
                    return [TextContent(type="text", text=f"Error: Unknown tool name: {name}")]

            except Exception as e:
                logger.error(f"Unexpected error calling tool {name}: {str(e)}")
                return [TextContent(type="text", text=f"Error: 服务器内部错误 - {str(e)}")]

    async def run(self):
        """运行服务器"""
        logger.info("Starting mcp-hot-news server...")
        async with stdio_server() as streams:
            await self.server.run(
                streams[0],
                streams[1],
                self.server.create_initialization_options()
            )


async def main():
    """主函数"""
    server = HotNewsServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
