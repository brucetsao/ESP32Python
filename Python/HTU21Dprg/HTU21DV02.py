# 這段 MicroPython 程式碼用於初始化 SoftI2C 通訊，
# 並與 HTU21D 溫濕度感測器通信。
# 程式的主要功能和註解如下：
# 
#     匯入必要的模組，包括 HTU21D、自訂函式庫，以及 MicroPython 的腳位和 I2C 通訊功能。
#     初始化 SoftI2C 通訊，指定 SCL 和 SDA 的腳位，以及通訊頻率。
#     建立 HTU21D 感測器的實例，傳入 SCL 和 SDA 的腳位號碼。
#     透過實例獲取濕度和溫度數據。
#     將取得的溫度和濕度數據打印到控制台。
from HTU21D import HTU21D  # 匯入 HTU21D 模組以使用溫濕度感測器
from myLib import *  # 匯入自訂函式庫
from machine import Pin, I2C, SoftI2C  # 匯入 Pin、I2C、SoftI2C 模組以操作腳位和 I2C 通訊

# 初始化 SoftI2C 通訊，設定 SCL 和 SDA 的腳位及頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 建立 HTU21D 實例，指定 SCL 和 SDA 的腳位
lectura = HTU21D(22, 21)

# 取得濕度和溫度數據
hum = lectura.humidity  # 讀取濕度
temp = lectura.temperature  # 讀取溫度

# 輸出溫度和濕度到控制台
print('濕度: ', hum)  # 輸出濕度
print('溫度: ', temp)  # 輸出溫度
