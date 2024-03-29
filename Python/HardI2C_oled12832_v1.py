from machine import Pin, I2C	#使用I2C與GPIO腳位之函式庫
#from machine import Pin, SoftI2C
#from machine import Pin, I2C	#使用I2C與GPIO腳位之函式庫
import ssd1306	#使用OLED 128XX chip SSD1306

# using default address 0x3C
#i2c = I2C(sda=Pin(1), scl=Pin(2))
i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100_000)
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
#產生i2c 物件， 用I2C 類別產生，id=哪一組I2C, scl=Pin(GPIO號碼),sda=Pin(GPIO號碼)
display = ssd1306.SSD1306_I2C(128, 32,i2c)
#產生oled物件，解析度為128x32,通訊物件為i2c

display.fill(0)	
display.show()	#更新螢幕資料並顯示內容於OLED


display.text('Hello, World!', 0, 0, 1)	#顯示'Hello, World!' 於位置*=(0,0) 
display.text('Hardware Test', 0, 10, 1)		#顯示'MicroPython Numebr1' 於位置*=(0,0) 

display.show()	#更新螢幕資料並顯示內容於OLED

