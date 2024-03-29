from machine import Pin, I2C, SoftI2C
from micropython_htu21df import htu21df
import time
i2c = SoftI2C(scl=Pin(22),sda=Pin(21),freq=100_000)
#i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100_000)
htu = htu21df.HTU21DF(i2c)

while True:
    print(f"Temperature: {htu.temperature:.2f}°C")
    print(f"Humidity: {htu.humidity:.2%}%")
    print("")
    time.sleep(1)