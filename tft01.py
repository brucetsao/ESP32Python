# 引入必要的函式庫
from ST7735 import TFT  # 引入 ST7735 螢幕控制庫
from sysfont import sysfont  # 引入系統字型
from umachine import SPI, Pin  # 引入 SPI 和 Pin
import time  # 引入時間函式庫
import math  # 引入數學函式庫

# 初始化 SPI 介面
spi = SPI(1, baudrate=10000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)  # 設定 SPI 的頻率和針腳
# 初始化 TFT 顯示器
tft = TFT(spi, 16, 17, 18)  # 設定 TFT 的引腳
tft.initb2()  # 初始化 TFT
tft.rgb(True)  # 設定為 RGB 模式
 
# 定義一組畫線的測試函式
def testlines(color):
    tft.fill(TFT.BLACK)  # 將螢幕填充為黑色
    # 繪製對角線
    for x in range(0, tft.size()[0], 6):
        tft.line((0, 0), (x, tft.size()[1] - 1), color)  # 繪製斜線
    for y in range(0, tft.size()[1], 6):
        tft.line((0, 0), (tft.size()[0] - 1, y), color)  # 繪製另一個方向的斜線
 
    tft.fill(TFT.BLACK)  # 重置螢幕
    # 繪製從另一個角落的斜線
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, 0), (0, y), color)
 
# 繪製快速線
def testfastlines(color1, color2):
    tft.fill(TFT.BLACK)  # 填充螢幕
    # 繪製水平線
    for y in range(0, tft.size()[1], 5):
        tft.hline((0, y), tft.size()[0], color1)  # 繪製水平線
    # 繪製垂直線
    for x in range(0, tft.size()[0], 5):
        tft.vline((x, 0), tft.size()[1], color2)  # 繪製垂直線
 
# 繪製矩形
def testdrawrects(color):
    tft.fill(TFT.BLACK)  # 填充螢幕
    for x in range(0, tft.size()[0], 6):
        tft.rect((tft.size()[0] // 2 - x // 2, tft.size()[1] // 2 - x // 2), (x, x), color)  # 在中心繪製矩形
 
# 繪製填充的矩形
def testfillrects(color1, color2):
    tft.fill(TFT.BLACK)  # 填充螢幕
    for x in range(tft.size()[0], 0, -6):
        tft.fillrect((tft.size()[0] // 2 - x // 2, tft.size()[1] // 2 - x // 2), (x, x), color1)  # 在中心填充矩形
        tft.rect((tft.size()[0] // 2 - x // 2, tft.size()[1] // 2 - x // 2), (x, x), color2)  # 繪製矩形框
 
# 繪製填充的圓圈
def testfillcircles(radius, color):
    for x in range(radius, tft.size()[0], radius * 2):
        for y in range radius, tft.size()[1], radius * 2):
            tft.fillcircle((x, y), radius, color)  # 填充圓圈
 
# 繪製圓圈
def testdrawcircles(radius, color):
    for x in range(0, tft.size()[0] + radius, radius * 2):
        for y in range(0, tft.size()[1] + radius, radius * 2):
            tft.circle((x, y), radius, color)  # 繪製圓圈
 
# 繪製三角形
def testtriangles():
    tft.fill(TFT.BLACK)  # 填充螢幕
    color = 0xF800  # 設定顏色
    w = tft.size()[0] // 2
    x = tft.size()[1] - 1
    y = 0
    z = tft.size()[0]
    for t in range(0, 15):
        tft.line((w, y), (y, x), color)  # 繪製三角形的邊
        tft.line((y, x), (z, x), color)
        tft.line((z, x), (w, y), color)
        x -= 4
        y += 4
        z -= 4
        color += 100
 
# 繪製圓角矩形
def testroundrects():
    tft.fill(TFT.BLACK)  # 填充螢幕
    color = 100
    for t in range(5):
        x = 0
        y = 0
        w = tft.size()[0] - 2
        h = tft.size()[1] - 2
        for i in range(17):
            tft.rect((x, y), (w, h), color)  # 繪製圓角矩形
            x += 2
            y += 3
            w -= 4
            h -= 6
            color += 1100
        color += 100
 
# 測試文字顯示
def tftprinttest():
    tft.fill(TFT.BLACK)  # 填充螢幕
    v = 30
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 1, nowrap=True)  # 顯示文字
    v += sysfont["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, sysfont, 2, nowrap=True)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, sysfont, 3, nowrap=True)
    v += sysfont["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, sysfont, 4, nowrap=True)  # 顯示數字
    time.sleep_ms(1500)  # 等待 1.5 秒
    tft.fill(TFT.BLACK)  # 填充螢幕
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont)  # 繼續顯示文字
    v += sysfont["Height"]
    tft.text((0, v), str(math.pi), TFT.GREEN, sysfont)  # 顯示圓周率
    v += sysfont["Height"]
    tft.text((0, v), "Want pi?", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), hex(8675309), TFT.GREEN, sysfont)  # 顯示十六進位數字
    v += sysfont["Height"]
    tft.text((0, v), "Print HEX!", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Sketch has been", TFT.WHITE, sysfont)  # 顯示字串
    v += sysfont["Height"]
    tft.text((0, v), "running for: ", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)  # 顯示運行時間
    v += sysfont["Height"]
    tft.text((0, v), "seconds.", TFT.WHITE, sysfont)  # 顯示單位
 
# 執行主測試函數
def test_main():
    tft.fill(TFT.BLACK)  # 填充螢幕
    tft.text((0, 0), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat.", TFT.WHITE, sysfont, 1)  # 顯示較長的字串
    time.sleep_ms(1000)  # 等待 1 秒
 
    tftprinttest()  # 測試文字顯示
    time.sleep_ms(4000)  # 等待 4 秒
 
    testlines(TFT.YELLOW)  # 測試畫線
    time.sleep_ms(500)  # 等待 0.5 秒
 
    testfastlines(TFT.RED, TFT.BLUE)  # 測試快速畫線
    time.sleep_ms(500)
 
    testdrawrects(TFT.GREEN)  # 測試繪製矩形
    time.sleep_ms(500)
 
    testfillrects(TFT.YELLOW, TFT.PURPLE)  # 測試填充矩形
    time.sleep_ms(500)
 
    tft.fill(TFT.BLACK)  # 填充螢幕
    testfillcircles(10, TFT.BLUE)  # 測試填充圓圈
    testdrawcircles(10, TFT.WHITE)  # 測試繪製圓圈
    time.sleep_ms(500)
 
    testroundrects()  # 測試圓角矩形
    time.sleep_ms(500)
 
    testtriangles()  # 測試三角形
    time.sleep_ms(500)
 
test_main()  # 執行主測試函數
