# 這個 MicroPython 程式示範了如何使用 SSD1306 OLED 顯示器，
# 並在螢幕上顯示文本。主要步驟包括：
# 
#     匯入必要的套件，包括硬體 I2C、軟體 I2C、GPIO、SSD1306 OLED 顯示驅動。
#     建立 I2C 物件，並指定 SDA 和 SCL 的腳位。
#     創建 SSD1306_OLED 物件，指定解析度與 I2C 通訊物件。
#     清除 OLED 顯示，使螢幕為黑色。
#     使用 display.text() 在指定的位置上顯示文本。
#     使用 display.show() 來更新 OLED 螢幕，使顯示內容生效。
from machine import Pin, SoftI2C, I2C  # 匯入 MicroPython 的 GPIO、軟體 I2C、硬體 I2C 套件
import ssd1306  # 匯入 SSD1306 套件，用於 OLED 顯示
from myLib import *  # 匯入自訂函數庫

# 使用預設地址 0x3C 來建立 I2C 物件，並設定 SDA 與 SCL 的腳位
i2c = I2C(sda=Pin(21), scl=Pin(22))  # 設定 I2C 通訊腳位

# 也可以選擇使用軟體 I2C
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 創建 SSD1306_I2C 物件，解析度為 128x32，使用剛創建的 I2C 物件
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 清除 OLED 顯示，將螢幕填滿黑色
display.fill(0)
display.show()  # 更新並顯示螢幕內容

# 顯示一系列文本於 OLED 上，並指定顯示位置與顏色
# 使用 display.text(文字, x 位置, y 位置, 顏色)
# 顏色值 1 表示亮，0 表示暗
display.text('Hello, World!', 0, 10, 1)  # 在 (0, 10) 顯示 'Hello, World!'
display.text('SoftI2C Test', 0, 20, 1)  # 在 (0, 20) 顯示 'SoftI2C Test'
display.text('SoftI2C Test2', 0, 30, 1)  # 在 (0, 30) 顯示 'SoftI2C Test2'

print("OK")  # 在控制台顯示 OK

# 更新並顯示 OLED 螢幕的內容
display.show()
