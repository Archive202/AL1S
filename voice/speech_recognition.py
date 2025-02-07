"""
语音识别模块，支持多种语音识别引擎
"""

import os
import speech_recognition as sr
from config.settings import RECOGNIZER_ENGINE

class SpeechRecognizer:
    """语音识别器"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.operation_timeout = 10
        
    def listen(self) -> str:
        """
        监听麦克风输入并进行语音识别
        
        Returns:
            识别出的文本内容
            
        Raises:
            sr.UnknownValueError: 当无法识别语音时
            sr.RequestError: 当识别服务出错时
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source=source, duration=2)
            audio = self.recognizer.listen(source, timeout=20)
            
        if RECOGNIZER_ENGINE == "google":
            return self.recognizer.recognize_google(audio, language="zh-CN")
        elif RECOGNIZER_ENGINE == "azure":
            return self._recognize_azure(audio)
        else:
            raise ValueError(f"不支持的识别引擎: {RECOGNIZER_ENGINE}")
            
    def _recognize_azure(self, audio):
        """使用 Azure 语音识别"""
        azure_key = os.getenv("AZURE_KEY")
        azure_location = os.getenv("AZURE_LOCATION", "eastus")
        return self.recognizer.recognize_azure(
            audio,
            key=azure_key,
            location=azure_location,
            language="zh-CN",
        )[0]