# 引入 MicroPython 的網路模組
import network  # 用於網路連接和操作

# 初始化 Wi-Fi 物件，使用 STA（站點）模式
wifi = network.WLAN(network.STA_IF)  # STA_IF 表示站點模式
wifi.active(True)  # 啟用 Wi-Fi

# 斷開當前連接（如果有）
wifi.disconnect()  # 確保 Wi-Fi 未連接到任何網路

# 掃描附近的 Wi-Fi 接入點（Access Points）
aps = wifi.scan()  # 掃描可用的 Wi-Fi 網路

# 遍歷掃描結果，顯示每個接入點的資訊
for ap in aps:  # 對於每個接入點
    for x in ap:  # 遍歷接入點的每個屬性
        # 顯示屬性的類型和值
        print("type:", type(x), end="/")  # 打印屬性類型
        print(x, end=",")  # 打印屬性值
    # 每個接入點後插入分隔符
    print("\n==========================\n")
