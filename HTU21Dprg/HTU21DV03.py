# 這段 MicroPython 程式碼用於初始化 SoftI2C 通訊，
# 並與 HTU21D 溫濕度感測器通信。
# 程式的主要功能和註解如下：
# 
#     匯入必要的模組，包括 HTU21D、自訂函式庫，以及 MicroPython 的腳位和 I2C 通訊功能。
#     初始化 SoftI2C 通訊，指定 SCL 和 SDA 的腳位，以及通訊頻率。
#     建立 HTU21D 感測器的實例，傳入 SCL 和 SDA 的腳位號碼。
#     透過實例獲取濕度和溫度數據。
#     將取得的溫度和濕度數據打印到控制台。
# 匯入所需的模組，包括 HTU21D、自訂函式庫，以及 SSD1306 OLED 顯示模組
from HTU21D import HTU21D  # 使用 HTU21D 溫濕度感測器
from myLib import *  # 使用自訂函式庫
import ssd1306  # 使用 SSD1306 OLED 顯示模組
from machine import Pin, SoftI2C  # 使用 Pin 和 SoftI2C 類別

# 初始化 SoftI2C，設定 SDA 和 SCL 的 GPIO 引腳和通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 初始化 SSD1306 OLED 顯示模組，解析度為 128x32，並使用 SoftI2C 通訊
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 清除 OLED 顯示模組的內容
display.fill(0)  # 將畫面填充為黑色
display.show()  # 更新顯示，清除之前的內容

# 在 OLED 顯示模組上顯示特定文字
display.text(GetMAC(), 0, 0, 1)  # 顯示 MAC 位址

# 初始化 HTU21D 感測器，並取得濕度和溫度數據
lectura = HTU21D(22, 21)  # 傳入 SDA 和 SCL 的腳位號碼
hum = lectura.humidity  # 取得濕度
temp = lectura.temperature  # 取得溫度

# 在控制台輸出濕度和溫度數據
print('Humedad: ', hum)  # 輸出濕度
print('Temperatura: ', abs(temp))  # 輸出溫度

# 在 OLED 顯示模組上顯示溫度和濕度數據
display.text('Temp:' + str(abs(temp)), 0, 10, 1)  # 顯示溫度
display.text('Humid:' + str(abs(hum)), 0, 20, 1)  # 顯示濕度

# 更新 OLED 顯示模組的內容
display.show()  # 更新顯示，將新的內容顯示在 OLED 上
