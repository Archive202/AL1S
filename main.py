import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import pvporcupine
import pyaudio
from dotenv import load_dotenv
from openai import OpenAI
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import asyncio
import httpx
import json
import os

# 加载环境变量
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
chat_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
picovoice_access_key = os.getenv("PICOVOICE_ACCESS_KEY")
recognizer_engine = os.getenv("RECOGNIZER_ENGINE", "google")

# 初始化
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty("voices")
tts_engine.setProperty("voice", voices[-1].id)

porcupine = pvporcupine.create(keywords=["爱丽丝"], access_key=picovoice_access_key,
                               keyword_paths=['./wakewords/爱丽丝_zh_windows_v3_0_0.ppn'],
                               model_path='./wakewords/porcupine_params_zh.pv')

recognizer = sr.Recognizer()
recognizer.operation_timeout = 10
chat_client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_base_url,
)
conversation_history = []
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_duckduckgo",
            "description": "使用DuckDuckGo搜索引擎查询信息。可以搜索最新新闻、文章、博客等内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "搜索的关键词列表。例如：['Python', '机器学习', '最新进展']。",
                    }
                },
                "required": ["keywords"],
            },
        },
    }
]


async def fetch_url(url: str):
    """
    异步获取指定URL的网页内容并提取文本。

    Parameters:
        url (str): 要获取内容的网页URL

    Returns:
        str: 提取的网页文本内容，经过清理和格式化

    Raises:
        httpx.RequestError: 当请求失败时抛出
    """
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
            }
            response = await client.get(url, headers=headers)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            text = "\n".join(
                [line.strip() for line in text.splitlines() if line.strip()]
            )
            return text
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")


async def crawl_web(urls: list[str]):
    """
    并发爬取多个URL的内容。

    Parameters:
        urls (list[str]): 要爬取的URL列表

    Returns:
        list: 所有URL的爬取结果列表
    """
    results = await asyncio.gather(*(fetch_url(url) for url in urls))
    return results


def search_duckduckgo(keywords: list[str]):
    """
    使用 DuckDuckGo 搜索引擎执行查询并获取详细内容。

    Parameters:
        keywords (list[str]): 搜索关键词列表

    Returns:
        list: 搜索结果页面的完整文本内容列表

    Example:
        >>> search_duckduckgo(['Python', '机器学习'])
        ['页面1的文本内容', '页面2的文本内容', ...]
    """
    search_term = " ".join(keywords)
    print(f"Searching: {search_term}")
    results = DDGS().text(
        keywords=search_term,
        region="cn-zh",
        safesearch="on",
        max_results=5,
        backend="html",
    )
    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print(result["title"])
        print(result["href"])
        print(result["body"])
        print()

    urls = [result["href"] for result in results]
    response_results = asyncio.run(crawl_web(urls))
    return response_results


def call_function(name: str, args: dict[str, str]):
    """
    根据函数名和参数动态调用工具函数。

    Parameters:
        name (str): 要调用的函数名
        args (dict): 函数参数字典

    Returns:
        Any: 函数调用的结果

    Raises:
        ValueError: 当指定的函数名不存在时抛出
    """
    if name == "search_duckduckgo":
        return search_duckduckgo(**args)


def detect_wake_word():
    """
    监听并检测唤醒词。

    使用 Porcupine 热词检测引擎来识别唤醒词 "hey siri"。
    当检测到唤醒词时，会播放语音确认并停止监听。

    Returns:
        None

    Raises:
        PyAudioError: 音频设备初始化失败时抛出
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )
    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)
        result = porcupine.process(pcm)
        if result >= 0:
            wake_sound = AudioSegment.from_file("./src/sounds/wake.mp3")
            play(wake_sound)
            break
    stream.stop_stream()
    stream.close()
    p.terminate()


def listen_for_commands() -> str:
    """
    监听并转换用户的语音指令为文本。

    使用选定的语音识别引擎（通过RECOGNIZER_ENGINE环境变量配置）：
    - google: Google Speech Recognition
    - azure: Microsoft Azure Speech Recognition（需要配置AZURE_KEY和AZURE_LOCATION）

    Returns:
        str: 识别出的用户语音指令文本

    Raises:
        sr.UnknownValueError: 语音无法被识别时抛出
        sr.RequestError: 语音识别服务出现问题时抛出
        sr.WaitTimeoutError: 等待用户输入超过20秒时抛出
    """
    print("等待用户指令")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=20)
    print("收到指令")

    match recognizer_engine:
        case "google":
            command = recognizer.recognize_google(audio, language="zh-CN")
        case "azure":
            azure_key = os.getenv("AZURE_KEY")
            azure_location = os.getenv("AZURE_LOCATION", "eastus")
            command = recognizer.recognize_azure(
                audio,
                key=azure_key,
                location=azure_location,
                language="zh-CN",
            )[0]

    print(f"User: {command}")
    return command


def speak(sentence: str):
    """
    使用文字转语音引擎朗读文本。

    使用 pyttsx3 引擎将文本转换为语音输出，
    同时在控制台打印输出内容。

    Parameters:
        sentence (str): 需要朗读的文本内容

    Returns:
        None

    Example:
        >>> speak("你好，我是语音助手")
        Assistant: 你好，我是语音助手
    """
    print(f"Assistant: {sentence}")
    tts_engine.say(sentence)
    tts_engine.runAndWait()


def get_model_response(user_input: str) -> str:
    """
    调用 OpenAI API 获取对话回复。

    功能：
    1. 将用户输入添加到对话历史
    2. 调用指定的 GPT 模型生成回复
    3. 支持工具调用（如网络搜索功能）
    4. 处理工具调用结果并生成最终回复
    5. 维护对话上下文

    Parameters:
        user_input (str): 用户的输入文本

    Returns:
        str: AI 模型生成的回复文本

    Raises:
        Exception: 当 API 调用失败时返回错误信息
    """
    try:
        conversation_history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )
        completion = chat_client.chat.completions.create(
            model=chat_model,
            messages=conversation_history,
            tools=tools,
        )
        conversation_history.append(completion.choices[0].message)
        if completion.choices[0].message.tool_calls:
            for tool_call in completion.choices[0].message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                result = call_function(name, args)
                result = json.dumps(result, ensure_ascii=False)
                conversation_history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

            completion = chat_client.chat.completions.create(
                model=chat_model,
                messages=conversation_history,
                tools=tools,
            )
            conversation_history.append(completion.choices[0].message)
        else:
            print("No search needed.")
        ai_response = completion.choices[0].message.content.strip()
        return ai_response
    except Exception as e:
        print(f"Error getting model response: {e}")
        return "抱歉，我现在无法回答这个问题。"


def start_assistant():
    """
    启动语音助手的主循环。

    主要功能：
    1. 等待唤醒词激活系统
    2. 进入交互式对话循环
    3. 处理用户指令并返回响应
    4. 管理对话状态和异常情况

    特性：
    - 每轮对话前自动清理历史记录
    - 支持多种退出命令（"再见"、"退出"、"结束"）
    - 错误重试机制（最多3次）
    - 超时（20秒）自动进入待机模式
    - 完善的异常处理机制
    - 系统提示词引导，确保AI回答简洁友好

    Returns:
        None

    Raises:
        KeyboardInterrupt: 用户手动中断程序时抛出
    """
    print("System UP")

    print(f"Use model: {chat_model}")
    try:
        while True:
            conversation_history.clear()
            detect_wake_word()
            unsuccessful_tries = 0
            conversation_history.append(
                {
                    "role": "system",
                    "content": "你是一个友好的AI助手，请用简洁的语言回答用户的问题。",
                }
            )

            while True:
                try:
                    user_input = listen_for_commands()
                    if any(word in user_input for word in ["再见", "退出", "结束"]):
                        speak("好的，下次再见。")
                        break

                    response = get_model_response(user_input)
                    speak(response)
                except sr.UnknownValueError:
                    speak("抱歉，我没有听清楚，请再说一遍。")
                    unsuccessful_tries += 1
                except sr.RequestError as e:
                    speak(f"语音识别服务错误: {e}")
                    unsuccessful_tries += 1
                except sr.WaitTimeoutError:
                    speak("进入待机状态。")
                    break
                except TimeoutError:
                    speak("请求超时。")
                    unsuccessful_tries += 1

                if unsuccessful_tries >= 3:
                    speak("尝试次数过多，进入待机状态。")
                    break

    except KeyboardInterrupt:
        speak("退出程序")


start_assistant()
