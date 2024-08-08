# 這段 MicroPython 程式碼定義了一個 HTU21D 溫濕度感測器的類別，
# 提供了測量溫度和濕度的功能。
# 這個程式碼使用 I2C 通訊與 HTU21D 感測器交互，
# 以獲取溫度和濕度數據。
# 它包括數據的 CRC 校驗，
# 以確保數據的完整性，
# 並提供相關方法來進行測量和獲取溫度、濕度值


from machine import I2C, Pin  # 匯入 MicroPython 的 I2C 和 Pin 套件
import time  # 匯入時間相關功能

class HTU21D(object):
    # 常數定義
    ADDRESS = 0x40  # HTU21D 感測器的 I2C 地址
    ISSUE_TEMP_ADDRESS = 0xE3  # 溫度測量指令地址
    ISSUE_HU_ADDRESS = 0xE5  # 濕度測量指令地址

    def __init__(self, scl, sda):
        """初始化 HTU21D 類別
        參數:
            scl (int): 連接到 I2C 的 SCL 腳位編號
            sda (int): 連接到 I2C 的 SDA 腳位編號
        """
        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)  # 初始化 I2C 通訊

    def _crc_check(self, value):
        """檢查數據的 CRC (循環冗餘校驗)
        備註:
            從 sparkfun/HTU21D_Breakout 的 GitHub 借鑑
        參數:
            value (bytearray): 要檢查的數據
        返回:
            True 表示有效，False 表示無效
        """
        # 初始化 CRC 計算
        remainder = ((value[0] << 8) + value[1]) << 8  # 計算餘數
        remainder |= value[2]  # 合併剩餘部分
        divsor = 0x988000  # CRC 多項式

        # 進行 16 次循環
        for i in range(0, 16):
            if remainder & (1 << (23 - i)):  # 如果特定位被設置
                remainder ^= divsor  # 與多項式進行 XOR
            divsor >>= 1  # 將多項式右移

        # 如果剩餘為零，則校驗通過
        return remainder == 0

    def _issue_measurement(self, write_address):
        """發出測量指令
        參數:
            write_address (int): 寫入的地址
        返回:
            測量到的原始數據
        """
        # 啟動 I2C 通訊
        self.i2c.start()  
        self.i2c.writeto_mem(int(self.ADDRESS), int(write_address), '')  # 發送指令
        self.i2c.stop()  # 停止 I2C 通訊
        time.sleep_ms(50)  # 等待 50 毫秒
        data = bytearray(3)  # 初始化數據
        self.i2c.readfrom_into(self.ADDRESS, data)  # 讀取感測器的數據
        # 檢查數據的 CRC 是否有效
        if not self._crc_check(data):
            raise ValueError()  # 如果無效，則引發錯誤
        raw = (data[0] << 8) + data[1]  # 合併數據
        raw &= 0xFFFC  # 清除無用的位
        return raw

    @property
    def temperature(self):
        """計算溫度"""
        raw = self._issue_measurement(self.ISSUE_TEMP_ADDRESS)  # 發送溫度測量指令
        # 計算溫度值
        return -46.85 + (175.72 * raw / 65536)

    @property
    def humidity(self):
        """計算濕度"""
        raw = self._issue_measurement(self.ISSUE_HU_ADDRESS)  # 發送濕度測量指令
        # 計算濕度值
        return -6 + (125.0 * raw / 65536)

    def test(self):
        """測試函數，打印訊息"""
        print("Test Self")  # 輸出訊息
