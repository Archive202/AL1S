"""
MQTT 客户端工具模块，提供连接和消息发送功能
"""

import paho.mqtt.client as mqtt
from config.settings import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD

def connect_mqtt() -> mqtt.Client:
    """
    创建并连接 MQTT 客户端
    
    Returns:
        已连接的 MQTT 客户端实例
    """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

def send_mqtt_message(topic: str, message: str) -> str:
    """
    发送 MQTT 消息到指定主题
    
    Args:
        topic: 目标主题
        message: 消息内容
        
    Returns:
        发送结果描述
    """
    client = connect_mqtt()
    result = client.publish(topic, message)
    status = result.rc
    if status == 0:
        return f"消息已成功发送到主题: {topic}"
    return f"消息发送失败，状态码: {status}"