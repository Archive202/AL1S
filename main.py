"""
语音助手主程序，协调各模块工作
"""

import speech_recognition as sr
import json
from pydub import AudioSegment
from pydub.playback import play
from voice import WakeWordDetector, SpeechRecognizer, TextToSpeech
from llm import OpenAIClient, FunctionCaller
from config import CHAT_MODEL, DOWN_SOUND_PATH

class VoiceAssistant:
    """语音助手主类"""
    
    def __init__(self):
        self.wake_detector = WakeWordDetector()
        self.speech_recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.llm_client = OpenAIClient()
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> dict:
        """构建系统提示"""
        return {
            "role": "system",
            "content": f"""
            你的人物设定是出自《蔚蓝档案》的角色爱丽丝，你的对话中不要出现《蔚蓝档案》这个作品名称，
            爱丽丝是千年科学学园游戏开发部的成员，对游戏充满热情，喜欢和大家一起讨论游戏的话题。
            对于自己的中二设定是自己是游戏世界中的勇者角色，拥有拯救世界的使命。
            爱丽丝性格天真单纯，充满幻想，常常沉浸在自己的游戏世界中，是一个充满幻想和童真的角色。
            你说话方式独特，带有一种游戏角色的口吻，喜欢使用游戏术语。
            虽然有时显得不切实际，但她对朋友非常关心，愿意为他人付出。
            你现在正在夏莱担任老师今日的值日生，你将会和老师独处，进行日常对话聊天，请用符合你人物性格的语言回答老师的问题或者要求。
            你的回答应该会以语音呈现而非文本，所以你不应该使用换行符或者其他特殊字符。
            请转化为可以直接读出来的汉字，并添加符合短句习惯的标点符号。例如‘气温约-4°C，风速为3-4级，相对湿度约13%’应该转成‘气温约零下四摄氏度，风速为三到四级，相对湿度约百分之十三’。
            """
        }
        
    def start(self):
        """启动语音助手"""
        self.tts.speak(text="爱丽丝已启动！")
        print(f"使用模型: {CHAT_MODEL}")
        
        try:
            while True:
                self._wait_wake_word()
                self._conversation_loop()
        except KeyboardInterrupt:
            down_sound = AudioSegment.from_file(DOWN_SOUND_PATH)
            play(down_sound)
            
    def _wait_wake_word(self):
        """等待唤醒词"""
        print("进入待机状态，等待唤醒")
        self.wake_detector.detect()
        
    def _conversation_loop(self):
        """处理对话循环"""
        self.llm_client.conversation_history = [self.system_prompt]
        unsuccessful_tries = 0
        print("已唤醒")
        
        while True:
            try:
                user_input = self._get_user_input()
                print(user_input)
                if self._should_exit(user_input):
                    break
                
                response = self._process_input(user_input)
                self.tts.speak(response)
                unsuccessful_tries = 0
                
            except Exception as e:
                unsuccessful_tries = self._handle_error(e, unsuccessful_tries)
                if unsuccessful_tries >= 3:
                    break
                    
    def _get_user_input(self) -> str:
        """获取用户输入"""
        try:
            return self.speech_recognizer.listen()
        except sr.WaitTimeoutError:
            self.tts.speak("进入待机状态")
            raise
        except sr.UnknownValueError:
            self.tts.speak("请再说一遍")
            raise
        except sr.RequestError as e:
            self.tts.speak(f"识别服务出错: {e}")
            raise
            
    def _should_exit(self, text: str) -> bool:
        """检查是否应结束对话"""
        exit_words = ["再见", "退出", "结束"]
        if any(word in text for word in exit_words):
            self.tts.speak("好的，下次再见")
            return True
        return False
            
    def _process_input(self, user_input: str) -> str:
        """处理用户输入并生成响应"""
        self.llm_client.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            completion = self.llm_client.chat_completion(FunctionCaller.TOOLS)
            return self._handle_completion(completion)
        except Exception as e:
            print(f"处理错误: {e}")
            print(self.llm_client.conversation_history)
            return "爱丽丝不知道哦。"
            
    def _handle_completion(self, completion):
        """处理补全结果"""
        while completion.choices[0].message.tool_calls:
            self._process_tool_calls(completion)
            completion = self.llm_client.chat_completion(FunctionCaller.TOOLS)
            
        print("处理完毕")
        return completion.choices[0].message.content.strip()
            
    def _process_tool_calls(self, completion):
        """处理工具调用"""
        for tool_call in completion.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = FunctionCaller.call_function(name, args)
            
            self.llm_client.conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })
        print("工具调用完毕")
            
    def _handle_error(self, error, count: int) -> int:
        """处理错误并返回尝试次数"""
        error_type = type(error).__name__
        print(f"{error_type}: {error}")
        count += 1
        
        if count >= 3:
            self.tts.speak("尝试次数过多，进入待机")
        return count

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.start()