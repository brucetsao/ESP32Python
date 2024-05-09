# 引入 MicroPython 中的時間和硬體模組
import time  # 用於時間相關操作，如 sleep
from machine import Pin, PWM  # 用於控制 GPIO 和 PWM

# 設定 PWM 引腳
pwm_pins = [18, 19, 20]  # 指定 PWM 引腳
# 初始化 PWM 物件，並放入列表中
pwms = [PWM(Pin(pwm_pins[0])), PWM(Pin(pwm_pins[1])), PWM(Pin(pwm_pins[2]))]  # 建立 PWM 物件列表
# 為每個 PWM 物件設置頻率
[pwm.freq(1000) for pwm in pwms]  # 設定每個 PWM 的頻率為 1000 Hz

# 定義 16 位呼吸燈效果的步進值
step_val = 64  # 每個步進的值
# 定義亮度從低到高的範圍
range_0 = [ii for ii in range(0, 2**16, step_val)]  # 亮度增強的範圍
# 定義亮度從高到低的範圍
range_1 = [ii for ii in range(2**16, -step_val, -step_val)]  # 亮度降低的範圍

# 無限循環
while True:  # 不斷執行迴圈
    # 通過 PWM 產生紅、藍、綠的呼吸燈效果
    for pwm in pwms:  # 遍歷每個 PWM 物件
           for ii in range_0 + range_1:  # 遍歷亮度增強和降低的範圍
               pwm.duty_u16(ii)  # 設定 PWM 的占空比（16 位）
               time.sleep(0.001)  # 在每次更改 PWM 之間等待 1 毫秒

    # 產生白色呼吸燈效果（同時控制三個 LED）
    for ii in range_0 + range_1:  # 遍歷亮度增強和降低的範圍
        for pwm in pwms:  # 對於每個 PWM 物件
            pwm.duty_u16(ii)  # 設定 PWM 的占空比
        time.sleep(0.001)  # 在每次更改 PWM 之間等待 1 毫秒
