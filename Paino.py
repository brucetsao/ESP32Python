# 引入 MicroPython 的 Pin、PWM 和時間相關模組
from machine import Pin, PWM  # 用於控制 GPIO 和 PWM
from time import sleep  # 用於延遲操作

# 定義 Paino 類，用於控制蜂鳴器
class Paino:
    __pin = 7  # 私有變數，表示蜂鳴器的預設引腳

    # 取得 pin 的屬性
    @property
    def pin(self):
        return self.__pin  # 返回私有變數 __pin

    # 設定 pin 的屬性
    @pin.setter
    def pin(self, nn):
        self.__pin = nn  # 更新私有變數 __pin
        self.BuzzerObj = PWM(Pin(self.__pin))  # 更新蜂鳴器的 PWM 物件

    # 初始化 Paino 類，設置引腳並初始化 PWM
    def __init__(self, setpin):
        self.__pin = setpin  # 設定引腳
        self.BuzzerObj = PWM(Pin(self.__pin))  # 初始化 PWM 物件

    # 控制蜂鳴器發出聲音
    def buzzer(self, frequency, sound_duration, silence_duration):
        # 設定占空比，讓蜂鳴器發出聲音
        self.BuzzerObj.duty_u16(int(65536 * 0.1))  # 設定占空比
        # 設定頻率
        self.BuzzerObj.freq(frequency)  # 設定頻率
        # 等待聲音持續時間
        sleep(sound_duration)  # 等待指定的聲音持續時間
        # 設定占空比為零，停止聲音
        self.BuzzerObj.duty_u16(int(65536 * 0))  # 停止蜂鳴器
        # 等待靜音時間
        sleep(silence_duration)  # 等待指定的靜音時間

    # 播放一首歌
    def playsong(self, song):
        for x in song:  # 對於歌曲中的每個音符
            self.buzzer(x[0], x[1], x[2])  # 播放音符
        self.BuzzerObj.deinit()  # 停用蜂鳴器
    
    # 發出一個聲音
    def beep(self):
        self.buzzer(554, 0.5, 1)  # 發出指定頻率和持續時間的聲音
