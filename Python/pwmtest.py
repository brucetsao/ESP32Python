#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Blog: https://peppe8o.com
# Date: Oct 6th, 2021
# Version: 1.0

from machine import Pin, PWM
from time import sleep

buzzerPIN=7
BuzzerObj = PWM(Pin(buzzerPIN))

def buzzer(buzzerPinObject,frequency,sound_duration,silence_duration):

    # Set duty cycle to a positive value to emit sound from buzzer
    buzzerPinObject.duty_u16(int(65536*0.1))
    # Set frequency
    buzzerPinObject.freq(frequency)
    # wait for sound duration
    sleep(sound_duration)
    # Set duty cycle to zero to stop sound
    buzzerPinObject.duty_u16(int(65536*0))
    # Wait for sound interrumption, if needed 
    sleep(silence_duration)


#set translation table from note to frequency
do5=523
dod5=554
re5=587
red5=622
mi5=659
fa5=698
fad5=739
sol5=784
sold5=830
la5=880
lad5=932
si5=987


buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,red5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,red5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,re5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,la5,0.5,0.1)

buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,la5,0.1,0.1)
buzzer(BuzzerObj,si5,0.5,0.1)

buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,sold5,0.1,0.1)
buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,do5,0.5,0.1)

buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,red5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,red5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,re5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,la5,0.5,0.1)

buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,la5,0.1,0.1)
buzzer(BuzzerObj,si5,0.5,0.1)

buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,la5,0.5,0.1)

buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,re5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.5,0.1)

buzzer(BuzzerObj,sol5,0.1,0.1)
buzzer(BuzzerObj,fa5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,re5,0.5,0.1)

buzzer(BuzzerObj,fa5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,re5,0.1,0.1)
buzzer(BuzzerObj,do5,0.5,0.1)

buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,re5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,si5,0.5,0.1)

buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,red5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,red5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,re5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,la5,0.5,0.1)

buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,la5,0.1,0.1)
buzzer(BuzzerObj,si5,0.5,0.1)

buzzer(BuzzerObj,mi5,0.1,0.1)
buzzer(BuzzerObj,do5,0.1,0.1)
buzzer(BuzzerObj,si5,0.1,0.1)
buzzer(BuzzerObj,la5,0.5,0.1)

#Deactivates the buzzer
BuzzerObj.deinit()