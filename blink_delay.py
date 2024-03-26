from machine import Pin	#GPIO 腳位所用，
import utime
#led = Pin(25, Pin.OUT)


led_onboard = Pin(14, Pin.OUT)

while True:
    #led_onboard.toggle()
    led_onboard.on()
    utime.sleep(2)
    led_onboard.off()
    utime.sleep(1)
# led_onboard.toggle() ==> led_onboard.on() and  led_onboard.off()