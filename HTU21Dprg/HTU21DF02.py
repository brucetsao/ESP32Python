# 這段 MicroPython 程式碼
# 實現了不斷讀取 HTU21DF 溫濕度感測器的溫度和濕度資訊
# 並將其打印到控制台。程式碼的關鍵部分如下：
# 
#     使用 SoftI2C 初始化 I2C 通訊，指定 SCL 和 SDA 腳位，以及 I2C 通訊頻率。
#     使用 SoftI2C 初始化 HTU21DF 溫濕度感測器。
#     使用無窮迴圈不斷讀取溫度和濕度資訊，並將其以適當的格式顯示在控制台。
#     加入 1 秒的延時，避免迴圈過於頻繁。
#     
# 
# 
# 
# 
from machine import Pin, I2C, SoftI2C  # 引入 Pin、I2C 和 SoftI2C 模塊，用於 I2C 通訊
from micropython_htu21df import htu21df  # 引入 HTU21DF 溫濕度感測器的 MicroPython 驅動
import time  # 引入 time 模塊，用於延時

# 初始化 SoftI2C，指定 SCL 和 SDA 腳位，以及通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 或者使用硬體 I2C
# i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 使用 SoftI2C 連接 HTU21DF 感測器
htu = htu21df.HTU21DF(i2c)  # 初始化 HTU21DF 感測器

# 不斷讀取溫度和濕度資訊
while True:  # 進入無窮迴圈
    # 讀取溫度並顯示，格式化為帶有兩位小數的浮點數
    print(f"Temperature: {htu.temperature:.2f}°C")
    # 讀取濕度並顯示，格式化為百分比
    print(f"Humidity: {htu.humidity:.2%}")
    print("")  # 輸出一個空行作為分隔
    time.sleep(1)  # 等待 1 秒
