# 引入 DHT 溫濕度感測器模組
import dht

# 引入 machine 模組，用於控制硬體和 GPIO
import machine

# 初始化 DHT11 溫濕度感測器，連接到 GPIO 4
d = dht.DHT11(machine.Pin(4))  # 使用 DHT11 型號

# 測量溫度和濕度
d.measure()  # 開始測量

# 取得測量的溫度值
d.temperature()  # 返回溫度（攝氏度），例如 23°C

# 取得測量的濕度值
d.humidity()  # 返回濕度（相對濕度），例如 41% RH

# 初始化 DHT22 溫濕度感測器，連接到 GPIO 4
d = dht.DHT22(machine.Pin(4))  # 使用 DHT22 型號

# 測量溫度和濕度
d.measure()  # 開始測量

# 取得測量的溫度值
d.temperature()  # 返回溫度（攝氏度），例如 23.6°C

# 取得測量的濕度值
d.humidity()  # 返回濕度（相對濕度），例如 41.3% RH
