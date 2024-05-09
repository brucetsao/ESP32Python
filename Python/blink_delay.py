# 引入 MicroPython 的 Pin 類別，用於控制 GPIO 腳位
from machine import Pin

# 引入 utime 模組，用於時間延遲和計時
import utime

# 建立一個 Pin 物件，控制板上內建的 LED
# led = Pin(25, Pin.OUT)  # 這行已註解，可能是控制內建 LED 的腳位

# 建立一個 Pin 物件，控制 14 號腳位上的 LED
led_onboard = Pin(14, Pin.OUT)  # 設定 14 號腳位為輸出模式

# 無窮迴圈，持續執行開關 LED 的操作
while True:
    # 打開 LED
    led_onboard.on()  # 設定 LED 腳位為高電位，打開 LED
    utime.sleep(2)  # 等待 2 秒
    
    # 關閉 LED
    led_onboard.off()  # 設定 LED 腳位為低電位，關閉 LED
    utime.sleep(1)  # 等待 1 秒
    
    # 此處的註解說明另一種方法：開關切換
    # led_onboard.toggle()  # 切換 LED 的狀態，打開或關閉
    # 此行被註解掉，取而代之的是分別使用 `led_onboard.on()` 和 `led_onboard.off()`
