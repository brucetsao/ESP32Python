# 這段 MicroPython 程式碼包含了三個函數，
# 用於獲取裝置的 MAC 位址。以下是這些函數的詳細註解：
# 這些函數主要用於 MicroPython 上的裝置，
# 使用網路功能來獲取該裝置的 MAC 位址。這對於識別裝置、
# 進行網路相關操作等用途非常有用。
# 每個函數的主要區別在於返回的 MAC 位址格式，
# 其中 GetMAC2 使用空格分隔，
# GetMACn 則可以自訂分隔符。


import network  # 匯入網路功能套件
import ubinascii  # 用於特殊數字轉16進位和轉換為字串的套件
import socket  # 用於網路通訊的套件

def GetMAC():
    """取得裝置的 MAC 位址"""
    wlan = network.WLAN(network.STA_IF)  # 初始化 WLAN 物件，以正常上網模式 (STA_IF)
    wlan.active(True)  # 啟動 WLAN
    mac = ubinascii.hexlify(network.WLAN().config('mac')).decode()  # 取得網卡的 MAC 位址，並將其轉換為十六進制字串
    # 這個過程通過 ubinascii.hexlify 轉換為十六進制，再用 decode() 將位元組轉換為字串
    return mac.upper()  # 回傳大寫格式的 MAC 位址

def GetMAC2():
    """取得裝置的 MAC 位址，帶有空格分隔"""
    wlan = network.WLAN(network.STA_IF)  # 初始化 WLAN 物件，以正常上網模式 (STA_IF)
    wlan.active(True)  # 啟動 WLAN
    mac = ubinascii.hexlify(network.WLAN().config('mac'), " ").decode()  # 取得 MAC 位址，並將其轉換為十六進制，帶空格分隔
    return mac.upper()  # 回傳大寫格式的 MAC 位址

def GetMACn(sepc):
    """取得裝置的 MAC 位址，使用指定的分隔符"""
    wlan = network.WLAN(network.STA_IF)  # 初始化 WLAN 物件，以正常上網模式 (STA_IF)
    wlan.active(True)  # 啟動 WLAN
    mac = ubinascii.hexlify(network.WLAN().config('mac'), sepc).decode()  # 取得 MAC 位址，並使用指定的分隔符
    # ubinascii.hexlify(目標位元組, 分隔符).decode() 用來將 MAC 位址轉換為十六進制字串
    return mac.upper()  # 回傳大寫格式的 MAC 位址
