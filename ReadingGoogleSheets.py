# 引入 MicroPython 所需的函式庫
import urequests  # 用於發送 HTTP 請求
import time  # 用於時間相關操作
import ubinascii  # 用於二進位和 ASCII 的轉換
import machine  # 用於控制機器相關功能
import network  # 用於網路連接
from machine import Pin, I2C  # 用於控制 GPIO 和 I2C
import bme280  # 引入 BME280 氣象感測器的函式庫

# 定義 WiFi 網路的 SSID 和密碼
ssid = 'NCNUIOT'  # WiFi 網路的 SSID
password = '12345678'  # WiFi 網路的密碼

# 設定 IFTTT 請求的 URL 和伺服器地址
IFTTT_URL = '/trigger/BME280_Sensor_Readings/with/key/enter_your_key_here'  # IFTTT 事件的 URL
server = 'maker.ifttt.com'  # IFTTT 伺服器的主機名

# 初始化感測器和 I2C 連接
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)  # 設定 I2C 的 SDA 和 SCL 引腳
bme = bme280.BME280(i2c=i2c)  # 初始化 BME280 感測器

# 定義連接 WiFi 的函數
def connect_wifi(ssid, password):
  # 連接到指定的 WiFi 網路
  station = network.WLAN(network.STA_IF)  # 使用 STA 模式
  station.active(True)  # 啟用網路
  station.connect(ssid, password)  # 連接到 WiFi 網路
  while not station.isconnected():  # 等待連接成功
    pass
  print('Connection successful')  # 顯示連接成功
  print(station.ifconfig())  # 打印網路配置

# 定義發送 IFTTT 請求的函數
def make_ifttt_request():
    print('Connecting to', server)  # 顯示正在連接
    # 準備要發送的 JSON 數據，包含 BME280 感測器的讀數
    json_data = '{"value1":"' + bme.values[0] + '","value2":"' + bme.values[1]  + \
        '","value3":"' + bme.values[2] + '"}'
    headers = {'Content-Type': 'application/json'}  # 設定請求標頭
    # 發送 POST 請求到 IFTTT
    response = urequests.post('https://' + server + IFTTT_URL, data=json_data, headers=headers)
    print('Response:', response.content.decode())  # 打印請求的回應
    response.close()  # 關閉回應
    print('Closing Connection')  # 顯示連接已關閉

# 定義主循環
last_message = 0  # 上一次發送訊息的時間
message_interval = 10  # 訊息發送的間隔時間

while True:  # 無限循環
    # 如果時間間隔已過
    if (time.time() - last_message) > message_interval:
        print('Sensor reading in progress...')  # 顯示感測器正在讀取
        connect_wifi(ssid, password)  # 連接 WiFi
        make_ifttt_request()  # 發送 IFTTT 請求
        last_message = time.time()  # 更新上一次發送訊息的時間
