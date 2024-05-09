# 引入 machine 模組中的 Pin 類別，用於控制 GPIO
from machine import Pin

# 引入 time 模組，用於延遲和時間相關操作
import time

# 定義 DHT 感測器連接的腳位
dht_pin = 16  # 使用 GPIO 16

# 初始化一個長度為 40 的位元流陣列，存儲從 DHT 感測器讀取的資料
bitstream = [0] * 40  # DHT 溫濕度感測器將傳輸 40 位的資料

# 定義 DHT 感測器讀取函式
def DHTread():
    # 初始化變數
    hum_hob = 0  # 濕度高位
    hum_lob = 0  # 濕度低位
    temp_hob = 0  # 溫度高位
    temp_lob = 0  # 溫度低位
    checksum = 0  # 校驗和
    global humidity, temperature, DataError  # 全域變數
    lastreadtime = 0  # 用於記錄最後一次讀取的時間
    
    # 觸發 DHT 感測器開始通訊
    dht = Pin(dht_pin, Pin.OUT)  # 設定腳位為輸出
    dht.low()  # 發送低脈衝，持續 1.1 毫秒
    time.sleep_us(1100)  # 等待 1.1 毫秒
    dht.high()  # 發送 40 微秒的高脈衝
    time.sleep_us(40)  # 等待 40 微秒
    dht = Pin(dht_pin, Pin.IN, Pin.PULL_UP)  # 設定腳位為輸入，並啟用上拉電阻
    
    # DHT 的信號確認
    while dht.value() == 0:  # 等待 DHT 拉低電位，持續 80 微秒
        pass
    while dht.value() == 1:  # 等待 DHT 拉高電位，持續 80 微秒
        pass
    
    # 讀取 40 位的資料，每個位包含一個高脈衝和一個低脈衝
    for i in range(40):
        lastreadtime = time.ticks_us()  # 記錄當前時間
        while dht.value() == 0:  # 等待低脈衝
            pass
        while dht.value() == 1:  # 等待高脈衝
            pass
        bitstream[i] = time.ticks_us() - lastreadtime  # 計算高脈衝的持續時間
    
    # 將位元流轉換為 1 和 0
    for i in range(40):
        if bitstream[i] < 100:  # 如果脈衝持續時間小於 100 微秒，則為 0
            bitstream[i] = 0
        else:  # 否則為 1
            bitstream[i] = 1
    
    # 將 40 位資料轉換為濕度、溫度和校驗和
    # 濕度高位的 8 位
    for i in range(8, 0, -1):
        if bitstream[8 - i] == 1:
            hum_hob |= 1 << (i - 1)  # 使用 OR 操作將 1 設定到相應位置

    # 濕度低位的 8 位
    for i in range(8, 0, -1):
        if bitstream[16 - i] == 1:
            hum_lob |= 1 << (i - 1)
    
    # 溫度高位的 8 位
    for i in range(8, 0, -1):
        if bitstream[24 - i] == 1:
            temp_hob |= 1 << (i - 1)
    
    # 溫度低位的 8 位
    for i in range(8, 0, -1):
        if bitstream[32 - i] == 1:
            temp_lob |= 1 << (i - 1)
    
    # 校驗和的 8 位
    for i in range(8, 0, -1):
        if bitstream[40 - i] == 1:
            checksum |= 1 << (i - 1)
    
    # 驗證校驗和是否正確
    if checksum == (hum_hob + hum_lob + temp_hob + temp_lob) & 0xFF:
        DataError = False
    else:
        DataError = True
    
    # 將濕度和溫度轉換為實際值
    humidity = ((hum_hob << 8) | hum_lob) * 0.1  # 濕度以 0.1% 為單位
    temperature = ((temp_hob & 0x7F) << 8 | temp_lob) * 0.1  # 溫度以 0.1°C 為單位

# 無限迴圈，每 2 秒讀取一次 DHT 感測器
while True:
    time.sleep(2)  # 延遲 2 秒
    DHTread()  # 讀取 DHT 感測器資料
    if not DataError:  # 如果校驗和正確
        print("Temp: {} °C".format(temperature))  # 列印溫度
        print("Humidity: {} %".format(humidity))  # 列印濕度
    else:
        print("Checksum Error")  # 校驗和錯誤
