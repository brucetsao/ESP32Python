# 引入 ST7735 顯示器控制模組、系統字體、機器控制和時間操作
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time
import math  # 用於數學運算

# 初始化 SPI 通訊
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
# SPI(組別, 波特率, 極性, 相位, 時鐘腳位, MOSI腳位, MISO腳位)

# 初始化 TFT 顯示器
tft = TFT(spi, 14, 15, 13)  # TFT(通訊, DC 腳位, CS 腳位, RESET 腳位)
tft.initb2()  # 初始化 ST7735 顯示器
tft.rgb(True)  # 設定 RGB 模式

# 測試函式：繪製交叉線
def testlines(color):
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    # 繪製從左上到右下的線
    for x in range(0, tft.size()[0], 6):
        tft.line((0, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0, 0), (tft.size()[0] - 1, y), color)
    
    # 繪製從右上到左下的線
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, 0), (0, y), color)
    
    # 繪製從左下到右上的線
    for x in range(0, tft.size()[0], 6):
        tft.line((0, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0, tft.size()[1] - 1), (tft.size()[0] - 1, y), color)

    # 繪製從右下到左上的線
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (0, y), color)

# 測試函式：繪製水平和垂直線
def testfastlines(color1, color2):
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    # 繪製水平線
    for y in range(0, tft.size()[1], 5):
        tft.hline((0, y), tft.size()[0], color1)
    # 繪製垂直線
    for x in range(0, tft.size()[0], 5):
        tft.vline((x, 0), tft.size()[1], color2)

# 測試函式：繪製矩形
def testdrawrects(color):
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    for x in range(0, tft.size()[0], 6):
        tft.rect((tft.size()[0] // 2 - x // 2, tft.size()[1] // 2 - x / 2), (x, x), color)

# 測試函式：繪製填充矩形
def testfillrects(color1, color2):
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    for x in range(tft.size()[0], 0, -6):
        tft.fillrect((tft.size()[0] // 2 - x // 2, tft.size()[1] // 2 - x // 2), (x, x), color1)
        tft.rect((tft.size()[0] // 2 - x // 2, tft.size()[1] // 2 - x // 2), (x, x), color2)

# 測試函式：繪製填充圓形
def testfillcircles(radius, color):
    for x in range(radius, tft.size()[0], radius * 2):
        for y in range(radius, tft.size()[1], radius * 2):
            tft.fillcircle((x, y), radius, color)

# 測試函式：繪製圓形
def testdrawcircles(radius, color):
    for x in range(0, tft.size()[0] + radius, radius * 2):
        for y in range(0, tft.size()[1] + radius, radius * 2):
            tft.circle((x, y), radius, color)

# 測試函式：繪製三角形
def testtriangles():
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    color = 0xF800  # 設定顏色
    w = tft.size()[0] // 2
    x = tft.size()[1] - 1
    y = 0
    z = tft.size()[0]
    for t in range(0, 15):
        tft.line((w, y), (y, x), color)
        tft.line((y, x), (z, x), color)
        tft.line((z, x), (w, y), color)
        x -= 4
        y += 4
        z -= 4
        color += 100  # 每個三角形增大顏色值

# 測試函式：繪製圓角矩形
def testroundrects():
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    color = 100  # 起始顏色
    for t in range(5):
        x = 0
        y = 0
        w = tft.size()[0] - 2
        h = tft.size()[1] - 2
        for i in range(17):
            tft.rect((x, y), (w, h), color)
            x += 2
            y += 3
            w -= 4
            h -= 6
            color += 1100  # 顏色逐漸增加
        color += 100  # 每個循環後增加顏色

# 測試函式：在顯示器上顯示文字
def tftprinttest():
    tft.fill(TFT.BLACK)  # 清除顯示器內容
    v = 30
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 1, nowrap=True)  # 顯示文字
    v += sysfont["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, sysfont, 2, nowrap=True)  # 不同大小的文字
    v += sysfont["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, sysfont, 3, nowrap=True)  # 不同大小和顏色的文字
    v += sysfont["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, sysfont, 4, nowrap=True)  # 顯示數字
    time.sleep_ms(1500)  # 等待 1.5 秒
    tft.fill(TFT.BLACK)  # 清除顯示器
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont)  # 顯示文字
    v += sysfont["Height"]
    tft.text((0, v), str(math.pi), TFT.GREEN, sysfont)  # 顯示圓周率
    v += sysfont["Height"]
    tft.text((0, v), "Want pi?", TFT.GREEN, sysfont)  # 顯示問題
    v += sysfont["Height"] * 2
    tft.text((0, v), hex(8675309), TFT.GREEN, sysfont)  # 顯示十六進位
    v += sysfont["Height"]
    tft.text((0, v), "Print HEX!", TFT.GREEN, sysfont)  # 顯示文字
    v += sysfont["Height"] * 2
    tft.text((0, v), "Sketch has been", TFT.WHITE, sysfont)  # 顯示句子
    v += sysfont["Height"]
    tft.text((0, v), "running for: ", TFT.WHITE, sysfont)  # 顯示文字
    v += sysfont["Height"]
    tft.text((0, v), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)  # 顯示運行時間
    v += sysfont["Height"]
    tft.text((0, v), "seconds.", TFT.WHITE, sysfont)  # 顯示 "seconds"

# 測試主函式
def test_main():
    tft.rotation(2)  # 設定顯示方向
    tft.fill(TFT.BLACK)  # 清除顯示器
    tft.text((0, 0), "Lorem ipsum dolor sit amet...", TFT.WHITE, sysfont, 1)  # 顯示長文本
    time.sleep_ms(1000)  # 等待 1 秒

    tftprinttest()  # 執行文字測試
    time.sleep_ms(4000)  # 等待 4 秒

    testlines(TFT.YELLOW)  # 執行交叉線測試
    time.sleep_ms(500)  # 等待 0.5 秒

    testfastlines(TFT.RED, TFT.BLUE)  # 執行快速線測試
    time.sleep_ms(500)  # 等待 0.5 秒

    testdrawrects(TFT.GREEN)  # 繪製矩形
    time.sleep_ms(500)  # 等待 0.5 秒

    testfillrects(TFT.YELLOW, TFT.PURPLE)  # 繪製填充矩形
    time.sleep_ms(500)  # 等待 0.5 秒

    tft.fill(TFT.BLACK)  # 清除顯示器
    testfillcircles(10, TFT.BLUE)  # 繪製填充圓形
    testdrawcircles(10, TFT.WHITE)  # 繪製圓形
    time.sleep_ms(500)  # 等待 0.5 秒

    testroundrects()  # 繪製圓角矩形
    time.sleep_ms(500)  # 等待 0.5 秒

    testtriangles()  # 繪製三角形
    time.sleep_ms(500)  # 等待 0.5 秒

# 執行測試主函式
test_main()  # 執行主測試
