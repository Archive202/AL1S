"""
文本转语音模块，支持多种 TTS 引擎
"""

import urllib.parse
import time
import vlc
from config.settings import GSV_BASE_URL, REF_AUDIO_PATH, PROMPT_TEXT, PROMPT_LANG

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