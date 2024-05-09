# 從 machine 模組引入 Pin 類別，用於 GPIO 控制
from machine import Pin

# 引入 time 模組中的 sleep 函式，用於延遲
from time import sleep

# 引入 dht 模組，用於 DHT 溫濕度感測器
import dht

# 初始化 DHT22 感測器，連接到 GPIO 16
sensor = dht.DHT22(Pin(16))  # 使用 DHT22 型號
# 如果使用 DHT11，可以將上面一行替換為
# sensor1 = dht.DHT11(Pin(16))

# 無限迴圈，每隔一段時間測量溫度和濕度
while True:
    sensor.measure()  # 開始測量溫度和濕度
    temp = sensor.temperature()  # 取得測量的溫度
    hum = sensor.humidity()  # 取得測量的濕度

    # 列印溫度和濕度
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))  # 格式化輸出

    # 延遲 2 秒，避免過於頻繁的測量
    sleep(2)  # 等待 2 秒
