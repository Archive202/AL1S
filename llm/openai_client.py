"""
OpenAI 客户端模块，处理与 LLM 的交互
"""

from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_BASE_URL, CHAT_MODEL

class OpenAIClient:
    """OpenAI 客户端"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )
        self.conversation_history = []
        
    def chat_completion(self, tools: list = None):
        """
        执行聊天补全请求
        
        Args:
            tools: 可用的工具列表
            
        Returns:
            聊天补全响应对象
        """
        completion = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=self.conversation_history,
            tools=tools,
            timeout=5,
        )
        self.conversation_history.append(completion.choices[0].message)
        return completion