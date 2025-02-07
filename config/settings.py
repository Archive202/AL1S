"""
应用程序配置模块，包含环境变量加载和全局配置
"""

import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

PROGRAM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# OpenAI API 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
CHAT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# 语音识别配置
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
RECOGNIZER_ENGINE = os.getenv("RECOGNIZER_ENGINE", "google")
WAKE_WORD_PATHS = {
    "爱丽丝": os.path.join(PROGRAM_DIR, "assets", "wakewords", "爱丽丝_zh_windows_v3_0_0.ppn"),
    "porcupine_params": os.path.join(PROGRAM_DIR, "assets", "wakewords", "porcupine_params_zh.pv"),
}

# MQTT 配置
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# GSV 配置
GSV_BASE_URL = os.getenv("GSV_BASE_URL")
REF_AUDIO_PATH = os.getenv("REF_AUDIO_PATH")
PROMPT_TEXT = urllib.parse.quote(os.getenv("PROMPT_TEXT"))
PROMPT_LANG = os.getenv("PROMPT_LANG")

# 音频文件路径
WAKE_SOUND_PATH = os.path.join(PROGRAM_DIR, "assets", "sounds", "wake_sound.mp3")
DOWN_SOUND_PATH = os.path.join(PROGRAM_DIR, "assets", "sounds", "down_sound.mp3")