# 引入 MicroPython 的 I2C、Pin 以及時間相關模組
from machine import I2C, Pin  # 用於 I2C 通訊和 GPIO 控制
from time import sleep  # 用於延遲

# 初始化 I2C 通訊
# i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)  # 使用 I2C 0，400 kHz
i2c = I2C(id=1, scl=Pin(7), sda=Pin(6), freq=100_000)  # 使用 I2C 1，100 kHz

# 掃描 I2C 匯流排以取得地址
I2C_ADDR = i2c.scan()[0]  # 取得第一個找到的 I2C 地址

# 初始化 I2cLcd 顯示器
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  # 使用 I2C 通訊，初始化 2 行 16 字的 LCD 顯示器
lcd.blink_cursor_on()  # 啟用游標閃爍
lcd.clear()  # 清除 LCD 顯示內容

# 在 LCD 上顯示文字
lcd.putstr("blog.csdn.net/\n")  # 顯示第一行的文字，換行
lcd.putstr("slofslb")  # 顯示第二行的文字
