#Pico/W Breadboard擴充板外接按鈕測試程式(button2LedOn.py)

from machine import Pin, Timer	#腳位套件
import utime		#時間 套件

#led = Pin(25, Pin.OUT)
led_onboard = Pin(2, Pin.OUT)	#GPIO 輸出
#button_onboard = Pin(6, Pin.IN)		#GPIO 輸入

interrupt_flag=1	#設定按鈕狀態為1

button_onboard = Pin(6,Pin.IN,Pin.PULL_UP)
#設定按鈕於 GPIO6，並設定為壓下去驅動

led_onboard.on()
#預設LED燈為亮起

def callback(pin):# 設定插斷函式
    global interrupt_flag	#設定按鈕狀態為全域變數
    #interrupt_flag=1
    interrupt_flag = interrupt_flag * (-1)
    #每案一次按鈕，按鈕狀態 *(-1)==>反相
    
button_onboard.irq(trigger=Pin.IRQ_FALLING, handler=callback)
#將按鈕與插斷建立連接，並設定處裡函式為callback



while True:
    #utime.sleep(1)
    #led_onboard.toggle()
    if interrupt_flag ==1 :#如果按鈕狀態為1
        led_onboard.on()	#LED燈亮
    else:
        led_onboard.off()	#LED燈滅
# led_onboard.toggle() ==> led_onboard.on() and  led_onboard.off()