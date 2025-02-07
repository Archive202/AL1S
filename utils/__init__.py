"""
工具函数包，导出网页抓取工具
"""

from .web_utils import fetch_url, crawl_web

__all__ = [
    "fetch_url",
    "crawl_web",
]