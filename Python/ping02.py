import ping3

response = ping3.ping("www.baidu.com", timeout=5)
if response:
    print("Success")
else:
    print("Fail")