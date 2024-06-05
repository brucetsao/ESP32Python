from machine import Pin, I2C  # 引入 Pin 和 I2C 函式庫
from ssd1306 import SSD1306_I2C  # 引入 SSD1306 顯示器函式庫
import utime  # 引入時間函式庫
 
WIDTH = 128  # OLED 顯示器的寬度
HEIGHT = 64  # OLED 顯示器的高度
 
# 初始化 I2C 物件，設置 I2C 線路和頻率
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)  # 設置 I2C 通訊的腳位和頻率
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)  # 初始化 SSD1306 顯示器
 
# 初始化超音波距離感測器的腳位
trigger = Pin(3, Pin.OUT)  # 設置超音波發射腳位
echo = Pin(2, Pin.IN)  # 設置超音波接收腳位
 
# 定義一個函式，用於計算距離
def ultra():
    # 初始化 trigger 脈衝
    trigger.low()  # 設置 trigger 為低
    utime.sleep_us(2)  # 等待 2 微秒
    trigger.high()  # 設置 trigger 為高
    utime.sleep_us(5)  # 等待 5 微秒
    trigger.low()  # 再次設置為低
    
    # 計算 echo 的高電平時間
    while echo.value() == 0:  # 等待 echo 變高
        signaloff = utime.ticks_us()  # 記錄信號關閉的時間
    while echo.value() == 1:  # 等待 echo 變低
        signalon = utime.ticks_us()  # 記錄信號打開的時間
    
    # 計算時間差和距離
    timepassed = signalon - signaloff  # 計算時間差
    distance = (timepassed * 0.0343) / 2  # 計算距離，聲音在空氣中的速度約為 343 米/秒
    distance = "{:.1f}".format(distance)  # 格式化距離為小數點一位
    
    print(distance + " cm")  # 印出距離
    return str(distance)  # 回傳距離字串
 
# 測試超音波感測器
print("fok")  # 印出一個訊息，表示程式開始
ngf = ultra()  # 測量距離
print(ngf)  # 印出距離
 
# 無限迴圈，更新 OLED 顯示器
while True:
    display.text(ultra(), 0, 0)  # 在 OLED 上顯示距離
    display.show()  # 顯示內容
    display.fill(0)  # 清空顯示器
    utime.sleep(1)  # 等待 1 秒
