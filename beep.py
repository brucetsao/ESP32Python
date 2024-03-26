#擴充板揚聲器測試程式(beep.py)
from machine import Pin, Timer	#時間 套件
import utime	#時間 套件

buzzer_onboard = Pin(4, Pin.OUT)	#外接揚聲器的腳位

while True:
    #buzzer_onboard.toggle()
    buzzer_onboard.on()		#設定外接揚聲器的腳位高電位
    utime.sleep(2)		#延遲兩秒鐘
    buzzer_onboard.off()	#設定外接揚聲器的腳位低電位
    utime.sleep(1)		#延遲兩秒鐘
# buzzer_onboard.toggle() ==> buzzer_onboard.on() and  buzzer_onboard.off()