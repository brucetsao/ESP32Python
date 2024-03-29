from machine import Pin, PWM
from time import sleep
#class buzzor:
    
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
        BuzzerObj = PWM(Pin(self.__pin))

    def __init__(self,setpin):
        self.__pin = setpin
        BuzzerObj = PWM(Pin(self.__pin))
    def buzzer(self,frequency,sound_duration,silence_duration):

        # Set duty cycle to a positive value to emit sound from buzzer
        BuzzerObj.duty_u16(int(65536*0.1))
        # Set frequency
        BuzzerObj.freq(frequency)
        # wait for sound duration
        sleep(sound_duration)
        # Set duty cycle to zero to stop sound
        BuzzerObj.duty_u16(int(65536*0))
        # Wait for sound interrumption, if needed 
        sleep(silence_duration)

    def playsong(self,song):
        for x in song:
            self.buzzer(x[0],x[1],x[2])
        BuzzerObj.deinit()    
        #Deactivates the buzzer    
    #set translation table from note to frequency
