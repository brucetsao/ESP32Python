#Pico/W Breadboard擴充板揚聲器測試程式(beepsong.py)
from machine import Pin, PWM	#腳位套件
from time import sleep	#時間 套件

buzzerPIN=4	#外接揚聲器的腳位
BuzzerObj = PWM(Pin(buzzerPIN))	#產生PWM物件

#以下為音符之tone的頻率
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
#以上為音符之tone的頻率

#以下為範例歌曲之歌曲內容
songlist=[[mi5,0.1,0.1],[red5,0.1,0.1],[mi5,0.1,0.1],
      [red5,0.1,0.1],[mi5,0.1,0.1],[si5,0.1,0.1],
      [re5,0.1,0.1],[do5,0.1,0.1],[la5,0.5,0.1],
      [do5,0.1,0.1],[mi5,0.1,0.1],[la5,0.1,0.1],
      [si5,0.5,0.1],[mi5,0.1,0.1],[sold5,0.1,0.1],
      [si5,0.1,0.1],[do5,0.5,0.1],[mi5,0.1,0.1],
      [red5,0.1,0.1],[mi5,0.1,0.1],[red5,0.1,0.1],
      [mi5,0.1,0.1],[si5,0.1,0.1],[re5,0.1,0.1],
      [do5,0.1,0.1],[la5,0.5,0.1],[do5,0.1,0.1],
      [mi5,0.1,0.1],[la5,0.1,0.1],[si5,0.5,0.1],
      [mi5,0.1,0.1],[do5,0.1,0.1],[si5,0.1,0.1],
      [la5,0.5,0.1],[si5,0.1,0.1],[do5,0.1,0.1],
      [re5,0.1,0.1],[mi5,0.5,0.1],[sol5,0.1,0.1],
      [fa5,0.1,0.1],[mi5,0.1,0.1],[re5,0.5,0.1],
      [fa5,0.1,0.1],[mi5,0.1,0.1],[re5,0.1,0.1],
      [do5,0.5,0.1],[mi5,0.1,0.1],[re5,0.1,0.1],
      [do5,0.1,0.1],[si5,0.5,0.1],[mi5,0.1,0.1],
      [red5,0.1,0.1],[mi5,0.1,0.1],[red5,0.1,0.1],
      [mi5,0.1,0.1],[si5,0.1,0.1],[re5,0.1,0.1],
      [do5,0.1,0.1],[la5,0.5,0.1],[do5,0.1,0.1],
      [mi5,0.1,0.1],[la5,0.1,0.1],[si5,0.5,0.1],
      [mi5,0.1,0.1],[do5,0.1,0.1],[si5,0.1,0.1],
      [la5,0.5,0.1]]


#產生tone的自訂函式
def buzzer(buzzerPinObject,frequency,sound_duration,silence_duration):

    # Set duty cycle to a positive value to emit sound from buzzer
    #設定pwm的duty
    buzzerPinObject.duty_u16(int(65536*0.1))
    # Set frequency
    #設定pwm的頻率
    buzzerPinObject.freq(frequency)
    # wait for sound duration
    #設定等待發生的時間
    sleep(sound_duration)
    # Set duty cycle to zero to stop sound
    #設定pwm的duty
    buzzerPinObject.duty_u16(int(65536*0))
    # Wait for sound interrumption, if needed
    #設定等待發生的時間
    sleep(silence_duration)

#定義傳入歌曲陣列，發出一首歌
def playsong(beep,song):
    for x in song:	#讀出一首個每一個音符
        buzzer(beep,x[0],x[1],x[2])	#發出音樂
    beep.deinit()    #停止音樂
    #Deactivates the buzzer    
#set translation table from note to frequency

#彈一首歌
playsong(BuzzerObj,songlist)