#
import time		#=匯入time 套件，使用sleep 物件
from machine import Pin,PWM
 
pwm_pins = [18,19,20] # set PWM pins
pwms = [PWM(Pin(pwm_pins[0])),PWM(Pin(pwm_pins[1])),
                PWM(Pin(pwm_pins[2]))] # pwm array
[pwm.freq(1000) for pwm in pwms] # set pwm freqs
 
step_val = 64 # step value for 16-bit breathing
range_0 = [ii for ii in range(0,2**16,step_val)] # brightening
range_1 = [ii for ii in range(2**16,-step_val,-step_val)] # dimming
 
while True: # loop indefinitely
    # looping through red, blue, green breathing
    for pwm in pwms: 
           for ii in range_0+range_1:
               pwm.duty_u16(ii) # set duty cycle out of 16-bits
               time.sleep(0.001) # sleep 1ms between pwm change
    # white pixel breathing (all three LEDs)
    for ii in range_0+range_1:
        for pwm in pwms:
            pwm.duty_u16(ii) # set duty cycle
        time.sleep(0.001) # wait 1ms