from st7735c import ST7735
from machine import Pin,SPI
import time
 
# 初始化SPI
spi=SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))

# 初始化LCD  rot 是显示方向，bgr是默认显示的颜色
lcd= ST7735 (128, 160, spi,dc=Pin(21),cs=Pin(16),rst=Pin(22),rot=2,bgr=0)

lcd.font_load('./font/GB2312-12.fon') # 加载字体 

lcd.text("MicroPython嵌入式学习",2,5,0x5836)
lcd.text("Perseverance9527",16,19,0xff45)
lcd.text("Perseverance9527",16,33,0x07e0)
lcd.text("Perseverance9527",16,47,0xf800)
lcd.text("Perseverance9527",16,61,0xFFE0)
lcd.text("Perseverance9527",16,75,0xEF7D)
lcd.text("Perseverance9527",16,89,0x4208)
lcd.text("Perseverance9527",16,104,0x001f)
lcd.text("Perseverance9527",16,119,0x4208)
lcd.text("Perseverance9527",16,133,0x00ff)
lcd.text("Perseverance9527",16,147,0x0fff)
lcd.show() # 显示出来 