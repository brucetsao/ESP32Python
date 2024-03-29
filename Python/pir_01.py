from machine import Pin
import time
 
sensor_pir = machine.Pin(28, machine.Pin.IN)
led = machine.Pin(15, machine.Pin.OUT)
 
def pir_handler(pin): 
    print("Motion detected!") 
    for i in range(50): 
        led.toggle() 
        time.sleep_ms(100)
 
sensor_pir.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_handler)
 
while True: 
    led.toggle() 
    time.sleep(5)