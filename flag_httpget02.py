# 引入 MicroPython 的網路功能、HTTP 請求、時間操作以及垃圾回收
import network## 引入 MicroPython 的網路功能
import urequests## 引入 MicroPython 的HTTP 請求
import time## 引入 MicroPython 的時間操作
import gc## 引入 MicroPython 的垃圾回收

# 連接無線網路
sta = network.WLAN(network.STA_IF)  # 設定為 STA 模式（連接到無線網路）
sta.active(True)  # 啟用 STA 模式
sta.connect('NCNUIOT', '12345678')  # 連接到指定 SSID，並使用給定的密碼

# 等待 Wi-Fi 連接成功
while not sta.isconnected():  # 如果未連接
    pass  # 等待 Wi-Fi 連接

print('Wi-Fi connected.')  # 顯示 Wi-Fi 連接成功的訊息

# 無限迴圈，持續檢查網路內容
while True:
    # 發送 HTTP GET 請求至指定 URL
    res = urequests.get("https://flagtech.github.io/flag.txt")  # 請求檔案
    
    # 檢查 HTTP 狀態碼是否為 200，表示成功
    if res.status_code == 200:  # 如果 HTTP 回應成功
        res.close()  # 關閉 HTTP 回應，釋放資源
        print("Success.")  # 顯示成功訊息
