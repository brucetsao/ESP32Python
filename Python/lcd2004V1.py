from lcd_i2c import LCD		#使用LCD 1602/2004 chip I2C
from machine import I2C, Pin		#使用I2C與GPIO腳位之函式庫
 
# 定义 LCD 的 I2C 地址、行数和列数
I2C_ADDR = 0x27		#使用LCD 1602/2004  I2C address is 	0x27
NUM_ROWS = 2		#使用LCD 1602/2004  row amount is 2		
NUM_COLS = 16		#使用LCD 1602/2004  column amount is 16		
	
 
# 定义 I2C 接口对象，使用指定的引脚和频率初始化
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=800_000)		#I2C pin(SDA=pin6,SCL=Pin7
         
# 创建 LCD 对象，并传入所需的参数
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)	#declare
#declare lcd object as LCD Package( address is I2C_ADDR = 0x27	,cols=NUM_COLS = 16,rows=NUM_ROWS = 2, I2C communication object is i2c=i2c
# 初始化 LCD 显示屏
lcd.begin()		#init lcd display
 
# 在 LCD 显示屏上打印字符串 "Hello World"
lcd.print("Hello World!")	#print "Hello World!" on lcd display