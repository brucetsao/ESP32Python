# 引入 ping3 模組，用於執行 ping 操作
import ping3  # 用於測試網路連通性

# 使用 ping3 對目標主機進行 ping 操作
response = ping3.ping("www.baidu.com", timeout=5)  # 對 www.baidu.com 進行 ping，設置超時 5 秒

# 檢查是否有回應
if response:  # 如果有回應
    print("Success")  # 打印 "Success"
else:  # 如果沒有回應
    print("Fail")  # 打印 "Fail"
