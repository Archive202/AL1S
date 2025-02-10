<div align="center">

# AL1S

Hehe, Alice is so cute. Anyway, Alice is on duty at Schale today~ 🌸

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge)](https://www.python.org/downloads/) 
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg?style=for-the-badge)](https://platform.openai.com/) 
[![License](https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge)](https://github.com/Archive202/AL1S/blob/main/LICENSE)

**English** | [**中文简体**](/docs/zh/README.md)

</div>

---

## ✨ Features

- 🎤 Voice wake-up ("爱丽丝")
- 🗣️ Chinese speech recognition
- 🤖 AI-based chat capabilities (OpenAI API)
- 🔊 `GPT-Sovits` text-to-speech
- 🔍 MQTT control, web search, etc., based on `Function Calling API`

## 🛠️ Requirements

- 🐍 Python 3.10+
- 🎤 Microphone
- (Required) [uv](https://github.com/astral-sh/uv) Python package manager
- (Required) OpenAI API key
- (Required) [GPT-Sovits](https://github.com/RVC-Boss/GPT-SoVITS) API
- (Required) [Picovoice](https://console.picovoice.ai/) Access Key
- (Optional) Speech-To-Text AI API (e.g., [SenseVoice](https://github.com/FunAudioLLM/SenseVoice))
- (Optional) MQTT server

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Archive202/AL1S.git
   cd AL1S
   ```

2. Install the `portaudio` runtime library (dependency for `pyaudio`):
   - Linux (apt): `sudo apt install portaudio19-dev`
   - macOS: `brew install portaudio`

3. Use [uv](https://hellowac.github.io/uv-zh-cn/getting-started/installation/) to install dependencies:
   ```bash
   uv sync
   ```

## ⚙️ Configuration

1. Copy the configuration template `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure the `.env` file:
   ```bash
   # OpenAI API configuration
   OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
   OPENAI_BASE_URL="https://api.openai.com/v1"
   OPENAI_MODEL="gpt-4o-mini"

   # Speech recognition configuration
   ## Wake-up
   PLATFORM="YOUR_PLATFORM"   # [windows, mac, linux]
   PICOVOICE_ACCESS_KEY="YOUR_PICOVOICE_ACCESS_KEY"   # Obtain from Picovoice website
   ## Speech recognition
   RECOGNIZER_ENGINE="google"                         # [google, custom]
   CUSTOM_RECOGNIZER_API_KEY="YOUR_CUSTOM_RECOGNIZER_API_KEY"  # For custom
   CUSTOM_RECOGNIZER_BASE_URL="CUSTOM_RECOGNIZER_BASE_URL"     # For custom
   CUSTOM_RECOGNIZER_MODEL="YOUR_CUSTOM_RECOGNIZER_MODEL"      # For custom           

   # MQTT configuration
   MQTT_BROKER="example.com"
   MQTT_PORT=1883
   MQTT_USERNAME="YOUR_MQTT_USERNAME"
   MQTT_PASSWORD="YOUR_MQTT_PASSWORD"

   # GSV configuration
   GSV_BASE_URL="YOUR_GSV_BASE_URL"            # GPT-Sovits API server address
   REF_AUDIO_PATH="YOUR_REF_AUDIO_PATH"        # Reference audio path (on the server)
   PROMPT_TEXT="YOUR_PROMPT_TEXT"              # Reference audio text
   PROMPT_LANG="YOUR_PROMPT_LANG"              # Reference audio language
   ```

## 🚀 Usage Guide

1. Alice is online!:
   ```bash
   uv run main.py
   ```

2. After starting, say the wake-up word `爱丽丝` to start chatting
3. Speak commands or start chatting
4. End the conversation by saying goodbye in the form of `bye-bye`, `goodbye`, etc

## 📝 License

MIT License - [LICENSE](LICENSE)
