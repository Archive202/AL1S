<div align="center">

# AL1S

嘿嘿爱丽丝可爱捏，总之今天爱丽丝来夏莱当值日生了~  🌸

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge)](https://www.python.org/downloads/) 
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg?style=for-the-badge)](https://platform.openai.com/) 
[![License](https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge)](https://github.com/Archive202/AL1S/blob/main/LICENSE)

[**English**](/README.md) | **中文简体**

</div>

---

## ✨ 功能 Features

- 🎤 语音唤醒 ("爱丽丝")
- 🗣️ 中文语音识别
- 🤖 基于AI的聊天能力 (OpenAI API)
- 🔊 GPT-Sovits 文本转语音
- 🔍 基于 Function Calling API 实现 mqtt 控制、网络搜索等

## 🛠️ 环境要求 Requirements

- 🐍 Python 3.10+
- (必需) [uv](https://github.com/astral-sh/uv) Python 包管理器
- (必需) OpenAI API key
- (必需) [GPT-Sovits](https://github.com/RVC-Boss/GPT-SoVITS) API
- (必需) [Picovoice](https://console.picovoice.ai/) Access Key
- (可选) Speech-To-Text AI API (例如: [SenseVoice](https://github.com/FunAudioLLM/SenseVoice))
- 🎤 麦克风
- (可选) MQTT 服务器

## 📦 安装 Installation

1. 克隆本仓库:
   ```bash
   git clone https://github.com/Archive202/AL1S.git
   cd AL1S
   ```

2. 安装 portaudio 运行库 (pyaudio 的依赖):
   - Linux (apt): `sudo apt install portaudio19-dev`
   - macOS: `brew install portaudio`

3. 使用 [uv](https://hellowac.github.io/uv-zh-cn/getting-started/installation/) 安装依赖库:
   ```bash
   uv sync
   ```

## ⚙️ 配置 Configuration

1. 复制配置模板 `.env.example` 为 `.env`:
   ```bash
   cp .env.example .env
   ```

2. 配置 `.env` 文件:
   ```bash
   # OpenAI API 配置
   OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
   OPENAI_BASE_URL="https://api.openai.com/v1"
   OPENAI_MODEL="gpt-4o-mini"

   # 语音识别配置
   ## 唤醒
   PLATFORM="YOUR_PLATFORM"   # [windows, mac, linux]
   PICOVOICE_ACCESS_KEY="YOUR_PICOVOICE_ACCESS_KEY"   # 前往 Picovoice 官网获取
   ## 语音识别
   RECOGNIZER_ENGINE="google"                         # [google, custom]
   CUSTOM_RECOGNIZER_API_KEY="YOUR_CUSTOM_RECOGNIZER_API_KEY"  # For custom
   CUSTOM_RECOGNIZER_BASE_URL="CUSTOM_RECOGNIZER_BASE_URL"     # For custom
   CUSTOM_RECOGNIZER_MODEL="YOUR_CUSTOM_RECOGNIZER_MODEL"      # For custom           

   # MQTT 配置
   MQTT_BROKER="example.com"
   MQTT_PORT=1883
   MQTT_USERNAME="YOUR_MQTT_USERNAME"
   MQTT_PASSWORD="YOUR_MQTT_PASSWORD"

   # GSV 配置
   GSV_BASE_URL="YOUR_GSV_BASE_URL"            # GPT-Sovits API 服务器地址
   REF_AUDIO_PATH="YOUR_REF_AUDIO_PATH"        # 参考音频路径 (于服务器上)
   PROMPT_TEXT="YOUR_PROMPT_TEXT"              # 参考音频文本
   PROMPT_LANG="YOUR_PROMPT_LANG"              # 参考音频语种
   ```

## 🚀 使用教程 Usage Guide

1. 爱丽丝上线！:
   ```bash
   uv run main.py
   ```

2. 启动后说出唤醒词 "爱丽丝" 以开启聊天
3. 说出指令或开始聊天
4. 使用 "再见", "退出", 或 "结束" 结束对话

## 📝 License

MIT License - [LICENSE](LICENSE)
