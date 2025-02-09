"""
语音识别模块，支持多种语音识别引擎
"""

from io import BytesIO
import speech_recognition as sr
from openai import OpenAI
from config.settings import RECOGNIZER_ENGINE, CUSTOM_RECOGNIZER_API_KEY, CUSTOM_RECOGNIZER_BASE_URL, CUSTOM_RECOGNIZER_MODEL

class SpeechRecognizer:
    """语音识别器"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.operation_timeout = 5
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.pause_threshold = 1.5
        
    def listen(self) -> str:
        """
        监听麦克风输入并进行语音识别
        
        Returns:
            识别出的文本内容
            
        Raises:
            sr.UnknownValueError: 当无法识别语音时
            sr.RequestError: 当识别服务出错时
        """
        print("输入: ", end="")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source=source, duration=2)
            audio = self.recognizer.listen(source, timeout=20)
            
        if RECOGNIZER_ENGINE == "custom":
            return self._regonize_custom(
                audio=audio,
                api_key=CUSTOM_RECOGNIZER_API_KEY, 
                base_url=CUSTOM_RECOGNIZER_BASE_URL, 
                model=CUSTOM_RECOGNIZER_MODEL)
        elif RECOGNIZER_ENGINE == "google":
            return self.recognizer.recognize_google(audio, language="zh-CN")
        else:
            raise ValueError(f"不支持的识别引擎: {RECOGNIZER_ENGINE}")
        
    def _regonize_custom(self, audio, api_key, base_url, model) -> str:
        """使用自定义语音识别引擎"""
        transcribe_client = OpenAI(api_key=api_key, base_url=base_url)
        audio_file = BytesIO(audio.get_wav_data())
        audio_file.name = "SpeechRecognition_audio.wav"
        transcription = transcribe_client.audio.transcriptions.create(
            file=audio_file,
            model=model, 
        )
        if transcription.text == "":
            raise sr.UnknownValueError
        return transcription.text