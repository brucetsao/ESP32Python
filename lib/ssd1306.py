# 這段 MicroPython 程式碼定義了 SSD1306 OLED 顯示驅動，
# 支援 I2C 和 SPI 通訊介面。
# 這段 MicroPython 程式碼為 SSD1306 OLED 顯示驅動提供了完整的功能，
# 包括初始化、開啟/關閉顯示器、設定對比度、反轉顯示、旋轉方向，以及顯示內容等。
# 該程式碼支援 I2C 和 SPI 兩種通訊介面，
# 並可用於與 MicroPython 裝置進行 OLED 顯示器的交互。


# 匯入必要的模組
from micropython import const  # 定義常數
import framebuf  # 框架緩衝區，用於繪圖操作

# 定義 SSD1306 OLED 的註冊器
SET_CONTRAST = const(0x81)  # 設定對比度
SET_ENTIRE_ON = const(0xA4)  # 設定整體開啟
SET_NORM_INV = const(0xA6)  # 設定顯示模式（正常/反轉）
SET_DISP = const(0xAE)  # 設定顯示開關
SET_MEM_ADDR = const(0x20)  # 設定記憶體地址模式
SET_COL_ADDR = const(0x21)  # 設定列地址
SET_PAGE_ADDR = const(0x22)  # 設定頁地址
SET_DISP_START_LINE = const(0x40)  # 設定顯示起始行
SET_SEG_REMAP = const(0xA0)  # 設定列重新映射
SET_MUX_RATIO = const(0xA8)  # 設定多工比例
SET_IREF_SELECT = const(0xAD)  # 設定內部參考電流選擇
SET_COM_OUT_DIR = const(0xC0)  # 設定 COM 輸出方向
SET_DISP_OFFSET = const(0xD3)  # 設定顯示偏移
SET_COM_PIN_CFG = const(0xDA)  # 設定 COM 針腳配置
SET_DISP_CLK_DIV = const(0xD5)  # 設定顯示時鐘分頻
SET_PRECHARGE = const(0xD9)  # 設定預充電時間
SET_VCOM_DESEL = const(0xDB)  # 設定 VCOM 停止電平
SET_CHARGE_PUMP = const(0x8D)  # 設定充電泵

# SSD1306 顯示類，繼承自 framebuf.FrameBuffer
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        """初始化 SSD1306 顯示器
        Args:
            width (int): 顯示器的寬度
            height (int): 顯示器的高度
            external_vcc (bool): 使用外部電壓
        """
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8  # 確定頁數
        self.buffer = bytearray(self.pages * self.width)  # 初始化緩衝區
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()  # 初始化顯示器

    def init_display(self):
        """初始化 SSD1306 顯示器的設定"""
        for cmd in (
            SET_DISP,  # 關閉顯示
            SET_MEM_ADDR,
            0x00,  # 設定記憶體地址模式為水平
            SET_DISP_START_LINE,
            SET_SEG_REMAP | 0x01,  # 設定列重新映射
            SET_MUX_RATIO,
            self.height - 1,  # 設定多工比例
            SET_COM_OUT_DIR | 0x08,  # 設定 COM 輸出方向
            SET_DISP_OFFSET,
            0x00,  # 顯示偏移
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            SET_DISP_CLK_DIV,
            0x80,  # 設定時鐘分頻
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,  # 預充電時間
            SET_VCOM_DESEL,
            0x30,  # 設定 VCOM 停止電平
            SET_CONTRAST,
            0xFF,  # 設定對比度
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,  # 開啟顯示
        ): 
            self.write_cmd(cmd)  # 發送指令到顯示器
        self.fill(0)  # 清除顯示內容
        self.show()  # 顯示內容

    def poweroff(self):
        """關閉顯示器"""
        self.write_cmd(SET_DISP)

    def poweron(self):
        """開啟顯示器"""
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        """設定顯示器對比度"""
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        """設定顯示器反轉模式"""
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def rotate(self, rotate):
        """設定顯示器旋轉方向"""
        self.write_cmd(SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(SET_SEG_REMAP | (rotate & 1))

    def show(self):
        """顯示緩衝區內容"""
        x0 = 0
        x1 = self.width - 1
        if self.width != 128:
            # 將列地址居中
            col_offset = (128 - self.width) // 2
            x0 += col_offset
            x1 += col_offset
        self.write_cmd(SET_COL_ADDR)  # 設定列地址
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)  # 設定頁地址
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)  # 將緩衝區內容發送到顯示器

# I2C 介面類
class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        """初始化 I2C 介面的 SSD1306 顯示器"""
        self.i2c = i2c  # I2C 物件
        self.addr = addr  # I2C 地址
        self.temp = bytearray(2)  # 暫存資料
        self.write_list = [b"\x40", None]  # 用於寫入的列表
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        """發送命令到 SSD1306 顯示器"""
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        """發送資料到 SSD1306 顯示器"""
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)

# SPI 介面類
class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        """初始化 SPI 介面的 SSD1306 顯示器"""
        self.rate = 10 * 1024 * 1024  # 設定 SPI 資料傳輸速率
        dc.init(dc.OUT, value=0)  # 初始化 DC 腳位
        res.init(res.OUT, value=0)  # 初始化 RESET 腳位
        cs.init(cs.OUT, value=1)  # 初始化 CS 腳位
        self.spi = spi  # SPI 物件
        self.dc = dc  # 資料/命令選擇
        self.res = res  # 重置
        self.cs = cs  # 選擇
        import time  # 時間相關模組

        self.res(1)  # 重置
        time.sleep_ms(1)  # 等待 1 毫秒
        self.res(0)  # 設定重置
        time.sleep_ms(10)  # 等待 10 毫秒
        self.res(1)  # 解除重置
        super().__init__(width, height, external_vcc)  # 初始化顯示器

    def write_cmd(self, cmd):
        """發送命令到 SSD1306 顯示器"""
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)  # 初始化 SPI
        self.cs(1)  # 選擇裝置
        self.dc(0)  # 設定為命令模式
        self.cs(0)  # 向下傳送
        self.spi.write(bytearray([cmd]))  # 發送命令
        self.cs(1)  # 停止

    def write_data(self, buf):
        """發送資料到 SSD1306 顯示器"""
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)  # 初始化 SPI
        self.cs(1)  # 選擇裝置
        self.dc(1)  # 設定為資料模式
        self.cs(0)  # 向下傳送
        self.spi.write(buf)  # 發送資料
        self.cs(1)  # 停止

__version__ = '0.1.0'  # SSD1306 驅動的版本號
