
from machine import Pin #GPIO 腳位所用之套件
import utime#Delay程式所用之套件
#led = Pin(x, Pin.OUT)
# x = GPIOn的 n

#led = Pin(n, Pin.OUT) GPIO n腳位，
#並定義其腳位為輸出模式(由CPUI向外部輸出電力:以電壓 高低來控制
led = Pin(16, Pin.OUT)
#Pin.OUT表輸出電位，Pin.IN表偵測腳位電位
#定義led_onboard 板載GPIO0 或 板載LED 字樣的GPIO 腳位

while True:
    #led_onboard.toggle()
    led.on()#設定led_onboard腳位物件為高電位
    utime.sleep(2)#休息兩秒鐘
    led.off()#設定led_onboard腳位物件為低電位
    utime.sleep(1)#休息兩秒鐘
# led_onboard.toggle() ==> led_onboard.on() and  led_onboard.off()


led = Pin(16, Pin.OUT)

while True:
    #led_onboard.toggle()
    led.on()
    utime.sleep(2)
    led.off()
    utime.sleep(1)
# led_onboard.toggle() ==> led_onboard.on() and  led_onboard.off()