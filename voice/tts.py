"""
文本转语音模块，支持多种 TTS 引擎
"""

import urllib.parse
import time
import vlc
from openai import OpenAI
import pyaudio
from config import GSV_BASE_URL, REF_AUDIO_PATH, PROMPT_TEXT, PROMPT_LANG
# from config import GSV_API_KEY, GSV_BASE_URL, GSV_MODEL, GSV_VOICE

class TextToSpeech:
    """文本转语音处理器"""
    
    def speak(self, text: str):
        """
        将文本转换为语音并播放
        
        Args:
            text: 要转换的文本内容
        """
        input_text = urllib.parse.quote(text)
        audio_url = f"{GSV_BASE_URL}?text={input_text}&text_lang=auto&ref_audio_path={REF_AUDIO_PATH}&prompt_text={PROMPT_TEXT}&prompt_lang={PROMPT_LANG}&streaming_mode=true&text_split_method=cut1"
        player = vlc.MediaPlayer(audio_url)
        player.play()
        self._wait_playback(player)
        
    def _wait_playback(self, player):
        """等待播放完成"""
        time.sleep(1)  # 初始缓冲
        while player.get_state() not in [vlc.State.Ended, vlc.State.Error]:
            time.sleep(0.5)

    # def speak(self, text: str):
    #     """
    #     使用OpenAI API标准将文本转换为语音并播放
        
    #     Args:
    #         text: 要转换的文本内容
    #     """
    #     player_stream = pyaudio.PyAudio().open(
    #         format=pyaudio.paInt16,
    #         channels=1,
    #         rate=32000,
    #         output=True
    #     )

    #     tts_client = OpenAI(api_key=GSV_API_KEY, base_url=GSV_BASE_URL)
    #     with tts_client.audio.speech.with_streaming_response.create(
    #         input=text,
    #         model=GSV_MODEL,
    #         voice=GSV_VOICE,
    #         response_format="pcm",
    #         # extra_body=
    #     ) as response:
    #         for chunk in response.iter_bytes(chunk_size=1024):
    #             player_stream.write(chunk)