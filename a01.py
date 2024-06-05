
# 從 machine 模組引入 Pin 類別，用於控制硬體的 GPIO 腳位
from machine import Pin

# 引入 time 模組，用於時間延遲和計時
import time

# 引入 umqtt.robust 模組，用於建立 MQTT 用戶端和通信
from umqtt.robust import MQTTClient

# 引入 network 模組，用於網路連線和設定
import network

# 引入 urequests 模組，用於 HTTP 請求
import urequests

# 執行一個 HTTP GET 請求，從指定的 URL 取得資料
response = urequests.get('http://jsonplaceholder.typicode.com/albums/1')

# 列印 response 的資料類型
print(type(response))  # 顯示 response 的類型，以確保請求成功
