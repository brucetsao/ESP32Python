# 引入自定義的 Servo 模組和時間相關模組
from myservo import Servo  # 從 myservo 模組引入 Servo 類
import time  # 用於時間相關操作
 
# 初始化伺服機物件，並設置伺服機的控制引腳
servo = Servo(15)  # 使用 GPIO 15 作為伺服機的控制引腳

# 設置伺服機角度為 0 度
servo.ServoAngle(0)  # 將伺服機設置為 0 度
time.sleep_ms(1000)  # 暫停 1 秒

# 使用 try-except 以防止意外發生
try:
    # 無限迴圈，讓伺服機來回旋轉
    while True:       
        # 讓伺服機從 0 度旋轉到 180 度
        for i in range(0, 180, 1):  # 以 1 度為步進，從 0 度旋轉到 180 度
            servo.ServoAngle(i)  # 設置伺服機的角度
            time.sleep_ms(15)  # 每個步進之間等待 15 毫秒
        # 讓伺服機從 180 度旋轉回 0 度
        for i in range(180, 0, -1):  # 以 1 度為步進，從 180 度旋轉回 0 度
            servo.ServoAngle(i)  # 設置伺服機的角度
            time.sleep_ms(15)  # 每個步進之間等待 15 毫秒        
except:  # 捕捉所有異常
    servo.deinit()  # 如果發生異常，停用伺服機
