"""
新闻提供者模块
"""
from .base_provider import BaseProvider
from .wechat_provider import WechatProvider
from .zhihu_provider import ZhihuProvider
from .weibo_provider import WeiboProvider
from .thepaper_provider import ThepaperProvider


__all__ = [
    'BaseProvider',
    'WechatProvider',
    'ZhihuProvider',
    'WeiboProvider',
    'ThepaperProvider'
]
