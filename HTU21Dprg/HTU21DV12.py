# 這段 MicroPython 程式碼執行以下操作：
# 
# 連接 Wi-Fi 網路
# 使用 SoftI2C 通訊方式初始化 SSD1306 OLED 顯示模組
# 讀取 HTU21D 溫濕度感測器數據，並將結果顯示在 OLED 上
# 根據讀取的溫濕度數據生成一個網址，並透過 HTTP GET 請求將資料傳送到伺服器
# 將伺服器的回應顯示在控制台
# 這段程式碼在無限循環中執行下列操作：
# 
# 連接 Wi-Fi 網路
# 讀取 HTU21D 溫濕度感測器的數據
# 將溫濕度數據顯示在 OLED 上
# 根據讀取的數據生成網址並發送 HTTP GET 請求
# 如果連接 Wi-Fi 失敗，顯示錯誤訊息
# 每 30 秒重複執行上述步驟。

# 匯入必要的模組，用於 Wi-Fi 連接、HTTP 請求、時間控制、和 OLED 顯示
import network
import urequests as requests  # 使用 HTTP 請求
import time  # 時間控制

# 匯入自訂 HTU21D 溫濕度感測器模組、自訂函式庫、SSD1306 OLED 顯示模組
from HTU21D import HTU21D  # 使用 HTU21D 溫濕度感測器
from myLib import *  # 使用自訂函式庫
import ssd1306  # 使用 SSD1306 OLED 顯示模組
from machine import Pin, SoftI2C, I2C  # 用於腳位控制和 I2C 通訊
import utime  # 延遲用的時間套件

# 初始化 Wi-Fi 網路為 STA_IF (Station Interface)
wlan = network.WLAN(network.STA_IF) 
wlan.active(True)  # 啟用 Wi-Fi 網路

# 連接 Wi-Fi 網路，並檢查連接狀態
status = wlan.connect("NUKIOT", "12345678")  # 連接指定 SSID 和密碼
print(status)  # 顯示連接狀態

# 初始化 SoftI2C 通訊
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 初始化 OLED 顯示模組，解析度為 128x32
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 取得 MAC 地址，並將其存入變數
macstr = GetMAC()

# 建立 URL 模板，用於上傳溫濕度數據
urlstr0 = "http://iot.arduino.org.tw:8888/bigdata/dhtdata/dhDatatadd.php?MAC=%s&T=%3.2f&H=%3.1f" 

# 清除 OLED 顯示模組的畫面
display.fill(0)	
display.show()  # 更新 OLED 顯示

# 在 OLED 顯示 MAC 地址
display.text(macstr, 0, 0, 1) 

# 初始化 HTU21D 溫濕度感測器
lectura = HTU21D(22, 21)

# 進入無限循環，持續讀取溫濕度數據
while True:
    # 讀取濕度和溫度
    hum = lectura.humidity
    temp = lectura.temperature

    # 顯示溫濕度在控制台
    print('Humedad:', hum)  
    print('Temperatura:', temp)  

    # 在 OLED 顯示溫度
    display.rect(0, 10, 128, 10, 0, 1)  
    display.text('Temp:' + str(temp), 0, 10, 1)  

    # 在 OLED 顯示濕度
    display.rect(0, 20, 128, 10, 0, 1)  
    display.text('Humid:' + str(hum), 0, 20, 1)  

    # 更新 OLED 顯示模組
    display.show()  

    # 生成 URL 以傳送溫濕度數據
    urlstr = urlstr0 % (macstr, temp, hum)
    print(urlstr)  # 在控制台顯示 URL

    # 如果 Wi-Fi 已經連接
    if wlan.isconnected():
        print(wlan.ifconfig())  # 顯示網路配置
        # 取得網路配置並顯示
        print("IP:", wlan.ifconfig()[0])
        print("MASK:", wlan.ifconfig()[1])
        print("GateWay:", wlan.ifconfig()[2])
        print("DNS:", wlan.ifconfig()[3])

        # 發送 HTTP GET 請求
        res = requests.get(urlstr)
        print("HTML is:", res.text)  # 顯示伺服器的回應
    else:
        print("Connect AP Fail")  # 連接失敗時顯示訊息

    # 等待 30 秒，再次進行循環
    utime.sleep(30)
