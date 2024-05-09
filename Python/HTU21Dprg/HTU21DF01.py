# 這段 MicroPython 程式碼使用 SoftI2C 
# 初始化並設定 I2C 通訊的 SCL 和 SDA 腳位，
# 然後用 micropython_htu21df 庫初始化 HTU21DF 溫濕度感測器。
# 程式碼的關鍵步驟如下：
# 
#     設定 SoftI2C 通訊，指定 SCL 和 SDA 腳位，以及 I2C 通訊頻率。
#     初始化 HTU21DF 溫濕度感測器。
#     獲取溫度和濕度讀數。
#     將溫度和濕度讀數顯示在終端。
from machine import Pin, I2C, SoftI2C  # 引入 Pin、I2C 和 SoftI2C 模塊，用於 I2C 通訊
from micropython_htu21df import htu21df  # 引入 HTU21DF 溫濕度感測器的 MicroPython 驅動

# 初始化 SoftI2C，指定 SCL 和 SDA 腳位，以及通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 或者可以使用硬體 I2C
# i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 初始化 HTU21DF 溫濕度感測器
htu21df = htu21df.HTU21DF(i2c)  # 使用 I2C 通訊初始化 HTU21DF 感測器

# 獲取溫度和濕度讀數
temp = htu21df.temperature  # 獲取溫度值
rh = htu21df.humidity  # 獲取濕度值

# 顯示溫度和濕度資訊
print("Temperature:", temp)  # 顯示溫度
print("Humidity:", rh)  # 顯示濕度
