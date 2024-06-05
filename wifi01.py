# 這個程式使用 MicroPython 建立一個無線網路連接，
# 並嘗試連接到指定的 Wi-Fi 網路。
# 程式中包括了檢查連接狀況、
# 獲取網路配置以及處理連接失敗的情況。
# 主要部分包括：
# 
#     使用 network.WLAN() 建立無線網路物件並啟用。
#     使用 connect() 方法連接到指定的 Wi-Fi 網路。
#     延遲 1 秒，以確保有足夠的時間進行連接。
#     確認連接狀態並打印相關的網路資訊，如 IP 地址、子網路遮罩、網關、以及 DNS 伺服器地址。
#     如果連接失敗，打印錯誤訊息。
import network  # 匯入網路連接套件
import utime  # 匯入時間相關函式庫，用於延遲

# 建立 WLAN 物件，指定 STA_IF 表示客戶端模式
wlan = network.WLAN(network.STA_IF)

# 啟用 WLAN 功能
wlan.active(True)

# 嘗試連接到指定的無線網路 (SSID 為 "NCNUIOT"，密碼為 "12345678")
status = wlan.connect("NCNUIOT", "12345678")

# 暫停 1 秒鐘
utime.sleep(1) 

# 打印連接狀態
print(status)

# 檢查無線網路是否已成功連接
if wlan.isconnected():
    # 打印網路配置
    print(wlan.ifconfig())
    
    # 取得並打印 IP 地址
    print("IP:", wlan.ifconfig()[0])
    
    # 取得並打印子網路遮罩
    print("MASK:", wlan.ifconfig()[1])
    
    # 取得並打印網關地址
    print("GateWay:", wlan.ifconfig()[2])
    
    # 取得並打印 DNS 伺服器地址
    print("DNS:", wlan.ifconfig()[3])
else:
    # 如果連接失敗，打印錯誤訊息
    print("Connect AP Fail")
