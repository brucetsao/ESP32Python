from machine import Pin, I2C	#使用I2C與GPIO腳位之函式庫
import ssd1306		#使用OLED 128XX chip SSD1306

#from machine import Pin	
from time import sleep	#=匯入time 套件，使用sleep 物件
import dht		#使用DHTXX 溫濕度感測元件
 
sensor = dht.DHT22(Pin(16)) 	#產生連接腳位GPIO16之DHT22 溫濕度感測元件之操控物件sensor
#sensor1 = dht.DHT11(Pin(16)) 
# using default address 0x3C
#i2c = I2C(sda=Pin(1), scl=Pin(2))
i2c = I2C(id=1,scl=Pin(7),sda=Pin(6),freq=100_000)
#產生i2c 物件， 用I2C 類別產生，id=哪一組I2C, scl=Pin(GPIO號碼),sda=Pin(GPIO號碼)
display = ssd1306.SSD1306_I2C(128, 32,i2c)
#產生oled物件，解析度為128x32,通訊物件為i2c
display.fill(0)
display.show()	#更新螢幕資料並顯示內容於OLED

while True:
    sensor.measure()		#呼叫腳位GPIO16之DHT22 溫濕度感測元件進行量測溫濕度
    temp = sensor.temperature()	#取得腳位GPIO16之DHT22 溫濕度感測元件之溫度
    hum = sensor.humidity()	#取得腳位GPIO16之DHT22 溫濕度感測元件之濕度
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    txt1 = "Temperature:%3.1f" % temp
    txt2 = "Humidity:%3.1f" % hum
    print(txt1)
    print(txt2)
    display.fill(0)
    display.text(txt1, 0, 0, 1)	#顯示'Hello, World!' 於位置*=(0,0) 
    display.text(txt2, 0, 10, 1)		#顯示'MicroPython Numebr1' 於位置*=(0,0)
    display.show()	#更新螢幕資料並顯示內容於OLED
    sleep(2)	#暫停兩秒鐘 