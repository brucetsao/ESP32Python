# 這段 MicroPython 程式碼主要用於從 HTU21D 溫濕度感測器讀取數據，
# 並將這些數據顯示在 SSD1306 OLED 顯示模組上。
# 程式碼中使用 SoftI2C 與感測器和 OLED 顯示模組進行通訊。
# 這段程式碼反覆執行，
# 讀取 HTU21D 溫濕度感測器的數據，
# 並將溫度和濕度資訊顯示在 SSD1306 OLED 顯示模組上，
# 並在控制台輸出這些數據。
# 同時，在顯示溫度和濕度之前，
# 程式碼會清除 OLED 的畫面，
# 以確保顯示的數據是最新的。

# 匯入必要的模組，包括 HTU21D、SSD1306 OLED 顯示模組、機器控制和時間管理模組
import network  # 匯入網路相關的功能模組
import urequests as requests  # 匯入 HTTP 請求功能模組
import time  # 匯入時間相關功能模組
# 匯入使用者自訂函式庫
from HTU21D import HTU21D  # HTU21D 溫濕度感測器
from myLib import *  # 使用者自訂函式庫
import ssd1306  # SSD1306 OLED 顯示模組
from machine import Pin, SoftI2C  # 進行 GPIO 操作和 SoftI2C 通訊
import utime  # 提供時間延遲功能

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
    
# 初始化 SoftI2C 通訊，指定 SCL 和 SDA 的 GPIO 腳位，以及通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 初始化 SSD1306 OLED 顯示模組，解析度為 128x32，並使用 I2C 通訊
display = ssd1306.SSD1306_I2C(128, 32, i2c)
macstr = GetMAC()  # 取得 MAC 地址（假設 GetMAC() 函式從某個地方取得 MAC 地址）

# 清除 OLED 顯示模組的畫面
display.fill(0)  # 用黑色填充整個畫面
display.show()  # 更新 OLED 顯示模組

# 在 OLED 上顯示 MAC 地址
display.text(macstr, 0, 0, 1)  # 在位置 (0, 0) 顯示 MAC 地址

# 初始化 HTU21D 溫濕度感測器，使用 SoftI2C 通訊
lectura = HTU21D(22, 21)

# 進入無窮迴圈，定期讀取並顯示溫濕度資訊
while True:
    # 讀取溫濕度感測器數據
    hum = lectura.humidity  # 取得濕度
    temp = lectura.temperature  # 取得溫度

    # 在控制台顯示溫濕度資訊
    print('Humedad:', hum)  # 輸出濕度
    print('Temperatura:', temp)  # 輸出溫度

    # 清除 OLED 顯示模組的畫面
    display.fill(0)  # 用黑色填充整個畫面
    
    # 在 OLED 上顯示 MAC 地址
    display.text(macstr, 0, 0, 1)  # 在位置 (0, 0) 顯示 MAC 地址

    # 在 OLED 上顯示溫度和濕度資訊
    display.text('Temp:' + str(temp), 0, 10, 1)  # 在位置 (0, 10) 顯示溫度
    display.text('Humid:' + str(hum), 0, 20, 1)  # 在位置 (0, 20) 顯示濕度

    # 更新 OLED 顯示模組的內容，將新的資訊顯示出來
    display.show()

    # RESTFul API，用 HTTP GET 送資料
    # 檢查無線網路是否已成功連接
    if wlan.isconnected():
        # 發送 HTTP GET 請求
        urlstr2 = urlstr % (macstr, temp, hum)  # 轉換變數內容到 HTTP GET 的 URL 字串
        print(urlstr2)
        res = requests.get(urlstr2)  # 發送 HTTP GET 請求並取得回應
        
        # 打印從目標網址獲取的回應內容
        print("HTML is:", res.text)
    else:
        # 如果連接失敗，打印錯誤訊息
        print("Connect AP Fail")

    # 暫停 30 秒，然後再執行下一個迭代
    utime.sleep(30)
