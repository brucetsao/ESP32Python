# 引入 MicroPython 的機器和時間相關模組
import machine  # 用於控制硬體
import utime  # 用於時間相關操作
 
# 初始化 ADC，將 GPIO 26 用於類比轉數位轉換
analog_value = machine.ADC(26)  # 初始化 ADC 物件，使用 GPIO 26
 
# 無限迴圈，持續讀取 ADC 值
while True:
    # 讀取 ADC 的 16 位類比值
    reading = analog_value.read_u16()  # 讀取類比值，返回 0 到 65535 之間的整數
    # 輸出 ADC 值到終端
    print("ADC:", reading)  # 打印 ADC 讀數
    # 等待 0.2 秒，然後再次讀取
    utime.sleep(0.2)  # 延遲 0.2 秒
