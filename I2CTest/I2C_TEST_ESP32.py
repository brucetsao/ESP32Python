# 這段程式碼示範了如何使用 MicroPython 掃描 I2C bus，以查找已連接的設備。
# 該程式碼會掃描兩組 I2C 通訊，並根據掃描結果顯示相關資訊。
# 
#     主要步驟包括：
#     
#     使用 I2C 類別建立兩組 I2C 通訊，並指定 SDA 和 SCL 腳位。
#     掃描 I2C bus，並根據掃描結果，判斷找到的設備數量。
#     顯示掃描結果，包括 I2C 通訊的編號和找到的設備地址。
#     依據掃描結果，顯示不同的訊息，例如 "Nothing connected"（沒有連接任何設備）或 "More than one device is connected"（連接了多於一個設備）。
from machine import Pin, SoftI2C  # 引入 Pin 和 SoftI2C 套件，用於軟體模擬 I2C 通訊
import ssd1306  # 引入 SSD1306 OLED 顯示器驅動

# 使用預設 I2C 地址 0x3C 來進行 OLED 顯示器通訊
# 使用 SoftI2C 方法進行軟體模擬 I2C 通訊
# 初始化 I2C 並指定 SDA 和 SCL 腳位
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)  # 設定 SCL 和 SDA 腳位，以及 I2C 通訊頻率
# 產生 I2C 物件，指定 SDA 和 SCL 腳位，頻率為 100,000 Hz

# 掃描 I2C bus，並獲取連接到 I2C bus 的所有設備地址
addr_list = i2c.scan()  # 掃描 I2C bus 以查找所有連接的設備

# 判斷掃描結果
if len(addr_list) >= 1:  # 如果找到至少一個 I2C 設備
    print("in I2C(%d)" % 1)  # 顯示目前正在使用的 I2C 編號
    # 列出所有找到的 I2C 設備
    for x in addr_list:
        # 顯示 I2C 設備的地址
        print("I2C Address: %x" % x)  # 以十六進制格式顯示 I2C 地址
        print("Have a device connected")  # 表示已找到設備
else:
    # 如果沒有找到任何設備
    if len(addr_list) == 0:
        print("in I
