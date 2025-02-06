# 🎤 Athena

> A Chinese voice assistant powered by OpenAI's GPT and Python text-to-speech technology, featuring wake word detection and web search capabilities.

## ✨ Features

- 🔊 Wake word detection ("Hey Siri")
- 🗣️ Chinese voice command recognition
- 🤖 AI-powered conversations using OpenAI GPT
- 🔍 Web search integration with DuckDuckGo
- 🌐 Multiple speech recognition engines (Google, Azure)
- 🎯 Automatic ambient noise adjustment
- 🔄 Conversation history management
- ⏲️ Auto-standby mode
- 🎵 Text-to-speech response in Chinese
- 🌍 Asynchronous web content extraction

## 🛠️ Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager 
- OpenAI API key
- [Picovoice Access key](https://console.picovoice.ai/)
- Azure Speech API key (optional, if using Azure speech recognition)
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

## ⚙️ Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update `.env` with your credentials:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_MODEL="gpt-4o-mini"
PICOVOICE_ACCESS_KEY="YOUR_PICOVOICE_ACCESS_KEY"
AZURE_KEY="YOUR_AZURE_KEY"           # Optional, for Azure speech recognition
RECOGNIZER_ENGINE="google"           # Options: "google" or "azure"
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
- Default engine: Google Speech Recognition
- Alternative: Azure Speech Recognition (requires Azure key)
- Automatic ambient noise adjustment
- 20-second timeout for commands

### Web Search
- Integrated DuckDuckGo search
- Region-specific results (cn-zh)
- Safe search enabled
- Asynchronous content extraction from search results
- Returns detailed content from up to 5 sources

### Error Handling
- Automatic retry on speech recognition failures (max 3 attempts)
- Graceful timeout handling
- Clear error messages
- Auto-standby mode

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
