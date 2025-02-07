"""
网页工具模块，提供网页抓取功能
"""

import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List

async def fetch_url(url: str) -> str:
    """
    异步获取单个URL的网页内容并提取文本
    
    Args:
        url: 目标网页URL
        
    Returns:
        清理后的网页文本内容
    """
    async with httpx.AsyncClient() as client:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = await client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            return _clean_text(soup.get_text())
        except httpx.RequestError:
            return ""

def _clean_text(text: str) -> str:
    """清理网页文本"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

async def crawl_web(urls: List[str]) -> List[str]:
    """
    并发抓取多个网页内容
    
    Args:
        urls: 要抓取的URL列表
        
    Returns:
        抓取结果列表，与输入URL顺序一致
    """
    return await asyncio.gather(*(fetch_url(url) for url in urls))