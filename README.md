# AL1S

> 嘿嘿爱丽丝可爱捏，总之今天爱丽丝来夏莱当值日生了~

## ✨ 功能

- 🔊 语音唤醒 ("爱丽丝")
- 🗣️ 中文语音识别
- 🤖 基于AI的聊天能力 (Openai API)
- 🔊 GPT-Sovits \[爱丽丝\]TTS语音
- 🔍 基于Function Calling API实现mqtt控制、网络搜索

## 🛠️ 环境要求

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager 
- OpenAI API key
- GPT-Sovits server
- [Picovoice Access key](https://console.picovoice.ai/)
- Azure Speech API key (optional, if using Azure speech recognition)
- VLC media player
- Working microphone and speakers
- mqtt server (optional)

## 📦 安装

1. 克隆本仓库:
```bash
git clone https://github.com/Archive202/AL1S.git
cd AL1S
```

2. 安装portaudio运行库:
   - Linux(apt): `sudo apt install portaudio19-dev`
   - macOS: `brew install portaudio`

3. 使用[uv](https://hellowac.github.io/uv-zh-cn/getting-started/installation/)安装依赖库:
```bash
uv sync
```

## ⚙️ 配置

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
PICOVOICE_ACCESS_KEY="YOUR_PICOVOICE_ACCESS_KEY"   # 前往Picovoice官网获取
## 语音识别
RECOGNIZER_ENGINE="google"                         # [google, custom]
CUSTOM_RECOGNIZER_API_KEY="YOUR_CUSTOM_RECOGNIZER_API_KEY"
CUSTOM_RECOGNIZER_BASE_URL="CUSTOM_RECOGNIZER_BASE_URL"
CUSTOM_RECOGNIZER_MODEL="YOUR_CUSTOM_RECOGNIZER_MODEL"                    

# MQTT 配置
MQTT_BROKER="example.com"
MQTT_PORT=1883
MQTT_USERNAME="YOUR_MQTT_USERNAME"
MQTT_PASSWORD="YOUR_MQTT_PASSWORD"

# GSV 配置
GSV_BASE_URL="YOUR_GSV_BASE_URL"            # GPT-Sovits API服务器地址
REF_AUDIO_PATH="YOUR_REF_AUDIO_PATH"        # 参考音频路径 (于服务器上)
PROMPT_TEXT="YOUR_PROMPT_TEXT"              # 参考音频文本
PROMPT_LANG="YOUR_PROMPT_LANG"              # 参考音频语种
```

## 🚀 使用教程

1. AL1S, System UP!:
```bash
uv run main.py
```

2. 启动后说出唤醒词"爱丽丝"以开启聊天
3. 说出指令或开始聊天
4. "再见", "退出", "结束"可作为结束词以结束此次回话 

## 📝 License

MIT License - [LICENSE](LICENSE)