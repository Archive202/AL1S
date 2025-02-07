"""
日期时间工具模块，提供当前时间获取功能
"""

from datetime import datetime

def get_current_datetime() -> str:
    """
    获取当前日期时间的字符串表示
    
    Returns:
        格式化的当前日期时间字符串
    """
    return str(datetime.now())