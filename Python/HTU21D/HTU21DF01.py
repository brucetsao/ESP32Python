from machine import Pin, I2C, SoftI2C
from micropython_htu21df import htu21df
i2c = SoftI2C(scl=Pin(22),sda=Pin(21),freq=100_000)
#i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100_000)
htu21df = htu21df.HTU21DF(i2c)
temp = htu21df.temperature
rh = htu21df.humidity
print("Temperature:",temp)
print("Humity:",rh)
