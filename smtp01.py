# 引入所需的函式庫
import umail  # 用於發送電子郵件的 MicroPython 函式庫：https://github.com/shawwwn/uMail
import network  # 用於網路連接
import bme280  # 用於操作 BME280 感測器
from machine import Pin, I2C  # 用於控制 GPIO 和 I2C

# 網路憑證
ssid = 'replace_with_your_ssid'  # 您的網路名稱
password = 'replace_with_your_password'  # 您的網路密碼

# 電子郵件詳細信息
sender_email = 'write_senders_email'  # 發送者的電子郵件地址
sender_name = 'BME280 Mail Client'  # 發送者的名稱
sender_app_password = 'write_senders_app_password'  # 發送者的應用程序密碼
recipient_email = 'write_receivers_email'  # 接收者的電子郵件地址
email_subject = 'BME280 Sensor Readings'  # 電子郵件主題

# 設定 BME280 感測器的引腳
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)  # 初始化 I2C 物件
bme = bme280.BME280(i2c=i2c)  # 初始化 BME280 感測器

# 定義函數以讀取感測器數據
def read_bme_sensor():
  try:
    # 取得感測器讀數
    temp = bme.values[0]  # 溫度（攝氏）
    hum = bme.values[2]  # 濕度（百分比）
    pres = bme.values[1]  # 氣壓（hPa）

    return temp, hum, pres  # 返回感測器讀數
  except OSError as e:  # 捕捉感測器讀取失敗的例外
    return('Failed to read sensor.')  # 返回錯誤訊息

# 定義函數以連接 WiFi 網路
def connect_wifi(ssid, password):
  # 連接到指定的網路
  station = network.WLAN(network.STA_IF)  # 使用 STA 模式
  station.active(True)  # 啟用網路
  station.connect(ssid, password)  # 連接到 WiFi
  while not station.isconnected():  # 等待連接成功
    pass
  print('Connection successful')  # 顯示連接成功
  print(station.ifconfig())  # 打印網路配置

# 連接到 WiFi 網路
connect_wifi(ssid, password)

# 取得感測器讀數
temp, hum, pres = read_bme_sensor()  # 讀取 BME280 感測器的溫度、濕度和氣壓
print(temp)  # 打印溫度
print(hum)  # 打印濕度
print(pres)  # 打印氣壓

# 發送電子郵件包含感測器讀數
smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)  # 使用 Gmail 的 SSL 埠
smtp.login(sender_email, sender_app_password)  # 使用電子郵件和應用程序密碼登入
smtp.to(recipient_email)  # 設置收件人
smtp.write("From:" + sender_name + "<" + sender_email + ">\n")  # 發送者信息
smtp.write("Subject:" + email_subject + "\n")  # 電子郵件主題
smtp.write("Temperature: " + temp + "\n")  # 電子郵件正文中的溫度
smtp.write("Humidity: " + hum + "\n")  # 電子郵件正文中的濕度
smtp.write("Pressure: " + pres + "\n")  # 電子郵件正文中的氣壓
smtp.send()  # 發送電子郵件
smtp.quit()  # 結束 SMTP 連接
