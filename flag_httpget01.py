# 引入 MicroPython 的網路功能、HTTP 請求、時間操作以及垃圾回收
import network## 引入 MicroPython 的網路功能
import urequests## 引入 MicroPython 的HTTP 請求
import time## 引入 MicroPython 的時間操作
import gc## 引入 MicroPython 的垃圾回收

# 連接無線網路
sta = network.WLAN(network.STA_IF)  # 設定為 STA 模式（連接到無線網路）
sta.active(True)  # 啟用無線網路
sta.connect('NCNUIOT', '12345678')  # 連接到指定 SSID，使用給定的密碼

# 等待無線網路連接成功
while not sta.isconnected():
    pass  # 不做任何操作，持續等待連接成功

# Wi-Fi 連接成功
print('Wi-Fi connected.')  # 顯示 Wi-Fi 連接成功

# 發送 HTTP GET 請求至指定 URL
res = urequests.get("https://flagtech.github.io/flag.txt")  # 取得旗標檔案

# 檢查 HTTP 狀態碼是否為 200，表示成功
if res.status_code == 200:
    print(res)  # 列印 HTTP 請求的回應
    res.close()  # 關閉回應，釋放資源
    print("Success.")  # 顯示成功訊息
else:
    print("Request failed.")  # 如果狀態碼不是 200，顯示失敗訊息

# 執行垃圾回收，釋放未使用的記憶體
gc.collect()  # 清理垃圾

# 顯示程式執行完畢
print("done")  # 顯示程式完成
