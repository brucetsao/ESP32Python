# 引入必要的 MicroPython 模組
from lcd_api import LcdApi  # 用於控制 LCD 顯示器的 API
from machine import I2C  # 用於 I2C 通訊
from time import sleep_ms  # 用於毫秒級別的睡眠

# PCF8574 的預設 I2C 地址，可以透過跳線選擇：0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27  # 預設地址為 0x27

# 定義 PCF8574 與 LCD 連接的各種線路的掩碼和移位
MASK_RS = 0x01  # 寄存器選擇
MASK_RW = 0x02  # 讀寫選擇
MASK_E = 0x04  # 啟用掩碼
SHIFT_BACKLIGHT = 3  # 背光的移位
SHIFT_DATA = 4  # 資料的移位

# 定義 I2cLcd 類別，用於通過 PCF8574 控制 I2C 介面的 LCD 顯示器
class I2cLcd(LcdApi):
    """實現通過 PCF8574 連接 I2C 的 HD44780 字符 LCD。"""

    # 初始化 I2cLcd 類別
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c  # I2C 通訊
        self.i2c_addr = i2c_addr  # I2C 地址
        self.i2c.writeto(self.i2c_addr, bytearray([0]))  # 初始化 I2C 線路
        sleep_ms(20)  # 等待 LCD 開機
        # 發送三次重置命令
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        sleep_ms(5)  # 等待至少 4.1 毫秒
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        sleep_ms(1)  # 短暫等待
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        sleep_ms(1)  # 短暫等待
        # 將 LCD 設定為 4 位模式
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        sleep_ms(1)  # 短暫等待
        # 初始化 LCD
        LcdApi.__init__(self, num_lines, num_columns)  # 初始化 LCD 顯示
        # 設定 LCD 功能和行數
        cmd = self.LCD_FUNCTION  # LCD 功能命令
        if num_lines > 1:  # 如果有多於一行
            cmd |= self.LCD_FUNCTION_2LINES  # 設定為兩行模式
        self.hal_write_command(cmd)  # 發送 LCD 功能命令

    # 在初始化期間寫入位元
    def hal_write_init_nibble(self, nibble):
        """將初始化的位元寫入 LCD。"""
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA  # 移位和設置資料
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))  # 發送資料並啟用
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))  # 關閉啟用

    # 背光控制：開啟背光
    def hal_backlight_on(self):
        """讓 HAL 層啟用背光。"""
        self.i2c.writeto(self.i2c_addr, bytearray([1 << SHIFT_BACKLIGHT]))  # 打開背光

    # 背光控制：關閉背光
    def hal_backlight_off(self):
        """讓 HAL 層關閉背光。"""
        self.i2c.writeto(self.i2c_addr, bytearray([0]))  # 關閉背光

    # 發送指令到 LCD
    def hal_write_command(self, cmd):
        """將指令寫入 LCD。"""
        # 將資料與啟用線結合並發送
        byte = ((self.backlight << SHIFT_BACKLIGHT) | (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))  # 發送資料並啟用
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))  # 關閉啟用
        # 設置資料和背光
        byte = ((self.backlight << SHIFT_BACKLIGHT) | ((cmd & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))  # 發送資料並啟用
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))  # 關閉啟用
        # 如果指令是重置或清除，需要更長的延遲
        if cmd <= 3:
            sleep_ms(5)  # 等待 5 毫秒

    # 發送資料到 LCD
    def hal_write_data(self, data):
        """將資料寫入 LCD。"""
        byte = (MASK_RS | (self.backlight << SHIFT_BACKLIGHT) | (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))  # 發送資料並啟用
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))  # 關閉啟用
        byte = (MASK_RS | (self.backlight << SHIFT_BACKLIGHT) | ((data & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))  # 發送資料並啟用
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))  # 關閉啟用
