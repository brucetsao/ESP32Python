# 引入必要的 MicroPython 模組
import esp  # 用於 ESP32/ESP8266 的硬體控制
import network  # 用於網路相關功能
import utime  # 提供時間相關的功能

# 停用 ESP 的 OS 偵錯訊息，減少不必要的資訊輸出
esp.osdebug(None)

# 初始化 WiFi 模組，設定為 STA_IF (站模式)，用於連接到現有的 WiFi 網路
wifi = network.WLAN(network.STA_IF)

# 啟用 WiFi 模組
wifi.active(True)

try:
    # 連接到指定的 WiFi 網路，SSID 為 'ncnuiot'，密碼為 'iot12345'
    wifi.connect('ncnuiot', 'iot12345')
    
    print('Start to connect to WiFi')  # 提示開始連接 WiFi

    # 試圖連接 WiFi 最多 10 次，每次等待 1 秒
    for i in range(10):
        print('Trying to connect to WiFi in {}s'.format(i))  # 顯示正在嘗試連接
        utime.sleep(1)  # 等待 1 秒
        if wifi.isconnected():  # 如果 WiFi 已連接
            break  # 退出迴圈

    # 檢查是否成功連接到 WiFi
    if wifi.isconnected():
        print('WiFi connection OK!')  # 連接成功
        print('Network Config =', wifi.ifconfig())  # 顯示網路設定
    else:
        print('WiFi connection Error')  # 連接失敗

# 捕獲可能發生的例外狀況，並列印錯誤訊息
except Exception as e:
    print(e)  # 列印例外狀況訊息
