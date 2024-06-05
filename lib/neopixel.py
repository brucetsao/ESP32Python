# 這段 MicroPython 程式碼定義了一個名為 NeoPixel 的類，
# 用於控制 WS2812 或類似的 NeoPixel LED 燈條。
# 這段程式碼定義了控制 NeoPixel LED 的基礎類，
# 其中包括初始化、
# 設定 LED 顏色、填充顏色、以及將資料寫入 LED 的功能。
# 該程式碼可以用於控制多種 NeoPixel 燈條，並適應不同的硬體設置。

# 匯入用於控制硬體和進行比特流操作的模組
from machine import bitstream

# NeoPixel 類定義
class NeoPixel:
    # G R B W
    ORDER = (1, 0, 2, 3)  # LED 色序：綠、紅、藍、白

    def __init__(self, pin, n, bpp=3, timing=1):
        """初始化 NeoPixel 類
        Args:
            pin (Pin): 接到 NeoPixel 的腳位
            n (int): NeoPixel LED 的數量
            bpp (int): 每個 LED 的位元組數（預設 3，RGB）
            timing (int/tuple): 定時參數，1 為 800kHz，0 為 400kHz，或自訂定時參數
        """
        self.pin = pin  # 儲存腳位
        self.n = n  # LED 數量
        self.bpp = bpp  # 每個 LED 的位元組數
        # 初始化緩衝區，長度為 LED 數量乘以每個 LED 的位元組數
        self.buf = bytearray(n * bpp)
        self.pin.init(pin.OUT)  # 初始化腳位為輸出
        # 根據傳入的 timing 引數設定定時參數
        self.timing = (
            ((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
            if isinstance(timing, int)  # 檢查是否為整數
            else timing  # 否則使用自訂定時參數
        )

    def __len__(self):
        """取得 NeoPixel LED 的數量"""
        return self.n

    def __setitem__(self, i, v):
        """設定特定位置的 LED 顏色
        Args:
            i (int): LED 的索引位置
            v (tuple): RGB 顏色值
        """
        offset = i * self.bpp  # 計算在緩衝區的偏移
        for i in range(self.bpp):  # 根據 bpp 將顏色值寫入緩衝區
            self.buf[offset + self.ORDER[i]] = v[i]

    def __getitem__(self, i):
        """取得特定位置的 LED 顏色
        Args:
            i (int): LED 的索引位置
        Returns:
            tuple: RGB 顏色值
        """
        offset = i * self.bpp  # 計算在緩衝區的偏移
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    def fill(self, v):
        """填充所有 LED 為相同的顏色
        Args:
            v (tuple): RGB 顏色值
        """
        b = self.buf  # 緩衝區
        l = len(self.buf)  # 緩衝區長度
        bpp = self.bpp  # 每個 LED 的位元組數
        for i in range(bpp):
            c = v[i]  # 顏色值
            j = self.ORDER[i]  # 色序中的索引
            while j < l:  # 填充整個緩衝區
                b[j] = c
                j += bpp

    def write(self):
        """將緩衝區的內容寫入到 LED"""
        bitstream(self.pin, 0, self.timing, self.buf)  # 使用比特流將數據寫入 LED

__version__ = '0.1.0'  # NeoPixel 模組的版本號
