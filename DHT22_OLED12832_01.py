# 引入 MicroPython 的 Pin 和 I2C 類別，用於控制 GPIO 和 I2C 通訊
from machine import Pin, I2C

# 引入 ssd1306 函式庫，用於控制 OLED 顯示器
import ssd1306

# 引入 time 模組中的 sleep 函式，用於延遲
from time import sleep

# 引入 dht 模組，用於使用 DHT 溫濕度感測元件
import dht

# 初始化 DHT22 溫濕度感測器，連接到 GPIO 16
sensor = dht.DHT22(Pin(16))  # 生成連接到 GPIO 16 的 DHT22 感測器物件
# 也可以使用 DHT11
# sensor1 = dht.DHT11(Pin(16))

# 使用 I2C 通訊建立 I2C 物件，指定 sda 和 scl 腳位
i2c = I2C(id=1, scl=Pin(7), sda=Pin(6), freq=100_000)  # 設定 I2C ID、時鐘腳位和資料腳位

# 初始化 OLED 顯示器，解析度為 128x32，通過 I2C 通訊
display = ssd1306.SSD1306_I2C(128, 32, i2c)  # 建立 OLED 物件
display.fill(0)  # 清除 OLED 的內容
display.show()  # 顯示器初始化，將清除後的內容顯示

# 無限迴圈，持續讀取溫濕度感測器，並在 OLED 上顯示結果
while True:
    # 讀取 DHT22 溫濕度感測器
    sensor.measure()  # 呼叫感測器進行測量
    temp = sensor.temperature()  # 取得溫度
    hum = sensor.humidity()  # 取得濕度
    
    # 在控制台顯示溫度和濕度
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))  # 格式化輸出
    
    # 將溫度和濕度轉換為文本，準備在 OLED 上顯示
    txt1 = "Temperature: %3.1f" % temp  # 格式化溫度
    txt2 = "Humidity: %3.1f" % hum  # 格式化濕度
    
    # 清除 OLED 的內容，準備顯示新的資料
    display.fill(0)  # 將 OLED 全部填充為黑色
    
    # 在 OLED 上顯示溫度和濕度
    display.text(txt1, 0, 0, 1)  # 在 OLED 的 (0, 0) 位置顯示溫度
    display.text(txt2, 0, 10, 1)  # 在 OLED 的 (0, 10) 位置顯示濕度
    
    # 更新 OLED，將資料顯示出來
    display.show()  # 將顯示器的緩衝區內容更新
    
    # 延遲 2 秒，避免過於頻繁的測量
    sleep(2)  # 暫停兩秒鐘
