# 這個程式嘗試建立無線網路連接，
# 然後使用 MicroPython 的 urequests 套件發送 HTTP GET 請求到特定網址。
# 程式的主要功能包括：
# 
#     啟用 WLAN，並連接到指定的 Wi-Fi 網路。
#     如果連接成功，打印網路相關資訊，如 IP 地址、子網路遮罩、網關和 DNS。
#     如果連接成功，發送 HTTP GET 請求到指定網址，並打印 HTTP 回應的內容。
#     如果連接失敗，打印連接失敗的訊息。
import network  # 匯入網路相關的功能模組
import urequests as requests  # 匯入 HTTP 請求功能模組
import time  # 匯入時間相關功能模組

# 建立 WLAN 物件，使用 STA_IF 代表客戶端模式
wlan = network.WLAN(network.STA_IF)

# 啟用 WLAN 功能
wlan.active(True)

# 嘗試連接到無線網路，使用 SSID 和密碼
status = wlan.connect("NUKIOT", "12345678")

# 定義一個目標網址，本例子是靜宜大學網址
urlstr = "https://www.pu.edu.tw/"

# 打印連接狀態
print(status)

# 檢查無線網路是否已成功連接
if wlan.isconnected():
    # 打印網路配置資訊
    print(wlan.ifconfig())
    print("IP:", wlan.ifconfig()[0])  # 打印 IP 地址
    print("MASK:", wlan.ifconfig()[1])  # 打印子網路遮罩
    print("GateWay:", wlan.ifconfig()[2])  # 打印網關地址
    print("DNS:", wlan.ifconfig()[3])  # 打印 DNS 伺服器地址
    
    # 發送 HTTP GET 請求
    res = requests.get(urlstr)
    
    # 打印從目標網址獲取的回應內容
    print("HTML is:", res.text)
else:
    # 如果連接失敗，打印錯誤訊息
    print("Connect AP Fail")
