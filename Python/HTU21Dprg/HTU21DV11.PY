# 這段 MicroPython 程式碼用於初始化 SoftI2C 通訊，
# 並與 HTU21D 溫濕度感測器通信，
# 同時將數據顯示在 SSD1306 OLED 顯示模組上。
# 程式還將讀取到的溫濕度數據，
# 以特定格式拼接成網址，
# 並每隔幾秒重複執行。
# 這段程式碼的主要功能是通過 SoftI2C 讀取 HTU21D 溫濕度感測器的數據，
# 並將其顯示在 SSD1306 OLED 顯示模組上。
# 此外，它還會根據讀取的溫濕度數據生成一個特定格式的網址。
# 該程式碼無限循環，
# 每隔 5 秒鐘讀取和顯示數據


# 匯入必要的模組，包括 HTU21D、自訂函式庫、SSD1306 OLED 顯示模組、GPIO 和 SoftI2C 通訊
from HTU21D import HTU21D  # 使用 HTU21D 溫濕度感測器
from myLib import *  # 使用自訂函式庫
import ssd1306  # 使用 SSD1306 OLED 顯示模組
from machine import Pin, SoftI2C, I2C  # 控制腳位和 I2C 通訊
import utime  # 用於時間延遲

# 初始化 SoftI2C 通訊，指定 SCL 和 SDA 的腳位，以及通訊頻率
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100_000)

# 初始化 SSD1306 OLED 顯示模組，解析度為 128x32，使用 I2C 通訊
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 從自訂函式庫中取得 MAC 地址，並將其儲存在變數中
macstr = GetMAC()

# 建立一個格式化的網址字串，用於上傳溫濕度數據
urlstr0 = "http://iot.arduino.org.tw:8888/bigdata/dhtdata/dhDatatadd.php?MAC=%s&T=%3.2f&H=%3.1f"

# 清除 OLED 顯示模組的畫面
display.fill(0)
display.show()  # 更新 OLED 顯示模組

# 在 OLED 上顯示 MAC 地址
display.text(macstr, 0, 0, 1)  # 在位置 (0, 0) 顯示 MAC 地址

# 初始化 HTU21D 溫濕度感測器，使用 SoftI2C 通訊
lectura = HTU21D(22, 21)

# 無限迴圈，每隔 5 秒讀取溫濕度數據，並將其顯示在 OLED 上
while True:
    # 讀取感測器的濕度和溫度
    hum = lectura.humidity  # 取得濕度
    temp = lectura.temperature  # 取得溫度

    # 在控制台顯示溫度和濕度
    print('Humedad:', hum)  # 顯示濕度
    print('Temperatura:', temp)  # 顯示溫度

    # 在 OLED 上顯示溫度和濕度
    display.rect(0, 10, 128, 10, 0, 1)  # 在 OLED 上繪製矩形
    display.text('Temp:' + str(temp), 0, 10, 1)  # 顯示溫度資訊
    display.rect(0, 20, 128, 10, 0, 1)  # 繪製另一個矩形
    display.text('Humid:' + str(hum), 0, 20, 1)  # 顯示濕度資訊
    display.show()  # 更新 OLED 顯示模組，將新內容顯示

    # 使用格式化的字串來更新網址，將溫濕度數據插入其中
    urlstr = urlstr0 % (macstr, temp, hum)  # 格式化網址
    print(urlstr)  # 在控制台顯示網址

    # 等待 5 秒鐘，再次讀取數據
    utime.sleep(5)
