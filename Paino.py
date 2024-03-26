from machine import Pin, PWM
from time import sleep
class Paino:
    __pin=7
    #BuzzerObj
        #-------------------------------
    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, nn):
        self.__pin = nn
        self.BuzzerObj = PWM(Pin(self.__pin))

    def __init__(self,setpin):
        self.__pin = setpin
        self.BuzzerObj = PWM(Pin(self.__pin))
    def buzzer(self,frequency,sound_duration,silence_duration):

        # Set duty cycle to a positive value to emit sound from buzzer
        self.BuzzerObj.duty_u16(int(65536*0.1))
        # Set frequency
        self.BuzzerObj.freq(frequency)
        # wait for sound duration
        sleep(sound_duration)
        # Set duty cycle to zero to stop sound
        self.BuzzerObj.duty_u16(int(65536*0))
        # Wait for sound interrumption, if needed 
        sleep(silence_duration)

    def playsong(self,song):
        for x in song:
            self.buzzer(x[0],x[1],x[2])
        self.BuzzerObj.deinit()    
        #Deactivates the buzzer    
    #set translation table from note to frequency
    def beep(self):
        self.buzzer(554,0.5,1)
