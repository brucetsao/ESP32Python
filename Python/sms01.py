# 尝试导入必要的库，如果失败则导入备用库
try:
  import urequests as requests  # 用于发送 HTTP 请求
except:
  import requests  # 备用库
  
import network  # 用于网络连接
import gc  # 用于垃圾收集
gc.collect()  # 释放未使用的内存

# Wi-Fi 连接的 SSID 和密码
ssid = 'Enter_Your_WiFi_SSID'  # 输入 Wi-Fi 的 SSID
password = 'Enter_Your_WiFi_PASSWORD'  # 输入 Wi-Fi 的密码

# Twilio 帐户的 SID 和身份验证令牌
account_sid = 'Enter_Your_Twilio_ACCOUNT_SID'  # Twilio 帐户 SID
auth_token = 'Enter_Your_Twilio_ACCOUNT_AUTH_TOKEN'  # Twilio 身份验证令牌
recipient_num = 'Enter_Recipient_number'  # 接收者的电话号码
sender_num = 'Enter_Sender_number'  # 发送者的电话号码

# 定义发送短信的函数
def send_sms(recipient, sender, message, auth_token, account_sid):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # 请求头
    # 发送短信所需的数据
    data = "To={}&From={}&Body={}".format(recipient, sender, message)
    # Twilio 的短信 API URL
    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(account_sid)
    
    print("Trying to send SMS with Twilio")  # 显示尝试发送短信
    
    # 发送 HTTP POST 请求以发送短信
    response = requests.post(url,
                             data=data,
                             auth=(account_sid, auth_token),  # 使用 SID 和令牌进行身份验证
                             headers=headers)
    
    # 检查 HTTP 响应状态码
    if response.status_code == 201:  # 如果状态码是 201，表示成功
        print("SMS sent!")  # 打印短信已发送
    else:
        print("Error sending SMS: {}".format(response.text))  # 打印错误信息
    
    response.close()  # 关闭响应

# 定义连接 Wi-Fi 的函数
def connect_wifi(ssid, password):
  station = network.WLAN(network.STA_IF)  # STA 模式用于连接 Wi-Fi
  station.active(True)  # 启用 Wi-Fi
  station.connect(ssid, password)  # 连接到 Wi-Fi
  while not station.isconnected():  # 等待连接成功
    pass
  print('Connection successful')  # 显示连接成功
  print(station.ifconfig())  # 打印网络配置

# 连接到 Wi-Fi
connect_wifi(ssid, password)

# 准备要发送的短信
message = "Hello, this is a test message"  # 短信内容
# 发送短信
send_sms(recipient_num, sender_num, message, auth_token, account_sid)  # 使用 Twilio 发送短信
