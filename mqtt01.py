# 引入 MicroPython 的相關模組
from machine import Pin  # 用於控制 GPIO 引腳
import time  # 用於時間相關操作
from umqttsimple import MQTTClient  # 用於 MQTT 通訊
import ubinascii  # 用於二進位到 ASCII 的轉換
import machine  # 用於控制機器相關操作
import micropython  # 用於 MicroPython 特定的功能
import network  # 用於網路操作
import gc  # 用於垃圾回收
gc.collect()  # 進行垃圾回收，釋放記憶體

# Wi-Fi 網路配置
ssid = 'HUAWEI-u67E'  # Wi-Fi 的 SSID
password = '4uF77R2n'  # Wi-Fi 的密碼
mqtt_server = '192.168.18.8'  # MQTT 伺服器的 IP 地址

# MQTT 配置
client_id = ubinascii.hexlify(machine.unique_id())  # 生成唯一的 Client ID
topic_pub = b'rpi_pico_w/test_pub'  # MQTT 發佈主題

# 連接到 Wi-Fi 網路
station = network.WLAN(network.STA_IF)  # 使用 STA 模式
station.active(True)  # 啟用網路
station.connect(ssid, password)  # 連接到指定 SSID

# 等待 Wi-Fi 連接成功
while not station.isconnected():  # 如果尚未連接
  pass  # 持續等待

print('Connection successful')  # 顯示連接成功
print(station.ifconfig())  # 顯示網路配置

# 連接到 MQTT 代理伺服器
def connect():
  print('Connecting to MQTT Broker...')  # 顯示正在連接
  global client_id, mqtt_server  # 使用全域變數
  client = MQTTClient(client_id, mqtt_server)  # 建立 MQTT 客戶端
  client.connect()  # 連接到 MQTT 代理伺服器
  print('Connected to %s MQTT broker' % (mqtt_server))  # 顯示連接成功
  return client  # 返回 MQTT 客戶端

# 重新啟動並重新連接
def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')  # 顯示連接失敗
  time.sleep(10)  # 等待 10 秒
  machine.reset()  # 重新啟動機器

# 嘗試連接到 MQTT 代理伺服器
try:
  client = connect()  # 連接到 MQTT
except OSError as e:  # 如果連接失敗
  restart_and_reconnect()  # 重新啟動並重新連接

# 初始化按鈕和其他變數
push_button = Pin(15, Pin.IN)  # 按鈕連接到 GPIO 15
push_button_Prv_state = False  # 按鈕的前一個狀態
mesg_id = 0  # 訊息 ID 初始值

# 無限迴圈，不斷發佈訊息
while True:
  try:
    # 準備要發佈的訊息
    msg = "Message id: " + str(mesg_id)  # 訊息內容包含訊息 ID
    print('Publishing message: %s on topic %s' % (msg, topic_pub))  # 顯示要發佈的訊息
    client.publish(topic_pub, msg)  # 發佈訊息到 MQTT 主題
    time.sleep(2)  # 等待 2 秒
    mesg_id += 1  # 增加訊息 ID
  except OSError as e:  # 如果發生錯誤
    restart_and_reconnect()  # 重新啟動並重新連接
