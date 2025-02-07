"""
语音处理包，导出语音识别、唤醒词检测和 TTS 模块中的类
"""

from .wake_word import WakeWordDetector
from .speech_recognition import SpeechRecognizer
from .tts import TextToSpeech

__all__ = [
    "WakeWordDetector",
    "SpeechRecognizer",
    "TextToSpeech",
]