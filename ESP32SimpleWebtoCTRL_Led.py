import network         # 匯入 network 模組以使用網路功能
import socket          # 匯入 socket 模組以建立網路連接
from machine import Pin # 匯入 machine 模組中的 Pin 類來控制硬體腳位

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


led = Pin(2, Pin.OUT)                   # 創建一個控制 GPIO2 的 Pin 物件作為輸出
led.value(0)                            # 將 LED 的初始狀態設為關閉 (0)

gpio_state = 'OFF'                      # 設定 LED 的狀態為關閉

# 定義一個返回 HTML 網頁的函數
def web_page():
    if led.value() == 1:                # 檢查 LED 的狀態
        gpio_state = 'ON'               # 如果 LED 開啟，設為 'ON'
    else:
        gpio_state = 'OFF'              # 如果 LED 關閉，設為 'OFF'
    
    # 定義 HTML 頁面內容
    html ="""
    <html>
        <head lang=\'zh-tw\'>
            <meta charset = \'UTF-8\'>
            <title>MicroPython Web Server modified from 動手玩MicroPython- ESP32物聯網互動設計</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                html{font-family: Helvetica;display:inline-block;margin:0px auto;text-align:center;}
                h1{color: #0F3376; padding:2vh;}
                p{font-size:1.5rem;}
                .button{
                    background-color:Yellow;
                    border:none; 
                    border-radius:4px;
                    color:blue;
                    padding:none;
                    font-size:30px;
                    margin:2px;
                    cursor:pointer;
                    width:240px;
                    height:100px;}
                .button2{background-color:Green;}            
            </style>
        </head>
        <body>
            <h1>MicroPython Web Server modified from 動手玩MicroPython- ESP32物聯網互動設計 written by 楊明豐</h1> 
            <p>LED : """ + gpio_state + """</p>  <!-- 顯示當前 LED 的狀態 -->
            <a href="/?led=on"><button class="button">ON</button></a>  <!-- LED 開啟按鈕 -->
            <a href="/?led=off"><button class="button button2">OFF</button></a>  <!-- LED 關閉按鈕 -->
        </body>
        </html>
    """
    return html                         # 返回 HTML 字串

while True:	#永久迴圈，使其網頁在一直等待再被連接狀態
    client, addr = s.accept()           # 接受來自客戶端的連接
    #使用 accept() 方法來接受一個新的連接。此方法會阻塞直到有新的連接，返回一個新的 socket 物件和客戶端地址。
    print('Got a connection from %s' % str(addr))  # 打印客戶端地址
    request = client.recv(1024)         # 接收客戶端的請求數據
    #使用 recv() 方法從客戶端接收數據。此方法需要指定最多接收的字節數
    request = str(request)              # 將請求數據轉換為字串
    led_on = request.find('/?led=on')   # 查找是否有開啟 LED 的請求
    led_off = request.find('/?led=off') # 查找是否有關閉 LED 的請求

    if led_on == 6:                     # 如果請求中包含 '/?led=on'
        led.value(1)                    # 開啟 LED
    if led_off == 6:                    # 如果請求中包含 '/?led=off'
        led.value(0)                    # 關閉 LED

    response = web_page()               # 生成 HTML 回應
    #使用 send() 或 sendall() 方法向客戶端發送數據。
    client.send('HTTP/1.1 200 OK\n')    # 發送 HTTP 回應狀態
    client.send('Content-Type: text/html\n') # 發送內容類型
    client.send('Connection: close\n\n')     # 關閉連接
    client.sendall(response)            # 發送所有 HTML 回應
    client.close()                      # 關閉客戶端連接，使用 close() 方法關閉 socket 連接。