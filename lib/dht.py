# 這段 MicroPython 程式碼為 DHT11 和 DHT22 
# 感測器提供了驅動程式，
# 以在 ESP8266 等微控制器上讀取溫度和濕度數據。
# 這個程式碼為 MicroPython 提供了 DHT11 和 DHT22 感測器的支援，
# 可以用來讀取溫度和濕度數據。
# 它包含了基類 DHTBase，
# 以及繼承自它的 DHT11 和 DHT22 類。基類負責讀取感測器數據並進行校驗，
# 而子類實現了獲取溫度和濕度的方法。


# 匯入必要的模組
import sys  # 提供系統相關功能
import machine  # MicroPython 的機器相關功能

# 根據不同平台匯入 `dht_readinto` 函數
if hasattr(machine, "dht_readinto"):  # 如果 `machine` 模組具有 `dht_readinto`
    from machine import dht_readinto  # 從 `machine` 匯入 `dht_readinto`
elif sys.platform.startswith("esp"):  # 如果平台是 ESP8266 或 ESP32
    from esp import dht_readinto  # 從 `esp` 匯入 `dht_readinto`
elif sys.platform == "pyboard":  # 如果平台是 PyBoard
    from pyb import dht_readinto  # 從 `pyb` 匯入 `dht_readinto`
else:
    # 如果是其他平台，嘗試從相應的平台模組匯入
    dht_readinto = __import__(sys.platform).dht_readinto

del machine  # 刪除 `machine`，以釋放記憶體

# 定義 DHT 基類，提供基礎功能
class DHTBase:
    def __init__(self, pin):
        self.pin = pin  # 指定感測器的 GPIO 腳位
        self.buf = bytearray(5)  # 用於儲存讀取的資料

    def measure(self):
        buf = self.buf
        dht_readinto(self.pin, buf)  # 將感測器數據讀入 `buf`
        # 校驗數據，以確保資料的正確性
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xFF != buf[4]:
            raise Exception("checksum error")  # 如果校驗失敗，拋出異常

# 定義 DHT11 類，繼承自 DHT 基類
class DHT11(DHTBase):
    def humidity(self):
        return self.buf[0]  # 濕度存儲在第一個字節

    def temperature(self):
        return self.buf[2]  # 溫度存儲在第三個字節

# 定義 DHT22 類，繼承自 DHT 基類
class DHT22(DHTBase):
    def humidity(self):
        # 濕度為兩個字節合併後的值，並乘以 0.1 以取得實際濕度
        return (self.buf[0] << 8 | self.buf[1]) * 0.1

    def temperature(self):
        # 溫度同樣為兩個字節合併後的值，並根據最高位確定正負號
        t = ((self.buf[2] & 0x7F) << 8 | self.buf[3]) * 0.1
        if self.buf[2] & 0x80:  # 如果最高位為 1，代表負數
            t = -t
        return t

__version__ = '0.1.0'  # 版本號
