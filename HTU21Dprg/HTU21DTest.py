# 這段 MicroPython 程式碼的主要功能是與 HTU21D 溫濕度感測器通訊，
# 這個程式碼不斷從 HTU21D 感測器取得溫度和濕度數據，
# 顯示內容包括溫濕度數據以。

# 匯入所需的模組，包括 HTU21D、SSD1306 OLED 顯示模組、Pin 和 SoftI2C，以及 utime
from HTU21D import HTU21D  # 使用 HTU21DF 溫濕度感測器
from myLib import *  # 使用者自訂函式庫
from machine import Pin, SoftI2C  # 使用 Pin 和 SoftI2C 套件
import utime  # 引入 utime 套件，提供時間延遲等功能

# 使用 SoftI2C 通訊，設定 SDA 和 SCL 的 GPIO 引腳和通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 建立 HTU21D 感測器的實例，使用 SDA 和 SCL 的腳位
lectura = HTU21D(22, 21)

# 進入無窮迴圈，不斷獲取並顯示溫濕度資訊
while True:
    # 取得溫濕度數據
    hum = lectura.humidity  # 取得濕度
    temp = lectura.temperature  # 取得溫度

    # 在控制台輸出溫濕度數據
    print('Humedad:', hum)  # 輸出濕度
    print('Temperatura:', temp)  # 輸出溫度

    # 休息 2 秒
    utime.sleep(2)  # 等待兩秒鐘
