# 引入必要的函式庫
import ESP8266WebServer  # 用於建立和管理網頁伺服器
import network  # 用於 Wi-Fi 連接
import machine  # 用於硬體操作

# 定義 GPIO 腳位號碼，這是 ESP8266 上內建 LED 的腳位（通常為 D4）
GPIO_NUM = 2

# Wi-Fi 設定
STA_SSID = "MEE_MI"  # Wi-Fi SSID
STA_PSK = "PinkFloyd1969"  # Wi-Fi 密碼

# 停用 AP 模式，僅使用 STA 模式
ap_if = network.WLAN(network.AP_IF)  # 取得 AP 模式的網路介面
if ap_if.active():  # 如果 AP 模式是啟用的
    ap_if.active(False)  # 停用 AP 模式

# 連接 Wi-Fi，如果尚未連接
sta_if = network.WLAN(network.STA_IF)  # 取得 STA 模式的網路介面
if not ap_if.active():  # 如果 AP 模式不是啟用的
    sta_if.active(True)  # 啟用 STA 模式
if not sta_if.isconnected():  # 如果 STA 模式尚未連接
    sta_if.connect(STA_SSID, STA_PSK)  # 連接到指定的 Wi-Fi 網路
    # 等待連接到 Wi-Fi
    while not sta_if.isconnected(): 
        pass  # 持續等待連接

# 顯示 IP 地址，確認伺服器已啟動
print("Server started @", sta_if.ifconfig()[0])  # 列印 IP 地址

# 獲取內建 LED 的 Pin 物件，用於控制 LED
pin = machine.Pin(GPIO_NUM, machine.Pin.OUT)  # 初始化 Pin 物件，設定為輸出模式
pin.on()  # 關閉 LED（這是因為內建 LED 通常使用 sinking input）

# 定義處理 "/cmd?led=[on|off]" 路徑的處理函式
def handleCmd(socket, args):
    if 'led' in args:  # 檢查是否有 'led' 參數
        if args['led'] == 'on':  # 如果 'led' 參數是 'on'
            pin.off()  # 開啟 LED
        elif args['led'] == 'off':  # 如果 'led' 參數是 'off'
            pin.on()  # 關閉 LED
        ESP8266WebServer.ok(socket, "200", args["led"])  # 傳回成功狀態
    else:  # 如果沒有 'led' 參數
        ESP8266WebServer.err(socket, "400", "Bad Request")  # 傳回錯誤狀態

# 啟動伺服器，並設置埠號為 8899
ESP8266WebServer.begin(8899)  # 開啟伺服器

# 註冊每個路徑的處理函式
ESP8266WebServer.onPath("/cmd", handleCmd)  # 設定 "/cmd" 路徑的處理函式

# 伺服器持續運行，處理客戶端請求
try:
    while True:
        ESP8266WebServer.handleClient()  # 處理客戶端請求
except:  # 捕獲例外狀況
    ESP8266WebServer.close()  # 關閉伺服器
