"""
函数调用处理模块，管理工具函数和调用
"""

import json
from typing import Any, Dict
from tools import duckduckgo, mqtt_client, datetime_provider

class FunctionCaller:
    """函数调用处理器"""
    
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "search_duckduckgo",
                "description": "使用DuckDuckGo搜索引擎查询信息。可以搜索最新新闻、文章、博客等内容。",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "搜索的关键词列表。例如：['Python', '机器学习', '最新进展']。",
                        }
                    },
                    "required": ["keywords"],
                    "addtionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "send_mqtt_message",
                "description": "发送 MQTT 消息到指定主题",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "MQTT 主题，例如：test/topic",
                        },
                        "message": {
                            "type": "string",
                            "description": "要发送的消息内容",
                        },
                    },
                    "required": ["topic", "message"],
                    "addtionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_datetime",
                "description": "获取当前的日期和时间",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "addtionalProperties": False,
                },
            },
        },
    ]
    
    FUNCTION_MAP = {
        "search_duckduckgo": duckduckgo.search_duckduckgo,
        "send_mqtt_message": mqtt_client.send_mqtt_message,
        "get_current_datetime": datetime_provider.get_current_datetime
    }
    
    @classmethod
    def call_function(cls, name: str, arguments: Dict[str, Any]) -> Any:
        """
        调用指定函数并返回结果
        
        Args:
            name: 函数名称
            arguments: 函数参数
            
        Returns:
            函数调用结果
        """
        func = cls.FUNCTION_MAP[name]
        return func(**arguments)