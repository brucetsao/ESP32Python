# 引入 MicroPython 的網路和通訊相關模組
import network  # 用於網路功能
import ubinascii  # 用於二進位與十六進位的轉換
import requests  # 用於 HTTP 請求
import socket  # 用於建立網路通訊

# 定義函式 GetMAC，用於取得裝置的 MAC 地址
def GetMAC():
    wlan = network.WLAN(network.STA_IF)  # 使用 STA 模式
    wlan.active(True)  # 啟用無線網路
    mac = ubinascii.hexlify(wlan.config('mac')).decode()  # 取得 MAC 地址並轉換為十六進位表示
    return mac.upper()  # 將 MAC 地址轉換為大寫並回傳

# 定義函式 GetMAC2，用於取得裝置的 MAC 地址並允許指定分隔符
def GetMAC2(sepc):
    wlan = network.WLAN(network.STA_IF)  # 使用 STA 模式
    wlan.active(True)  # 啟用無線網路
    mac = ubinascii.hexlify(wlan.config('mac'), sepc).decode()  # 使用指定的分隔符轉換為十六進位
    return mac.upper()  # 將 MAC 地址轉換為大寫並回傳

# 定義函式 http_get，用於發送 HTTP GET 請求
def http_get(url):
    # 解析 URL 以取得主機和路徑
    print("in http get", url)
    _a, _b, host0, path = url.split('/', 3)  # 分割 URL
    host, port = host0.split(':', 1)  # 分割主機和埠號
    print("變數:", _a, "/", _b, "/", host, "/", path, "/", port)

    # 備註：這段程式碼已註解，可能是預備建立 HTTP 請求的步驟
    # addr = socket.getaddrinfo(host0, port)[0][-1]  # 取得主機的地址資訊
    # s = socket.socket()  # 建立一個 socket 物件
    # s.connect(addr)  # 連接到地址
    # s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))  # 送出 HTTP GET 請求

    # 從伺服器接收資料並列印
    # while True:
    #     data = s.recv(100)  # 接收資料
    #     if data:  # 如果有資料
    #         print(str(data, 'utf8'), end='')  # 列印資料
    #     else:  # 如果沒有資料
    #         break
    # s.close()  # 關閉 socket

# 定義 URL 字串
urlstr = "http://iot.arduino.org.tw:8888/bigdata/dhtdata/dhDatatadd.php?MAC=5566778899AA&T=65.1&H=76"  # 預設 URL
urlstr1 = "http://iot.arduino.org.tw:8888/bigdata/dhtdata/dhDatatadd.php?MAC="  # URL 開頭
urlstr2 = "&T=65.1&H=76"  # URL 結尾

# 組合完整的 URL，包含動態取得的 MAC 地址
urlstrall = urlstr1 + GetMAC() + urlstr2  # 將 GetMAC 返回的值加到 URL 中

# 列印取得的 MAC 地址
print(GetMAC())  # 取得並列印 MAC 地址

# 列印完整的 URL
print(urlstrall)  # 列印組合好的 URL
