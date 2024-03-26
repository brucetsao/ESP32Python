from machine import Pin #GPIO 腳位所用之套件
import utime#Delay程式所用之套件
#led_onboard = Pin(0, Pin.OUT)  <==> Pin('LED', Pin.OUT)
#定義led_onboard 板載GPIO0 或 板載LED 字樣的GPIO 腳位，
#並定義其腳位為輸出模式(由CPUI向外部輸出電力:以電壓 高低來控制
led_onboard = Pin(2, Pin.OUT)
#定義led_onboard 板載GPIO0 或 板載LED 字樣的GPIO 腳位

while True:
    #led_onboard.toggle()
    led_onboard.on()#設定led_onboard腳位物件為高電位
    utime.sleep(2)#休息兩秒鐘
    led_onboard.off()#設定led_onboard腳位物件為低電位
    utime.sleep(1)#休息兩秒鐘
# led_onboard.toggle() ==> led_onboard.on() and  led_onboard.off()