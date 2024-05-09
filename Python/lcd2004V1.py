# 引入 LCD 控制模組和 MicroPython 中的 I2C、Pin 模組
from lcd_i2c import LCD  # 使用 LCD I2C 的控制模組
from machine import I2C, Pin  # 用於 I2C 通訊和 GPIO 控制

# 定義 LCD 的 I2C 地址、行數和列數
I2C_ADDR = 0x27  # LCD 的 I2C 地址為 0x27
NUM_ROWS = 2  # LCD 的行數為 2
NUM_COLS = 16  # LCD 的列數為 16

# 定義 I2C 接口對象，使用指定的腳位和頻率進行初始化
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=800_000)  # 初始化 I2C 通訊，使用 SDA 和 SCL 腳位

# 創建 LCD 對象，並傳入所需的參數
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)  # 創建 LCD 物件，指定 I2C 地址、行數和列數，以及 I2C 通訊對象

# 初始化 LCD 顯示屏
lcd.begin()  # 開始初始化 LCD 顯示器

# 在 LCD 顯示屏上打印字符串 "Hello World"
lcd.print("Hello World!")  # 在 LCD 顯示器上顯示 "Hello World"
