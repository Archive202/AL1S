# 🎤 Athena

> A Chinese voice assistant powered by OpenAI's GPT and Python text-to-speech technology, featuring wake word detection and web search capabilities.

## ✨ Features

- 🔊 Wake word detection ("Hey Siri")
- 🗣️ Chinese voice command recognition
- 🤖 AI-powered conversations using OpenAI GPT
- 🔍 Web search integration with DuckDuckGo
- 🌐 Multiple speech recognition engines (Google, Azure)
- 🔊 Multiple TTS engines (pyttsx3, Sovits)
- 🎯 Automatic ambient noise adjustment
- 🔄 Conversation history management
- ⏲️ Auto-standby mode
- 🎵 Text-to-speech response in Chinese
- 🌍 Asynchronous web content extraction
- 📅 Time-aware responses

## 🛠️ Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager 
- OpenAI API key
- [Picovoice Access key](https://console.picovoice.ai/)
- Azure Speech API key (optional, if using Azure speech recognition)
- Sovits server (optional, if using Sovits TTS)
- VLC media player
- Working microphone and speakers

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/AbyssSkb/Athena
cd Athena
```

2. Install required packages:
```bash
uv sync
```

3. Install VLC media player:
   - Windows: Download and install from [VideoLAN official website](https://www.videolan.org/)
   - Linux: `sudo apt install vlc`
   - macOS: `brew install vlc`

## ⚙️ Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update `.env` with your credentials:
```bash
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_MODEL="gpt-4o-mini"
PICOVOICE_ACCESS_KEY="YOUR_PICOVOICE_ACCESS_KEY"
AZURE_KEY="YOUR_AZURE_KEY"           # Optional, for Azure speech recognition
RECOGNIZER_ENGINE="google"           # Options: "google" or "azure"
SPEAKER_ENGINE="pyttsx3"            # Options: "pyttsx3" or "sovits"
SOVITS_BASE_URL="YOUR_SOVITS_BASE_URL" # Required if using Sovits
REF_AUDIO_PATH="YOUR_REF_AUDIO_PATH"   # Required if using Sovits
PROMPT_TEXT="YOUR_PROMPT_TEXT"         # Required if using Sovits
PROMPT_LANG="YOUR_PROMPT_LANG"         # Required if using Sovits
```

3. Configure `pyttsx3` for Linux users:
```bash
sudo apt update && sudo apt install espeak-ng libespeak1
```
> **Note:** This step is only required for Linux users if voice output is not working.

## 🚀 Usage

1. Start the voice assistant:
```bash
uv run main.py
```

2. Say "Hey Siri" to activate the assistant
3. Speak your command or question in Chinese
4. Say "再见", "退出" or "结束" to end the conversation

## ⚡ Quick Commands

- Wake Word: "Hey Siri"
- Exit Commands: "再见", "退出", "结束"

## 🎯 Features Details

### Speech Recognition
- Supports Google Speech Recognition and Azure Speech Recognition
- Automatic ambient noise adjustment
- 20-second timeout for commands
- Error retry mechanism (max 3 attempts)

### Text-to-Speech
- Default engine: pyttsx3 (offline)
- Alternative: Sovits (requires server setup)
- Automatic number and symbol conversion for natural speech

### Web Search
- Integrated DuckDuckGo search
- Region-specific results (cn-zh)
- Safe search enabled
- Asynchronous content extraction
- Returns detailed content from up to 5 sources

### AI Conversation
- Powered by OpenAI GPT models
- Context-aware responses
- Tool functions support (web search, time query)
- Natural Chinese language processing
- Time-aware responses

### Error Handling
- Automatic retry on failures
- Graceful timeout handling
- Clear error messages
- Auto-standby mode after multiple failures

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
