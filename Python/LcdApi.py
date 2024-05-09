# 引入 MicroPython 的時間相關模組
import time  # 用於延遲和計時

# 定義 LcdApi 類，實現與 HD44780 相容的字符 LCD 進行通訊的 API
class LcdApi:
    """實現與 HD44780 相容的字符 LCD 進行通訊的 API。
    這個類僅知道要向 LCD 發送哪些命令，而不關心如何將它們發送到 LCD。
    期望衍生類別實現 hal_xxx 函數。
    """

    # 定義 HD44780 LCD 控制器的指令集
    LCD_CLR = 0x01  # 清除顯示
    LCD_HOME = 0x02  # 返回起始位置
    
    LCD_ENTRY_MODE = 0x04  # 設定輸入模式
    LCD_ENTRY_INC = 0x02  # 增量模式
    LCD_ENTRY_SHIFT = 0x01  # 移動模式
    
    LCD_ON_CTRL = 0x08  # LCD 控制指令
    LCD_ON_DISPLAY = 0x04  # 顯示
    LCD_ON_CURSOR = 0x02  # 游標
    LCD_ON_BLINK = 0x01  # 游標閃爍
    
    LCD_MOVE = 0x10  # 移動指令
    LCD_MOVE_DISP = 0x08  # 移動顯示 (0 表示移動游標)
    LCD_MOVE_RIGHT = 0x04  # 向右移動 (0 表示向左)
    
    LCD_FUNCTION = 0x20  # 功能設置
    LCD_FUNCTION_8BIT = 0x10  # 8 位模式 (0 表示 4 位模式)
    LCD_FUNCTION_2LINES = 0x08  # 兩行模式 (0 表示一行模式)
    LCD_FUNCTION_10DOTS = 0x04  # 10 點陣字體 (0 表示 7 點陣)
    LCD_FUNCTION_RESET = 0x30  # 初始化指令
    
    LCD_CGRAM = 0x40  # 設定 CGRAM 地址
    LCD_DDRAM = 0x80  # 設定 DDRAM 地址
    
    LCD_RS_CMD = 0  # 指令寄存器選擇
    LCD_RS_DATA = 1  # 數據寄存器選擇
    
    LCD_RW_WRITE = 0  # 寫入模式
    LCD_RW_READ = 1  # 讀取模式

    # 初始化 LcdApi 類
    def __init__(self, num_lines, num_columns):
        self.num_lines = min(num_lines, 4)  # 最大支援 4 行
        self.num_columns = min(num_columns, 40)  # 最大支援 40 列
        self.cursor_x = 0  # 游標的 x 位置
        self.cursor_y = 0  # 游標的 y 位置
        self.backlight = True  # 背光狀態
        self.display_off()  # 關閉顯示
        self.backlight_on()  # 開啟背光
        self.clear()  # 清除顯示
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)  # 設定輸入模式
        self.hide_cursor()  # 隱藏游標
        self.display_on()  # 開啟顯示

    # 清除 LCD 顯示並將游標移至左上角
    def clear(self):
        self.hal_write_command(self.LCD_CLR)  # 清除顯示
        self.hal_write_command(self.LCD_HOME)  # 返回起始位置
        self.cursor_x = 0  # 重置游標 x 位置
        self.cursor_y = 0  # 重置游標 y 位置

    # 讓游標可見
    def show_cursor(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR)  # 顯示游標

    # 隱藏游標
    def hide_cursor(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)  # 隱藏游標

    # 開啟游標閃爍
    def blink_cursor_on(self):
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR | self.LCD_ON_BLINK
        )

    # 關閉游標閃爍
    def blink_cursor_off(self):
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR
        )

    # 開啟 LCD 顯示
    def display_on(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)  # 開啟顯示

    # 關閉 LCD 顯示
    def display_off(self):
        self.hal_write_command(self.LCD_ON_CTRL)  # 關閉顯示

    # 開啟背光
    def backlight_on(self):
        self.backlight = True  # 更新背光狀態
        self.hal_backlight_on()  # 開啟背光

    # 關閉背光
    def backlight_off(self):
        self.backlight = False  # 更新背光狀態
        self.hal_backlight_off()  # 關閉背光

    # 移動游標到指定位置
    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x  # 設定游標 x 位置
        self.cursor_y = cursor_y  # 設定游標 y 位置
        addr = cursor_x & 0x3f  # 計算地址
        if cursor_y & 1:
            addr += 0x40  # 行 1 和 3 加上 0x40
        if cursor_y & 2:
            addr += 0x14  # 行 2 和 3 加上 0x14
        self.hal_write_command(self.LCD_DDRAM | addr)  # 發送地址指令

    # 在當前游標位置寫入字符並將游標前移
    def putchar(self, char):
        if char != '\n':
            self.hal_write_data(ord(char))  # 寫入字符
            self.cursor_x += 1  # 游標前移
        if self.cursor_x >= self.num_columns or char == '\n':
            self.cursor_x = 0  # 重置游標 x 位置
            self.cursor_y += 1  # 游標 y 位置增加
            if self.cursor_y >= self.num_lines:
                self.cursor_y = 0  # 重置游標 y 位置
            self.move_to(self.cursor_x, self.cursor_y)  # 移動游標

    # 在當前游標位置寫入字符串
    def putstr(self, string):
        for char in string:  # 將字符串中的字符逐一寫入
            self.putchar(char)

    # 定義自定義字符
    def custom_char(self, location, charmap):
        location &= 0x7  # 確定位置
        self.hal_write_command(self.LCD_CGRAM | (location << 3))  # 設定 CGRAM 地址
        time.sleep_us(40)  # 等待 40 微秒
        for i in range 8:
            self.hal_write_data(charmap[i])  # 寫入字符映射
            time.sleep_us(40)  # 等待 40 微秒
        self.move_to(self.cursor_x, self.cursor_y)  # 移動游標

    # HAL 層控制背光
    def hal_backlight_on(self):
        """開啟背光，供 HAL 層使用。"""
        pass  # 預設未實現

    def hal_backlight_off(self):
        """關閉背光，供 HAL 層使用。"""
        pass  # 預設未實現

    # HAL 層寫入指令
    def hal_write_command(self, cmd):
        """寫入指令到 LCD，預期 HAL 層實現。"""
        raise NotImplementedError  # 預設未實現

    # HAL 層寫入資料
    def hal_write_data(self, data):
        """寫入資料到 LCD，預期 HAL 層實現。"""
        raise NotImplementedError  # 預設未實現
