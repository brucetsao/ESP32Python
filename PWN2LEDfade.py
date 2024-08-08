from machine import Pin,PWM #GPIO 腳位所用之套件
import time#Delay程式所用之套件
Led_PWN = PWM(Pin(5)) 
#Led_PWN(LED模組) 使用PW連接GPIO5腳位

Led_PWN.freq(1000)#設定PWM寬度為1000
while True:
    for x in range(1,1000,3):#從1到1000開始loop
        Led_PWN.duty(x)#以迴圈值X來設定PWM的輸出(Duty)
        time.sleep_ms(3)#延遲3 ms
    #time.sleep(2)
    for x in range(1000,1,-3):#從1000到1開始loop
        Led_PWN.duty(x)#以迴圈值X來設定PWM的輸出(Duty)
        time.sleep_ms(3)#延遲3 ms
    time.sleep(2)#延遲2 秒