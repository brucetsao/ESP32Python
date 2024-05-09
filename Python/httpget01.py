# 引入 MicroPython 中的垃圾回收、時間和網路相關模組
import gc  # 用於垃圾回收
import time  # 用於時間相關操作

# 嘗試引入 urequests 以支援 HTTP 請求，若失敗則引入 requests
try:
  import urequests as requests
except:
  import requests
  
# 嘗試引入 ujson 以支援 JSON 處理，若失敗則引入 json
try:
  import ujson as json
except:
  import json

import network  # 用於 Wi-Fi 連接

# 執行垃圾回收以釋放未使用的記憶體
gc.collect()  # 清理垃圾

# 定義 Wi-Fi 的 SSID 和密碼
ssid = 'NCNUIOT'
password = '12345678'

# 定義城市和國家代碼，用於 OpenWeatherMap API
city = 'Puli'
country_code = 'TW'

# 定義 OpenWeatherMap 的 API 金鑰
open_weather_map_api_key = 'a14064cb58b67aff9d6116e82b3364dd'

# 建立 WLAN 物件並連接到 Wi-Fi
station = network.WLAN(network.STA_IF)  # 使用 STA 模式
station.active(True)  # 啟用無線網路
station.connect(ssid, password)  # 連接到指定 SSID，使用給定的密碼

# 等待 Wi-Fi 連接成功
while not station.isconnected():  # 如果尚未連接
  pass  # 持續等待

# Wi-Fi 連接成功後顯示連接訊息
print('Connection successful')  # 顯示連接成功
print(station.ifconfig())  # 顯示網路配置

# 執行垃圾回收
gc.collect()  # 清理垃圾

# 設定 HTTP GET 請求的目標 URL
httpget_url = 'http://ncnu.arduino.org.tw:9999/ems/GetAllDevice.php'  # 設定 API 的 URL
print(httpget_url)  # 列印 URL

# 發送 HTTP GET 請求並獲取回應
r = requests.get(httpget_url)  # 發送 HTTP GET 請求
# httpget_data = r.text  # 取得回應的文字內容

# 將回應的 JSON 內容轉換為字串
data = json.dumps(r.text)  # 將回應轉換為 JSON 字串
print(data)  # 列印 JSON 字串

# 執行垃圾回收
gc.collect()  # 清理垃圾
