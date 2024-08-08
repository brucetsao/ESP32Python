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


relay1 = Pin(5, Pin.OUT)                   # 創建一個控制 GPIO5 的 Pin 物件作為輸出
relay1.value(0)                            # 將 繼電器模組 的初始狀態設為關閉 (0)
relay2 = Pin(12, Pin.OUT)                   # 創建一個控制 GPIO12 的 Pin 物件作為輸出
relay2.value(0)                            # 將 繼電器模組 的初始狀態設為關閉 (0)
relay3 = Pin(14, Pin.OUT)                   # 創建一個控制 GPIO14 的 Pin 物件作為輸出
relay3.value(0)                            # 將 繼電器模組 的初始狀態設為關閉 (0)

gpio1_state = 'OFF'                      # 設定 繼電器模組 的狀態為關閉
gpio2_state = 'OFF'                      # 設定 繼電器模組 的狀態為關閉
gpio3_state = 'OFF'                      # 設定 繼電器模組 的狀態為關閉

# 定義一個返回 HTML 網頁的函數
def web_page():
    if relay1.value() == 1:                # 檢查 繼電器模組 的狀態
        gpio1_state = '開啟'               # 如果 繼電器模組 開啟，設為 'ON'
    else:
        gpio1_state = '關閉'              # 如果 繼電器模組 關閉，設為 'OFF'

    if relay2.value() == 1:                # 檢查 繼電器模組 的狀態
        gpio2_state = '開啟'               # 如果 繼電器模組 開啟，設為 'ON'
    else:
        gpio2_state = '關閉'              # 如果 繼電器模組 關閉，設為 'OFF'

    if relay3.value() == 1:                # 檢查 繼電器模組 的狀態
        gpio3_state = '開啟'               # 如果 繼電器模組 開啟，設為 'ON'
    else:
        gpio3_state = '關閉'              # 如果 繼電器模組 關閉，設為 'OFF'


    # 定義 HTML 頁面內容
    html ="""
    <html>
        <head lang=\'zh-tw\'>
            <meta charset = \'UTF-8\'>
            <title>控制多組繼電器之網站 modified from 動手玩MicroPython- ESP32物聯網互動設計</title>
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
            <h1>控制多組繼電器之網站 modified from 動手玩MicroPython- ESP32物聯網互動設計 written by 楊明豐</h1> 
            <p>第一組繼電器模組: """ + gpio1_state + """</p>  <!-- 顯示當前 繼電器模組 的狀態 -->
            <a href="/?d1=on"><button class="button">ON</button></a>  <!-- 繼電器模組 開啟按鈕 -->
            <a href="/?d1=off"><button class="button button2">OFF</button></a>  <!-- 繼電器模組 關閉按鈕 -->
            <hr>
            <p>第二組繼電器模組: """ + gpio2_state + """</p>  <!-- 顯示當前 繼電器模組 的狀態 -->
            <a href="/?d2=on"><button class="button">ON</button></a>  <!-- 繼電器模組 開啟按鈕 -->
            <a href="/?d2=off"><button class="button button2">OFF</button></a>  <!-- 繼電器模組 關閉按鈕 -->
            <hr>
            <p>第三組繼電器模組: """ + gpio3_state + """</p>  <!-- 顯示當前 繼電器模組 的狀態 -->
            <a href="/?d3=on"><button class="button">ON</button></a>  <!-- 繼電器模組 開啟按鈕 -->
            <a href="/?d3=off"><button class="button button2">OFF</button></a>  <!-- 繼電器模組 關閉按鈕 -->
            <hr>
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
    device1_on = request.find('/?d1=on')   # 查找是否有開啟 繼電器模組 的請求
    device1_off = request.find('/?d1=off') # 查找是否有關閉 繼電器模組 的請求
    device2_on = request.find('/?d2=on')   # 查找是否有開啟 繼電器模組 的請求
    device2_off = request.find('/?d2=off') # 查找是否有關閉 繼電器模組 的請求
    device3_on = request.find('/?d3=on')   # 查找是否有開啟 繼電器模組 的請求
    device3_off = request.find('/?d3=off') # 查找是否有關閉 繼電器模組 的請求

    if device1_on == 6:                     # 如果請求中包含 '/?dx=on'
        relay1.value(1)                    # 開啟 繼電器模組
    if device1_off == 6:                    # 如果請求中包含 '/?dx=off'
        relay1.value(0)                    # 關閉 繼電器模組

    if device2_on == 6:                     # 如果請求中包含 '/?dx=on'
        relay2.value(1)                    # 開啟 繼電器模組
    if device2_off == 6:                    # 如果請求中包含 '/?dx=off'
        relay2.value(0)                    # 關閉 繼電器模組

    if device3_on == 6:                     # 如果請求中包含 '/?dx=on'
        relay3.value(1)                    # 開啟 繼電器模組
    if device3_off == 6:                    # 如果請求中包含 '/?dx=off'
        relay3.value(0)                    # 關閉 繼電器模組

    response = web_page()               # 生成 HTML 回應
    #使用 send() 或 sendall() 方法向客戶端發送數據。
    client.send('HTTP/1.1 200 OK\n')    # 發送 HTTP 回應狀態
    client.send('Content-Type: text/html\n') # 發送內容類型
    client.send('Connection: close\n\n')     # 關閉連接
    client.sendall(response)            # 發送所有 HTML 回應
    client.close()                      # 關閉客戶端連接，使用 close() 方法關閉 socket 連接。
