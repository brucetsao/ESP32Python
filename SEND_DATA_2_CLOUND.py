import network  # 匯入網路相關的功能模組
import urequests as requests  # 匯入 HTTP 請求功能模組
# 建立 WLAN 物件，使用 STA_IF 代表客戶端模式
wlan = network.WLAN(network.STA_IF)

# 啟用 WLAN 功能
wlan.active(True)

# 設定 SSID 和密碼
ssidstr = "NCNUIOT"
ssidpwd = "12345678"

# 嘗試連接到無線網路，使用 SSID 和密碼
status = wlan.connect(ssidstr, ssidpwd)

# 定義一個目標網址
urlstr = "http://iot.arduino.org.tw:8888/bigdata/dhtdata/dhDatatadd.php?MAC=%s&T=%3.1f&H=%3.1f"
#urlstr = "http://localhost:8888/bigdata/bmp/bmpDatatadd.php?MAC=AABBCCDDEEFF&P=1034.3&T=27.3"
#urlstr = "http://localhost:8888/bigdata/bmp/bmpDatatadd.php?MAC=%s&P=%5.1f&T=%3.1f"
# 打印連接狀態
print(status)

# 檢查是否成功連接到無線網路
if wlan.isconnected():
    # 打印網路配置資訊
    print(wlan.ifconfig())
    print("IP:", wlan.ifconfig()[0])  # 打印 IP 地址
    print("MASK:", wlan.ifconfig()[1])  # 打印子網路遮罩
    print("GateWay:", wlan.ifconfig()[2])  # 打印網關地址
    print("DNS:", wlan.ifconfig()[3])  # 打印 DNS 伺服器地址
 
 
macstr = GetMAC()  # 取得 MAC 地址（假設 GetMAC() 函式從某個地方取得 MAC 地址）

# 在 OLED 上顯示 MAC 地址
display.text(macstr, 0, 0, 1)  # 在位置 (0, 0) 顯示 MAC 地址


# 進入無窮迴圈，定期讀取並顯示溫濕度資訊
while True:
#   這裡寫讀感測器

    # RESTFul API，用 HTTP GET 送資料
    # 檢查無線網路是否已成功連接
    if wlan.isconnected():
        # 發送 HTTP GET 請求
        urlstr2 = urlstr % (macstr, temp, hum)  # 轉換變數內容到 HTTP GET 的 URL 字串
        #把新的格式化字串，根據所需要的格式化變數的個數，位置與對應的格式，一一填回去
        res = requests.get(urlstr2)  # 發送 HTTP GET 請求並取得回應
        
        # 打印從目標網址獲取的回應內容
        print("HTML is:", res.text)
    else:
        # 如果連接失敗，打印錯誤訊息
        print("Connect AP Fail")

    # 暫停 30 秒，然後再執行下一個迭代
    utime.sleep(30)
 