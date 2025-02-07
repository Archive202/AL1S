"""
唤醒词检测模块，使用 Porcupine 进行语音唤醒检测
"""

import numpy as np
import pyaudio
import pvporcupine
from pydub import AudioSegment
from pydub.playback import play
from config.settings import PICOVOICE_ACCESS_KEY, WAKE_WORD_PATHS, WAKE_SOUND_PATH

class WakeWordDetector:
    """唤醒词检测器"""
    
    def __init__(self):
        """
        初始化 Porcupine 唤醒词检测引擎
        """
        self.porcupine = pvporcupine.create(
            keywords=["爱丽丝"],
            access_key=PICOVOICE_ACCESS_KEY,
            keyword_paths=[WAKE_WORD_PATHS["爱丽丝"]],
            model_path=WAKE_WORD_PATHS["porcupine_params"],
        )

    def detect(self):
        """
        持续监听麦克风输入，直到检测到唤醒词
        """
        pa = pyaudio.PyAudio()
        
        stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )
            
        print("等待唤醒...")
        while True:
            pcm = stream.read(self.porcupine.frame_length)
            pcm = np.frombuffer(pcm, dtype=np.int16)
            if self.porcupine.process(pcm) >= 0:
                wake_sound = AudioSegment.from_file(WAKE_SOUND_PATH)
                play(wake_sound)
                break
        
        if 'stream' in locals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        pa.terminate()
