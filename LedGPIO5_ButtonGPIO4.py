from machine import Pin #GPIO 腳位所用之套件
import utime#Delay程式所用之套件
led_GPIO5 = Pin(5, Pin.OUT)
#定義led_GPIO5 連接GPIO5腳位
button_GPIO4 = Pin(4, Pin.IN)
#定義button_GPIO4 連接GPIO4腳位

while True:
    print(button_GPIO4.value())
    #led_onboard.toggle()
    if (button_GPIO4.value()):
        print("button is pressed")
        led_GPIO5.on()#設定led_GPIO5腳位物件為高電位
       
    else:
        print("button is not pressed")
        led_GPIO5.off()#設定led_GPIO5腳位物件為低電位
           