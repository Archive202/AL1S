"""
DuckDuckGo 搜索工具模块，提供网页搜索和内容抓取功能
"""

from typing import List
import asyncio
from duckduckgo_search import DDGS
from utils.web_utils import crawl_web

def search_duckduckgo(keywords: List[str]) -> List[str]:
    """
    使用 DuckDuckGo 进行搜索并抓取网页内容
    
    Args:
        keywords: 搜索关键词列表
        
    Returns:
        包含抓取结果的字符串列表
    """
    search_term = " ".join(keywords)
    results = DDGS().text(
        keywords=search_term,
        region="cn-zh",
        safesearch="on",
        max_results=5,
        backend="html",
    )
    urls = [result["href"] for result in results]
    return asyncio.run(crawl_web(urls))