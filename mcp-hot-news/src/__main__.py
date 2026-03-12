"""
mcp-hot-news 主入口
"""
import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main())
