# 引入 MicroPython 中的 I2C、Pin 和時間相關模組
from machine import I2C  # 用於 I2C 通訊
from machine import Pin  # 用於 GPIO 控制
import utime as time  # 使用 utime 模組的時間功能

# 初始化 I2C 通訊
i2c = I2C(id=1, scl=Pin(27), sda=Pin(26), freq=100000)  # 使用 I2C 1，100 kHz 頻率

# 初始化 LCD 顯示器
lcd = I2cLcd(i2c, 0x27, 2, 16)  # 初始化 16x2 的 LCD，I2C 地址為 0x27

# 在 LCD 上顯示文本
lcd.putstr('DiY Projects Lab')  # 在 LCD 上顯示 "DiY Projects Lab"
