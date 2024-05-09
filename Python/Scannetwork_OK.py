# 引入 MicroPython 的網路、請求、時間和二進位 ASCII 轉換模組
import network  # 用於網路連接和操作
import urequests  # 用於發送 HTTP 請求
import time  # 用於時間相關操作
import binascii  # 用於二進位和 ASCII 的轉換

# 初始化 WLAN 物件
wlan = network.WLAN()  # 使用預設 WLAN（通常是 STA 模式）
wlan.active(True)  # 啟用 WLAN

# 掃描附近的 Wi-Fi 網路
networks = wlan.scan()  # 返回一個包含 6 個元素的元組列表（SSID、BSSID、頻道、RSSI、加密方式、是否隱藏）

# 打印掃描到的網路
print(networks)  # 打印所有掃描到的網路

# 根據 RSSI 值排序（從高到低）
networks.sort(key=lambda x: x[3], reverse=True)  # 按照 RSSI 排序，從高到低

# 打印排序後的網路列表
i = 0  # 初始化計數器
for w in networks:  # 遍歷排序後的網路
    i += 1  # 計數器遞增
    # 打印網路的 SSID、BSSID（轉換為十六進位）、頻道、RSSI、加密方式和是否隱藏
    print(i, w[0].decode(), binascii.hexlify(w[1]).decode(), w[2], w[3], w[4], w[5])
