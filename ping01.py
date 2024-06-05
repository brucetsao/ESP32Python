

def ping():
    rq = requests.get("http://www.example.com")  # 向example.com发送get请求
    if rq.status_code != 200 or "Example Domain" not in rq.text:  # 分析返回内容是否正确
        print("Unconnected to the Internet!")
        rq.close()  # 注意此处有必要关闭response对象，同时开启过多的response对象会导致报错OSError 32
        return False
    else:
        print("Connected to the Internet!")
        rq.close()
        return True
