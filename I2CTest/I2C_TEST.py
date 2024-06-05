# 這段程式碼示範了如何使用 MicroPython 掃描 I2C bus，以查找已連接的設備。
# 該程式碼會掃描兩組 I2C 通訊，並根據掃描結果顯示相關資訊。
# 
#     主要步驟包括：
#     
#     使用 I2C 類別建立兩組 I2C 通訊，並指定 SDA 和 SCL 腳位。
#     掃描 I2C bus，並根據掃描結果，判斷找到的設備數量。
#     顯示掃描結果，包括 I2C 通訊的編號和找到的設備地址。
#     依據掃描結果，顯示不同的訊息，例如 "Nothing connected"（沒有連接任何設備）或 "More than one device is connected"（連接了多於一個設備）。
from machine import I2C, Pin  # 匯入 I2C 和 GPIO 套件

# 初始化 I2C 通訊
# 第一組 I2C (id=1)，設定 SCL 和 SDA 的腳位，通訊頻率 100,000 Hz
i2c = I2C(id=1, scl=Pin(7), sda=Pin(6), freq=100_000)
# 第二組 I2C (id=0)，設定 SCL 和 SDA 的腳位，通訊頻率 100,000 Hz
i2c0 = I2C(id=0, scl=Pin(9), sda=Pin(8), freq=100_000)

# 掃描 I2C bus 以查找已連接的設備
addr_list = i2c.scan()  # 掃描第一組 I2C，有哪些設備連接在 I2C bus 上
# 根據掃描結果，解決設備訊息
if len(addr_list) >= 1:  # 如果找到至少一個設備
    print("in I2C(%d)" % 1)  # 顯示正在使用的 I2C 編號
    for x in addr_list:  # 列出找到的所有 I2C 設備
        # who = i2c.readfrom_mem(x, 0x00, 1)  # 讀取 I2C 設備屬性
        print(x)  # 顯示 I2C 設備的地址
        print("Have a device connected")  # 顯示設備已連接
        # print("address is :(%x)" % int(who[0]))  # 顯示設備地址
# 若沒有找到任何設備
elif len(addr_list) == 0:
    print("in I2C(%d)" % 1)
    print("Nothing connected")  # 顯示沒有連接任何設備
# 若找到多於一個設備
else:
    print("More than one device is connected")  # 顯示找到多於一個設備

# 掃描第二組 I2C，尋找已連接的設備
addr_list = i2c0.scan()  # 掃描第二組 I2C
# 根據掃描結果，解決設備訊息
if len(addr_list) >= 1:  # 如果找到至少一個設備
    print("in I2C(%d)" % 0)  # 顯示第二組 I2C 編號
    for x in addr_list:  # 列出找到的所有 I2C 設備
        # who = i2c0.readfrom_mem(x, 0x00, 1)  # 讀取 I2C 設備屬性
        print(x)  # 顯示 I2C 設備的地址
        print("Have a device connected")  # 顯示設備已連接
        # print("address is :(%x)" % who[0])  # 顯示設備地址
# 若沒有找到任何設備
elif len(addr_list) == 0:
    print("Nothing connected")  # 顯示沒有連接任何設備
# 若找到多於一個設備
else:
    print("More than one device is connected")  # 顯示找到多於一個設備
