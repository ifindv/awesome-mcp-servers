"""
新闻提供者模块
"""
from .base_provider import BaseProvider
from .wechat_provider import WechatProvider
from .zhihu_provider import ZhihuProvider
from .weibo_provider import WeiboProvider


__all__ = [
    'BaseProvider',
    'WechatProvider',
    'ZhihuProvider',
    'WeiboProvider'
]
