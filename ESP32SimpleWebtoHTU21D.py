import network         # 匯入 network 模組以使用網路功能
import socket          # 匯入 socket 模組以建立網路連接
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
from HTU21D import HTU21D  # HTU21D 溫濕度感測器
from myLib import *  # 使用者自訂函式庫
import ssd1306  # SSD1306 OLED 顯示模組
from machine import Pin, SoftI2C  # 進行 GPIO 操作和 SoftI2C 通訊
import utime  # 提供時間延遲功能

# 初始化 SoftI2C 通訊，指定 SCL 和 SDA 的 GPIO 腳位，以及通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 初始化 SSD1306 OLED 顯示模組，解析度為 128x32，並使用 I2C 通訊
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 清除 OLED 顯示模組的畫面
display.fill(0)  # 用黑色填充整個畫面
display.show()  # 更新 OLED 顯示模組

# 在 OLED 上顯示 MAC 地址（假設 GetMAC() 函式從某個地方取得 MAC 地址）
display.text(GetMAC(), 0, 0, 1)  # 在位置 (0, 0) 顯示 MAC 地址

# 初始化 HTU21D 溫濕度感測器，使用 SoftI2C 通訊
lectura = HTU21D(22, 21)
temp=0
hum=0
# 設定 Wi-Fi 的 SSID 和密碼
ssid='NCNUIOT'
pwd='12345678'

# 設定為站點模式 (STA_IF) 的 Wi-Fi 物件
wifi = network.WLAN(network.STA_IF)

# 檢查是否已連接到 Wi-Fi
if not wifi.isconnected():	#如果以連接上網路
    print('connecting to network...')  # 打印連接信息
    wifi.active(True)                  # 啟用 Wi-Fi 連接
    wifi.connect(ssid, pwd)            # 連接到指定的 Wi-Fi 網路
    while not wifi.isconnected():      # 等待連接成功
        pass

print(wifi.ifconfig())                 # 打印連接成功後的網路配置

# 創建一個網路套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#創建 Socket 物件，
#使用 socket.socket() 方法來創建一個新的 socket 物件。這個方法需要兩個參數：
#AF_INET：表示使用 IPv4 地址。
#SOCK_STREAM：表示使用 TCP 協議。

s.bind(('', 80))                        # 綁定到本機 IP 和埠 80
#使用 bind() 方法來綁定 socket 到一個特定的地址和埠。這個方法需要一個元組作為參數，包含 IP 地址和埠號。
s.listen(5)                             # 設定最多允許 5 個連接
#使用 listen() 方法使 socket 開始監聽進入的連接。參數指定可以排隊的最大連接數

def read_htu21d():
    t = h = 0
    #temp = 0
    #hum = 0
    try:
        h = lectura.humidity  # 取得濕度
        t = lectura.temperature  # 取得溫度
        print('Humidity:', h)  # 輸出濕度
        print('Temperatura:', t)  # 輸出溫度

        # 清除 OLED 顯示模組的畫面
        display.fill(0)  # 用黑色填充整個畫面
        
        # 在 OLED 上顯示 MAC 地址（假設 GetMAC() 函式從某個地方取得 MAC 地址）
        display.text(GetMAC(), 0, 0, 1)  # 在位置 (0, 0) 顯示 MAC 地址
        # 在 OLED 上顯示溫度和濕度資訊
        display.rect(0, 10, 128, 10, 0, 1)  # 繪製橫線
        display.text('Temp:' + str(temp), 0, 10, 1)  # 在位置 (0, 10) 顯示溫度
        display.rect(0, 20, 128, 10, 0, 1)  # 繪製另一個橫線
        display.text('Humid:' + str(hum), 0, 20, 1)  # 在位置 (0, 20) 顯示濕度
        # 更新 OLED 顯示模組的內容，將新的資訊顯示出來
        display.show()
    except OSError as e:
        print("read sensor error")
        #return('Failed to read sensor.')
    return t,h    
    #return temp , hum
# 定義一個返回 HTML 網頁的函數

#def web_page(t,h):
def web_page():
    # 定義 HTML 頁面內容
    html ="""
    <html>
        <head lang=\'zh-tw\'>
            <meta charset = \'UTF-8\' http-equiv="refresh" content="5" />
            <title>顯示溫溼度感測器資料 modified from 動手玩MicroPython- ESP32物聯網互動設計</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                html{
                        font-family: Helvetica;
                        display: inline-block;
                        margin: 0px auto;
                        text-align: center;
                        color: #09F;
                    }
                    h1{
                        color: #FF9900;
                        padding: 2vh;
                    }
                p{font-size:1.5rem;}
            </style>        </head>
        <body>
            <h1>顯示溫溼度感測器資料 modified from 動手玩MicroPython- ESP32物聯網互動設計 written by 楊明豐</h1> 
            <h1> <span>Temperature</span> 
                <span>"""+str(temp)+"""</span>
                <sub>&deg;C</sub></h1>
            <h1> <span>Humidity</span>
                <span>"""+str(hum)+"""</span>
                <sub>%</sub></h1>
        </body>
        </html>
    """
    return html                         # 返回 HTML 字串

while True:	#永久迴圈，使其網頁在一直等待再被連接狀態
    client, addr = s.accept()           # 接受來自客戶端的連接
    #使用 accept() 方法來接受一個新的連接。此方法會阻塞直到有新的連接，返回一個新的 socket 物件和客戶端地址。
    temp,hum = read_htu21d()
    print("in temp:",temp)
    print("in humid:",hum)
    
    response = web_page()               # 生成 HTML 回應
    #response = web_page()               # 生成 HTML 回應
    #使用 send() 或 sendall() 方法向客戶端發送數據。
    # 在控制台顯示溫濕度資訊
    print(response)
    client.send('HTTP/1.1 200 OK\n')    # 發送 HTTP 回應狀態
    client.send('Content-Type: text/html\n') # 發送內容類型
    client.send('Connection: close\n\n')     # 關閉連接
    client.sendall(response)            # 發送所有 HTML 回應
    client.close()                      # 關閉客戶端連接，使用 close() 方法關閉 socket 連接。
    #utime.sleep(5)