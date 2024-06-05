from machine import I2C  # 匯入 I2C 模組
from bmp280 import *  # 匯入 BMP280 感測器模組

# 初始化 I2C 總線
bus = I2C()

# 初始化 BMP280 感測器，並將其連接到 I2C 總線
bmp = BMP280(bus)

# 設定 BMP280 的使用情境為氣象模式
bmp.use_case(BMP280_CASE_WEATHER)

# 設定 BMP280 的過採樣率為高
bmp.oversample(BMP280_OS_HIGH)

# 設定溫度過採樣率為 8 倍
bmp.temp_os = BMP280_TEMP_OS_8

# 設定氣壓過採樣率為 4 倍
bmp.press_os = BMP280_PRES_OS_4

# 設定待機時間為 250 毫秒
bmp.standby = BMP280_STANDBY_250

# 設定 IIR 濾波器的係數為 2
bmp.iir = BMP280_IIR_FILTER_2

# 啟用三線 SPI 接口
bmp.spi3w = BMP280_SPI3W_ON

# 設定電源模式為強制模式
bmp.power_mode = BMP280_POWER_FORCED

# 或者使用強制測量模式
bmp.force_measure()

# 設定電源模式為正常模式
bmp.power_mode = BMP280_POWER_NORMAL

# 或者使用正常測量模式
bmp.normal_measure()

# 或者檢查是否在正常模式
bmp.in_normal_mode()

# 設定電源模式為睡眠模式
bmp.power_mode = BMP280_POWER_SLEEP

# 或者進入睡眠模式
bmp.sleep()

# 打印感測器讀取的溫度值
print(bmp.temperature)

# 打印感測器讀取的氣壓值
print(bmp.pressure)

# 檢查感測器是否正在測量，測量時返回 True
bmp.is_measuring

# 檢查感測器是否正在將數據複製到寄存器，複製時返回 True
bmp.is_updating
