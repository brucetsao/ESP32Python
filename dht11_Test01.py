# 引入 dht 套件，用於使用 DHT 溫濕度感測器
import dht

# 從 machine 模組引入 Pin 類別，用於控制 GPIO 腳位
from machine import Pin

# 初始化 DHT11 溫濕度感測器，連接到 GPIO 14
sensor = dht.DHT11(Pin(14))  # 使用 DHT11 型號
# 如果使用 DHT22，可以將上面一行替換為
# sensor = dht.DHT22(Pin(14))

# 測量溫度和濕度
sensor.measure()  # 開始測量溫度和濕度

# 列印測得的溫度
print("temperature", sensor.temperature())  # 列印溫度

# 列印測得的濕度
print("humidity", sensor.humidity())  # 列印濕度
