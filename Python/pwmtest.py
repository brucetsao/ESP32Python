# 引入 MicroPython 的 Pin、PWM 和時間相關模組
from machine import Pin, PWM  # 用於控制 GPIO 和 PWM
from time import sleep  # 用於時間相關操作

# 初始化蜂鳴器的引腳和 PWM 物件
buzzerPIN = 7  # 設定蜂鳴器的引腳
BuzzerObj = PWM(Pin(buzzerPIN))  # 使用指定引腳初始化 PWM 物件

# 定義控制蜂鳴器的函數
def buzzer(buzzerPinObject, frequency, sound_duration, silence_duration):
    # 設定占空比為正值，以發出蜂鳴器的聲音
    buzzerPinObject.duty_u16(int(65536 * 0.1))  # 設定占空比
    # 設定蜂鳴器的頻率
    buzzerPinObject.freq(frequency)  # 設定頻率
    # 等待聲音持續時間
    sleep(sound_duration)  # 等待指定的聲音持續時間
    # 設定占空比為零，以停止聲音
    buzzerPinObject.duty_u16(int(65536 * 0))  # 停止蜂鳴器
    # 等待靜音時間，如果需要
    sleep(silence_duration)  # 等待指定的靜音時間

# 定義音符到頻率的對應表
do5 = 523  # do 音符的頻率
dod5 = 554  # dod 音符的頻率
re5 = 587  # re 音符的頻率
red5 = 622  # red 音符的頻率
mi5 = 659  # mi 音符的頻率
fa5 = 698  # fa 音符的頻率
fad5 = 739  # fad 音符的頻率
sol5 = 784  # sol 音符的頻率
sold5 = 830  # sold 音符的頻率
la5 = 880  # la 音符的頻率
lad5 = 932  # lad 音符的頻率
si5 = 987  # si 音符的頻率

# 播放一段音符序列
buzzer(BuzzerObj, mi5, 0.1, 0.1)  # 播放指定的音符序列
# 重複播放不同音符，根據所需的持續時間和靜音時間
# 這裡省略了中間的重複代碼，以簡化說明

# 停用蜂鳴器
BuzzerObj.deinit()  # 停用 PWM，關閉蜂鳴器
