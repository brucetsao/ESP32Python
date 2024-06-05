# 從 Paino 模組引入所有函式和類別
from Paino import *

# 設定蜂鳴器的腳位
buzzerPIN = 7  # 蜂鳴器連接的腳位

# 建立一個 Paino 類別的實例，並指定蜂鳴器的腳位
music = Paino(buzzerPIN)  # 使用 buzzerPIN 初始化 Paino 物件

# 使用 Paino 類別的 beep 函式發出蜂鳴器的聲音
music.beep()  # 發出預定義的蜂鳴器聲音
