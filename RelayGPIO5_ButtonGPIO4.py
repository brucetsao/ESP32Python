from machine import Pin #GPIO 腳位所用之套件
import utime#Delay程式所用之套件
relay_GPIO5 = Pin(5, Pin.OUT)
#定義relay_GPIO5(Relay模組) 連接GPIO5腳位
button_GPIO4 = Pin(4, Pin.IN)
#定義button_GPIO4 連接GPIO4腳位

while True:
    print(button_GPIO4.value())
    #led_onboard.toggle()
    if (button_GPIO4.value()):
        print("Relay is activated")
        relay_GPIO5.on()#設定繼電器模組觸發腳位為高電位
       
    else:
        print("Relay is not activated")
        relay_GPIO5.off()#設定繼電器模組觸發腳位為低電位
           