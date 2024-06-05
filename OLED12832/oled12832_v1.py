# 這個程式示範了如何在 MicroPython 中使用 SSD1306 OLED 顯示器，
# 並使用軟體 I2C 進行通訊。它包含以下步驟：
# 
#     匯入必要的模組，包括 SoftI2C 用於軟體 I2C 通訊，Pin 用於設定 GPIO 腳位，ssd1306 用於 OLED 顯示。
#     創建 SoftI2C 物件，並指定 SDA 和 SCL 的腳位以及通訊頻率。
#     使用創建的 SoftI2C 物件來初始化 SSD1306 OLED 顯示物件，並設定解析度為 128x32。
#     清除顯示，以確保沒有殘留的資料。
#     使用 display.text() 方法在指定位置顯示文字。
#     使用 display.show() 來更新 OLED 顯示，使文本可見。
from machine import Pin, SoftI2C, I2C  # 匯入 MicroPython 的 GPIO 和 I2C 功能模組
import ssd1306  # 匯入 SSD1306 顯示驅動模組，用於 OLED 顯示

# 使用預設的 I2C 地址 0x3C
# 創建 SoftI2C 物件，指定 SDA 和 SCL 的腳位以及頻率
# 也可以選擇使用硬體 I2C，如下所示：
# i2c = I2C(sda=Pin(1), scl=Pin(2))
# 這裡選擇軟體 I2C，指定 SDA 為 Pin 21，SCL 為 Pin 22，頻率為 100,000 Hz
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# 創建 SSD1306_OLED 顯示物件，解析度為 128x32，並且使用剛創建的 SoftI2C 物件
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 清除顯示，確保沒有殘留的資料
display.fill(0)
display.show()  # 更新 OLED 顯示

# 在指定位置 (x, y) 顯示文本，並設定文本顏色 (1 表示亮)
display.text('Hello, World!', 0, 0, 1)  # 在 (0, 0) 顯示 'Hello, World!'
display.text('SoftI2C Test', 0, 10, 1)  # 在 (0, 10) 顯示 'SoftI2C Test'

# 更新 OLED 顯示
display.show()
