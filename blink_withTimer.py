# 引入 Pin 和 Timer 類別，用於 GPIO 控制和計時器
from machine import Pin, Timer

# 初始化 LED 腳位，設定為輸出模式
led = Pin("LED", Pin.OUT)  # "LED" 是特定開發板上內建 LED 的標識符

# 建立 Timer 物件
tim = Timer()  # 建立計時器實例

# 定義計時器的回調函式
def tick(timer):  # 當計時器觸發時執行此函式
    global led  # 使用全域變數 led
    led.toggle()  # 切換 LED 的狀態，開或關

# 初始化計時器
tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)  
# 設定計時器的頻率為 2.5 Hz，模式為週期性，並將回調函式設為 tick
