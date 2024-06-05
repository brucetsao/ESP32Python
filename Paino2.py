# 引入 MicroPython 中的 Pin、PWM 和時間相關模組
from machine import Pin, PWM  # 用於控制 GPIO 和 PWM
from time import sleep  # 用於延遲操作

# 定義 Paino 類，用於控制蜂鳴器
class Paino:
    __pin = 7  # 私有變數，表示蜂鳴器的預設引腳

    # 屬性存取器，用於取得 pin 的值
    @property
    def pin(self):
        return self.__pin  # 返回私有變數 __pin

    # 屬性存取器，用於設置 pin 的值
    @pin.setter
    def pin(self, nn):
        self.__pin = nn  # 設定新的引腳號碼
        BuzzerObj = PWM(Pin(self.__pin))  # 使用新的引腳初始化 PWM

    # 初始化 Paino 類，設置蜂鳴器的引腳和 PWM
    def __init__(self, setpin):
        self.__pin = setpin  # 設定蜂鳴器的引腳
        BuzzerObj = PWM(Pin(self.__pin))  # 初始化 PWM

    # 控制蜂鳴器發出聲音
    def buzzer(self, frequency, sound_duration, silence_duration):
        # 設定占空比為正值以發出聲音
        BuzzerObj.duty_u16(int(65536 * 0.1))  # 設定占空比
        # 設定頻率
        BuzzerObj.freq(frequency)  # 設定頻率
        # 等待指定的聲音持續時間
        sleep(sound_duration)  # 等待聲音持續時間
        # 設定占空比為零以停止聲音
        BuzzerObj.duty_u16(int(65536 * 0))  # 停止蜂鳴器
        # 如果需要，等待靜音時間
        sleep(silence_duration)  # 等待靜音時間

    # 播放一首歌
    def playsong(self, song):
        for x in song:  # 對於歌曲中的每個音符
            self.buzzer(x[0], x[1], x[2])  # 播放音符
        BuzzerObj.deinit()  # 停用蜂鳴器

    # 設定音符到頻率的轉換表
