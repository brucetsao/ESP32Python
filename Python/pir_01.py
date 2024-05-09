# 引入 MicroPython 的 Pin 和時間相關模組
from machine import Pin  # 用於控制 GPIO
import time  # 用於時間相關操作

# 初始化 PIR 感測器和 LED
sensor_pir = Pin(28, Pin.IN)  # 初始化 GPIO 28 作為輸入，用於 PIR 感測器
led = Pin(15, Pin.OUT)  # 初始化 GPIO 15 作為輸出，用於 LED

# 定義 PIR 感測器的中斷處理程序
def pir_handler(pin):
    print("Motion detected!")  # 當偵測到動作時，打印訊息
    for i in range(50):  # 閃爍 LED 50 次
        led.toggle()  # 切換 LED 的狀態
        time.sleep_ms(100)  # 每次閃爍間隔 100 毫秒

# 設定 PIR 感測器的中斷
sensor_pir.irq(trigger=Pin.IRQ_RISING, handler=pir_handler)  # 當偵測到動作時觸發中斷

# 無限迴圈，持續切換 LED
while True:
    led.toggle()  # 切換 LED 的狀態
    time.sleep(5)  # 每 5 秒切換一次
