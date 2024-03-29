from machine import I2C, Pin
from time import sleep


#i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
i2c = I2C(id=1,scl=Pin(7),sda=Pin(6),freq=100_000)
I2C_ADDR = i2c.scan()[0]

lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.blink_cursor_on()
lcd.clear()
lcd.putstr("blog.csdn.net/\n")
lcd.putstr("slofslb")
