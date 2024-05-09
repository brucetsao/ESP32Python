# 這段 MicroPython 程式碼定義了一個 HTU21D 類，
# 該類可以與 HTU21D 溫濕度感測器進行通信，
# 並提供溫度和濕度的讀取方法。
# 該類實現了 I2C 通訊、CRC 檢查、溫度和濕度測量等功能。
# 程式的主要功能和註解如下：
# 
#     初始化 I2C 通訊：I2C(scl=Pin(22), sda=Pin(21), freq=100_000) 以設定 SCL 和 SDA 的腳位號碼以及 I2C 通訊頻率。
#     HTU21D 類使用 I2C 通訊與 HTU21D 感測器交互。提供了測量溫度和濕度的方法，以及 CRC 檢查功能。
#     定義了 _crc_check 方法來檢查數據的有效性，_issue_measurement 方法發出測量指令並讀取結果。
#     使用 @property 裝飾器提供了獲取溫度和濕度的屬性方法。
#     最後，程式建立了一個 HTU21D 的實例，並讀取溫度和濕度，然後將其打印到控制台。
from machine import I2C, Pin  # 匯入I2C和Pin模組，用於I2C通訊和GPIO操作
import time  # 匯入time模組，用於延時

# HTU21D溫濕度感測器的類別
class HTU21D(object):
    # 設置HTU21D感測器的I2C地址和測量命令
    ADDRESS = 0x40  # I2C地址
    ISSUE_TEMP_ADDRESS = 0xE3  # 溫度測量命令
    ISSUE_HU_ADDRESS = 0xE5  # 濕度測量命令

    # 初始化HTU21D
    def __init__(self, scl, sda):
        """初始化HTU21D感測器
        Args:
            scl (int): I2C通訊中scl腳位的Pin編號
            sda (int): I2C通訊中sda腳位的Pin編號
        """
        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100_000)  # 初始化I2C，設定SCL和SDA的Pin編號

    # CRC檢查，檢查數據的有效性
    def _crc_check(self, value):
        """檢查CRC校驗碼的正確性
        Args:
            value (bytearray): 要檢查的數據
        Returns:
            True代表有效，False代表無效
        """
        remainder = ((value[0] << 8) + value[1]) << 8  # 將數據拼接成CRC校驗碼
        remainder |= value[2]
        divsor = 0x988000  # 進行CRC校驗的除數

        # 進行CRC校驗
        for i in range(0, 16):
            if remainder & (1 << (23 - i)):  # 檢查高位
                remainder ^= divsor  # 如果匹配，進行異或操作
            divsor >>= 1  # 右移除數

        return remainder == 0  # 如果剩餘值為0，代表校驗通過

    # 發出測量指令
    def _issue_measurement(self, write_address):
        """發出測量指令
        Args:
            write_address (int): 要寫入的I2C地址
        """
        self.i2c.start()  # 開始I2C通訊
        self.i2c.writeto_mem(self.ADDRESS, write_address, b'')  # 向指定地址發出命令
        self.i2c.stop()  # 結束I2C通訊
        time.sleep_ms(50)  # 等待一段時間，確保感測器完成測量
        data = bytearray(3)  # 準備三個字節的數據容器
        self.i2c.readfrom_into(self.ADDRESS, data)  # 讀取I2C數據
        if not self._crc_check(data):  # 檢查數據的CRC校驗
            raise ValueError("CRC校驗失敗")
        raw = (data[0] << 8) + data[1]  # 組合成一個16位元數值
        raw &= 0xFFFC  # 去除低位的狀態位
        return raw  # 返回原始數據

    # 獲取溫度
    @property
    def temperature(self):
        """計算溫度"""
        raw = self._issue_measurement(self.ISSUE_TEMP_ADDRESS)  # 發出溫度測量指令並獲取數據
        return -46.85 + (175.72 * raw / 65536)  # 使用原始數據計算溫度

    # 獲取濕度
    @property
    def humidity(self):
        """計算濕度"""
        raw = self._issue_measurement(self.ISSUE_HU_ADDRESS)  # 發出濕度測量指令並獲取數據
        return -6 + (125.0 * raw / 65536)  # 使用原始數據計算濕度

    # 測試方法
    def test(self):
        print("進入測試函數")

# 建立HTU21D的實例並測量溫度和濕度
lectura = HTU21D(22, 21)  # 使用SCL和SDA的腳位號碼建立HTU21D實例
hum = lectura.humidity  # 獲取濕度
temp = lectura.temperature  # 獲取溫度
print('濕度: ', hum)  # 輸出濕度
print('溫度: ', temp)  # 輸出溫度
