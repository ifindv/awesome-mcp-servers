"""
mcp-hot-news 安装配置
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-hot-news",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="MCP server for hot news from WeChat, Zhihu and Weibo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-hot-news",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mcp>=1.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "aiohttp>=3.8.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.3",
    ],
    entry_points={
        "console_scripts": [
            "mcp-hot-news=server:main",
        ],
    },
)
