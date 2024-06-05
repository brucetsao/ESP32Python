# 這段 MicroPython 程式碼提供了一個名為 strftime 的函數，
# 用於根據特定的日期格式將時間戳轉換為格式化的日期字串。
# 這個程式碼定義了 strftime 函數，
# 它接收日期格式字串和時間戳，
# 並根據日期格式將時間戳轉換為格式化的日期字串。
# 它支援多種格式化選項，
# 如星期幾、月份、日期、時間、分鐘、秒、AM/PM 等。
# 這在 MicroPython 環境中實用，
# 可以用來顯示或記錄格式化的日期和時間。


# 匯入必要的模組
from utime import *  # 時間相關函數，如 sleep、time、localtime
from micropython import const  # 用於定義常數

# 定義時間戳索引的常數
_TS_YEAR = const(0)  # 年
_TS_MON = const(1)  # 月
_TS_MDAY = const(2)  # 日
_TS_HOUR = const(3)  # 小時
_TS_MIN = const(4)  # 分鐘
_TS_SEC = const(5)  # 秒
_TS_WDAY = const(6)  # 星期幾
_TS_YDAY = const(7)  # 一年中的第幾天
_TS_ISDST = const(8)  # 夏令時

# 定義星期幾的名稱
_WDAY = const(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))

# 定義月份的名稱
_MDAY = const(
    (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )
)

# 定義 `strftime` 函數，用於根據指定的日期格式轉換時間戳
def strftime(datefmt, ts):
    from io import StringIO  # 引入 StringIO，用於構建字串

    fmtsp = False  # 格式化標記，用於檢測百分號
    ftime = StringIO()  # 初始化字串緩衝區

    # 遍歷日期格式字串
    for k in datefmt:
        if fmtsp:  # 如果遇到百分號
            if k == "a":
                ftime.write(_WDAY[ts[_TS_WDAY]][0:3])  # 簡寫星期幾
            elif k == "A":
                ftime.write(_WDAY[ts[_TS_WDAY]])  # 全寫星期幾
            elif k == "b":
                ftime.write(_MDAY[ts[_TS_MON] - 1][0:3])  # 簡寫月份
            elif k == "B":
                ftime.write(_MDAY[ts[_TS_MON] - 1])  # 全寫月份
            elif k == "d":
                ftime.write("%02d" % ts[_TS_MDAY])  # 格式化日
            elif k == "H":
                ftime.write("%02d" % ts[_TS_HOUR])  # 格式化 24 小時制
            elif k == "I":
                ftime.write("%02d" % (ts[_TS_HOUR] % 12))  # 格式化 12 小時制
            elif k == "j":
                ftime.write("%03d" % ts[_TS_YDAY])  # 格式化一年中的第幾天
            elif k == "m":
                ftime.write("%02d" % ts[_TS_MON])  # 格式化月
            elif k == "M":
                ftime.write("%02d" % ts[_TS_MIN])  # 格式化分鐘
            elif k == "P":
                ftime.write("AM" if ts[_TS_HOUR] < 12 else "PM")  # AM/PM
            elif k == "S":
                ftime.write("%02d" % ts[_TS_SEC])  # 格式化秒
            elif k == "w":
                ftime.write(str(ts[_TS_WDAY]))  # 星期幾的數字表示
            elif k == "y":
                ftime.write("%02d" % (ts[_TS_YEAR] % 100))  # 兩位數的年份
            elif k == "Y":
                ftime.write(str(ts[_TS_YEAR]))  # 四位數的年份
            else:
                ftime.write(k)  # 如果是其他字符，直接寫入
            fmtsp = False  # 重置格式化標記
        elif k == "%":
            fmtsp = True  # 如果遇到百分號，設為 True
        else:
            ftime.write(k)  # 如果不是格式化字符，直接寫入

    val = ftime.getvalue()  # 取得構建的字串
    ftime.close()  # 關閉 StringIO
    return val  # 回傳格式化的日期字串


__version__ = '0.1.0'  # 版本號
