# 引入 machine 模組中的 I2C 類別，允許 I2C 通訊
from machine import I2C

# 引入 time 模組，提供時間相關功能
import time

# BME280 的預設 I2C 地址
BME280_I2CADDR = 0x76  # 常用的 I2C 地址

# BME280 的操作模式
BME280_OSAMPLE_1 = 1
BME280_OSAMPLE_2 = 2
BME280_OSAMPLE_4 = 3
BME280_OSAMPLE_8 = 4
BME280_OSAMPLE_16 = 5

# BME280 的註冊地址
BME280_REGISTER_DIG_T1 = 0x88  # 溫度校準參數
BME280_REGISTER_DIG_T2 = 0x8A
BME280_REGISTER_DIG_T3 = 0x8C

BME280_REGISTER_DIG_P1 = 0x8E  # 壓力校準參數
BME280_REGISTER_DIG_P2 = 0x90
BME280_REGISTER_DIG_P3 = 0x92
BME280_REGISTER_DIG_P4 = 0x94
BME280_REGISTER_DIG_P5 = 0x96
BME280_REGISTER_DIG_P6 = 0x98
BME280_REGISTER_DIG_P7 = 0x9A
BME280_REGISTER_DIG_P8 = 0x9C
BME280_REGISTER_DIG_P9 = 0x9E

BME280_REGISTER_DIG_H1 = 0xA1  # 濕度校準參數
BME280_REGISTER_DIG_H2 = 0xE1
BME280_REGISTER_DIG_H3 = 0xE3
BME280_REGISTER_DIG_H4 = 0xE4
BME280_REGISTER_DIG_H5 = 0xE5
BME280_REGISTER_DIG_H6 = 0xE6
BME280_REGISTER_DIG_H7 = 0xE7

BME280_REGISTER_CHIPID = 0xD0  # BME280 的晶片 ID
BME280_REGISTER_VERSION = 0xD1  # 版本資訊
BME280_REGISTER_SOFTRESET = 0xE0  # 軟體重置註冊
BME280_REGISTER_CONTROL_HUM = 0xF2  # 濕度控制註冊
BME280_REGISTER_CONTROL = 0xF4  # 溫度與壓力控制註冊
BME280_REGISTER_CONFIG = 0xF5  # 配置註冊
BME280_REGISTER_PRESSURE_DATA = 0xF7  # 壓力數據註冊
BME280_REGISTER_TEMP_DATA = 0xFA  # 溫度數據註冊
BME280_REGISTER_HUMIDITY_DATA = 0xFD  # 濕度數據註冊

# 設定一個用於 I2C 通訊的基礎類別
class Device:
    """用於與 I2C 裝置通訊的類別，提供 8 位、16 位、以及 byte array 的讀寫功能。"""

    # 初始化 Device 類別，指定 I2C 地址和 I2C 介面物件
    def __init__(self, address, i2c):
        self._address = address
        self._i2c = i2c

    # 寫入 8 位元的值（不使用註冊）
    def writeRaw8(self, value):
        value = value & 0xFF  # 確保值在 8 位範圍內
        self._i2c.writeto(self._address, bytes([value]))  # 寫入到 I2C 地址

    # 寫入 8 位元的值到指定註冊
    def write8(self, register, value):
        b = bytearray(1)  # 建立一個 bytearray
        b[0] = value & 0xFF  # 設定為 8 位範圍內
        self._i2c.writeto_mem(self._address, register, b)  # 寫入到指定註冊

    # 寫入 16 位元的值到指定註冊
    def write16(self, register, value):
        value = value & 0xFFFF  # 確保值在 16 位範圍內
        b = bytearray(2)  # 建立一個 2 位的 bytearray
        b[0] = value & 0xFF  # 設定低位
        b[1] = (value >> 8) & 0xFF  # 設定高位
        self._i2c.writeto_mem(self._address, register, b)  # 寫入到指定註冊

    # 讀取 8 位元的值（不使用註冊）
    def readRaw8(self):
        return int.from_bytes(self._i2c.readfrom(self._address, 1), 'little')  # 讀取 1 byte 並轉為整數

    # 讀取指定註冊的無號 8 位元值
    def readU8(self, register):
        return int.from_bytes(
            self._i2c.readfrom_mem(self._address, register, 1), 'little')  # 讀取註冊的 1 byte 並轉為整數

    # 讀取指定註冊的有號 8 位元值
    def readS8(self, register):
        result = self.readU8(register)  # 讀取無號 8 位元
        if result > 127:  # 如果值大於 127，表示是負數
            result -= 256  # 將值轉換為負數
        return result

    # 讀取指定註冊的無號 16 位元值，允許指定大端或小端順序
    def readU16(self, register, little_endian=True):
        result = int.from_bytes(
            self._i2c.readfrom_mem(self._address, register, 2), 'little')  # 讀取 2 byte 並轉為整數
        if not little_endian:  # 如果是大端順序，則調整
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    # 讀取指定註冊的有號 16 位元值，允許指定大端或小端順序
    def readS16(self, register, little_endian=True):
        result = self.readU16(register, little_endian)  # 讀取無號 16 位元
        if result > 32767:  # 如果值大於 32767，表示是負數
            result -= 65536  # 將值轉換為負數
        return result

    # 讀取指定註冊的無號 16 位元值，小端順序
    def readU16LE(self, register):
        return self.readU16(register, little_endian=True)

    # 讀取指定註冊的無號 16 位元值，大端順序
    def readU16BE(self, register):
        return self.readU16(register, little_endian=False)

    # 讀取指定註冊的有號 16 位元值，小端順序
    def readS16LE(self, register):
        return self.readS16(register, little_endian=True)

    # 讀取指定註冊的有號 16 位元值，大端順序
    def readS16BE(self, register):
        return self.readS16(register, little_endian=False)
