# 引入 MicroPython 中的時間模組
import time  # 用於延遲和計時

# 嘗試引入 urequests 和 ujson，若失敗則引入備用模組
try:
  import urequests as requests  # 用於 HTTP 請求
except:
  import requests  # 備用請求模組
  
try:
  import ujson as json  # 用於 JSON 處理
except:
  import json  # 備用 JSON 模組

import network  # 用於網路操作

import gc  # 用於垃圾回收
gc.collect()  # 進行垃圾回收

# 設定 Wi-Fi 連接的 SSID 和密碼
ssid = 'NCNUIOT'  # Wi-Fi 的 SSID
password = '12345678'  # Wi-Fi 的密碼

# 定義城市和國家代碼，用於查詢天氣
city = 'Puli'  # 所查詢的城市
country_code = 'TW'  # 所查詢的國家代碼

# 定義 OpenWeatherMap 的 API 金鑰
open_weather_map_api_key = 'a14064cb58b67aff9d6116e82b3364dd'  # 天氣 API 的金鑰

# 初始化 WLAN 物件
station = network.WLAN(network.STA_IF)  # 使用 STA 模式

# 啟用並連接到指定 Wi-Fi 網路
station.active(True)  # 啟用網路
station.connect(ssid, password)  # 連接到 Wi-Fi 網路

# 等待 Wi-Fi 連接成功
while not station.isconnected():  # 如果尚未連接
  pass  # 等待連接成功

print('Connection successful')  # 顯示連接成功
print(station.ifconfig())  # 顯示網路配置

# 設定 OpenWeatherMap 的查詢 URL
open_weather_map_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=' + open_weather_map_api_key
print(open_weather_map_url)  # 顯示查詢 URL

# 發送 HTTP GET 請求並取得回應
weather_data = requests.get(open_weather_map_url)  # 取得天氣數據
print(weather_data.json())  # 顯示天氣數據的 JSON 格式

# 取得並顯示城市和國家代碼
location = 'Location: ' + weather_data.json().get('name') + ' - ' + weather_data.json().get('sys').get('country')  # 取得城市和國家
print(location)  # 顯示地點

# 取得並顯示天氣描述
description = 'Description: ' + weather_data.json().get('weather')[0].get('main')  # 天氣描述
print(description)  # 顯示描述

# 取得並顯示溫度
raw_temperature = weather_data.json().get('main').get('temp') - 273.15  # 轉換為攝氏溫度
temperature = 'Temperature: ' + str(raw_temperature) + '*C'  # 溫度描述
# 如果需要攝氏轉華氏
# temperature = 'Temperature: ' + str(raw_temperature * (9/5.0) + 32) + '*F'
print(temperature)  # 顯示溫度

# 取得並顯示氣壓
pressure = 'Pressure: ' + str(weather_data.json().get('main').get('pressure')) + ' hPa'  # 氣壓
print(pressure)  # 顯示氣壓

# 取得並顯示濕度
humidity = 'Humidity: ' + str(weather_data.json().get('main').get('humidity')) + '%'  # 濕度
print(humidity)  # 顯示濕度

# 取得並顯示風速和風向
wind = 'Wind: ' + str(weather_data.json().get('wind').get('speed')) + ' mps ' + str(weather_data.json().get('wind').get('deg')) + '*'  # 風速和風向
print(wind)  # 顯示風
