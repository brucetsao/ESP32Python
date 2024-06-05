# 引入 MicroPython 中的 Pin 和 PWM 模組
from machine import Pin, PWM  # 用於控制 GPIO 和 PWM

# 定義 Servo 類，用於控制伺服馬達
class Servo(object):
    def __init__(self, pin: int = 15, hz: int = 50):
        self._servo = PWM(Pin(pin))  # 初始化 PWM 在指定的引腳上
        self._servo.freq(hz)  # 設定 PWM 頻率為 50 Hz
    
    # 設定伺服馬達的占空比
    def ServoDuty(self, duty):
        # 確保占空比在 1638 和 8190 之間
        if duty <= 1638:
            duty = 1638
        if duty >= 8190:
            duty = 8190
        self._servo.duty_u16(duty)  # 設定占空比

    # 設定伺服馬達的角度
    def ServoAngle(self, pos):
        # 確保角度在 0 和 180 之間
        if pos <= 0:
            pos = 0
        if pos >= 180:
            pos = 180
        pos_buffer = (pos / 180) * 6552  # 角度轉換為占空比
        self._servo.duty_u16(int(pos_buffer) + 1638)  # 設定占空比

    # 設定伺服馬達的脈衝時間
    def ServoTime(self, us):
        # 確保脈衝時間在 500 和 2500 微秒之間
        if us <= 500:
            us = 500
        if us >= 2500:
            us = 2500
        pos_buffer = (us / 1000) * 3276  # 將脈衝時間轉換為占空比
        self._servo.duty_u16(int(pos_buffer))  # 設定占空比

    # 停用伺服馬達
    def deinit(self):
        self._servo.deinit()  # 停用 PWM
