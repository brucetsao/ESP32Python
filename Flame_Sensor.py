# 引入 MicroPython 的 Pin 和 PWM 類別，用於控制 GPIO 和 PWM 功能
from machine import Pin, PWM

# 引入 utime 模組，用於時間相關操作
import utime

# 初始化火焰感測器和蜂鳴器的腳位
flame_sensor = Pin(16, Pin.IN)  # 連接到 GPIO 16 的火焰感測器
buzzer = Pin(17, Pin.OUT)  # 連接到 GPIO 17 的蜂鳴器

# 等待 0.5 秒以確保硬體初始化完成
utime.sleep(0.5)  # 暫停 0.5 秒

# 關閉蜂鳴器（初始化狀態）
buzzer.high()  # 設定高電位以關閉蜂鳴器

# 初始化馬達控制腳位
In1 = Pin(1, Pin.OUT)  # 連接到 GPIO 1 的控制腳位
In2 = Pin(0, Pin.OUT)  # 連接到 GPIO 0 的控制腳位
EN_A = PWM(Pin(2))  # 連接到 GPIO 2 的 PWM 腳位，用於控制馬達速度

# 設定 PWM 頻率
EN_A.freq(1500)  # 將 PWM 頻率設定為 1500 Hz

# 設定 PWM 的預設占空比
duty_cycle = 65535  # 最大值 65535 表示 100% 占空比

# 無限迴圈，持續檢測火焰感測器的狀態
while True:
    while flame_sensor.value() == 1:  # 如果偵測到火焰
        print("Flame Detected")  # 列印訊息
        
        buzzer.low()  # 開啟蜂鳴器
        In1.low()  # 停止馬達
        In2.high()  # 啟動馬達
        EN_A.duty_u16(int(duty_cycle / 2))  # 將馬達速度設定為 50% 占空比
    
    if flame_sensor.value() == 0:  # 如果沒有偵測到火焰
        buzzer.high()  # 關閉蜂鳴器
        In1.low()  # 停止馬達
        In2.low()  # 停止馬達
        print("No Flame")  # 列印訊息

    # 短暫休息，以避免迴圈過於頻繁
    utime.sleep(0.2)  # 暫停 0.2 秒
