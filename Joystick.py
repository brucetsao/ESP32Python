# 引入 MicroPython 的 Pin、ADC 和時間相關模組
from machine import Pin, ADC  # 用於控制 GPIO 和模擬數位轉換器
import utime  # 用於延遲和時間相關操作

# 初始化 ADC 和按鈕
xAxis = ADC(Pin(27))  # 使用 GPIO 27 作為 x 軸的 ADC 輸入
yAxis = ADC(Pin(26))  # 使用 GPIO 26 作為 y 軸的 ADC 輸入
button = Pin(17, Pin.IN, Pin.PULL_UP)  # 使用 GPIO 17 作為按鈕，啟用上拉電阻

# 無限迴圈，持續讀取 ADC 和按鈕狀態
while True:
    xValue = xAxis.read_u16()  # 讀取 x 軸的 ADC 值
    yValue = yAxis.read_u16()  # 讀取 y 軸的 ADC 值
    buttonValue = button.value()  # 讀取按鈕狀態
    buttonStatus = "not pressed"  # 初始化按鈕狀態

    # 根據按鈕值更新按鈕狀態
    if buttonValue == 0:  # 如果按鈕被按下
        buttonStatus = "pressed"  # 更新按鈕狀態為 "pressed"

    # 列印 ADC 和按鈕的值
    print(
        "X: " + str(xValue) + ", Y: " + str(yValue) + " -- button value: " + str(buttonValue) + " button status: " + buttonStatus
    )
    # 暫停 0.2 秒，避免迴圈過於頻繁
    utime.sleep(0.2)  # 延遲 0.2 秒
