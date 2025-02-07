"""
大语言模型包，导出 OpenAI 客户端和函数调用处理器
"""

from .openai_client import OpenAIClient
from .function_calling import FunctionCaller

__all__ = [
    "OpenAIClient",
    "FunctionCaller",
]