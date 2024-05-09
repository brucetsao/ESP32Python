# 引入 ST7735 顯示模組，支援 128x160 的 LCD
from st7735c import ST7735

# 引入 machine 模組中的 Pin 和 SPI，用於控制 GPIO 和 SPI 通訊
from machine import Pin, SPI

# 引入時間模組，用於延遲和計時
import time

# 初始化 SPI 通訊，指定通訊參數
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
# 使用 SPI2，設定波特率為 20000000，polarity 和 phase 都為 0，sck 腳位為 18，mosi 腳位為 23

# 初始化 LCD 顯示器
lcd = ST7735(128, 160, spi, dc=Pin(21), cs=Pin(16), rst=Pin(22), rot=2, bgr=0)
# ST7735(寬度, 高度, SPI 通訊, dc 腳位, cs 腳位, rst 腳位, 顯示方向, 顏色順序)

# 加載字體，用於在 LCD 上顯示中文或其他特定字體
lcd.font_load('./font/GB2312-12.fon')  # 加載字體檔案

# 在 LCD 上顯示不同的文字與顏色
lcd.text("MicroPython嵌入式学习", 2, 5, 0x5836)  # 文字，x,y 位置，顏色
lcd.text("Perseverance9527", 16, 19, 0xff45)  # 使用不同的顏色顯示文本
lcd.text("Perseverance9527", 16, 33, 0x07e0)
lcd.text("Perseverance9527", 16, 47, 0xf800)
lcd.text("Perseverance9527", 16, 61, 0xFFE0)
lcd.text("Perseverance9527", 16, 75, 0xEF7D)
lcd.text("Perseverance9527", 16, 89, 0x4208)
lcd.text("Perseverance9527", 16, 104, 0x001f)
lcd.text("Perseverance9527", 16, 119, 0x4208)
lcd.text("Perseverance9527", 16, 133, 0x00ff)
lcd.text("Perseverance9527", 16, 147, 0x0fff)

# 將所有繪製的內容顯示出來
lcd.show()  # 將緩衝區的內容顯示到 LCD
