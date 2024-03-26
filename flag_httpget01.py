

import network
import urequests
import time
import gc

# 連線至無線網路
sta=network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('NCNUIOT','12345678')

while not sta.isconnected() :
    pass

print('Wi-Fi connected.')

res = urequests.get("https://flagtech.github.io/flag.txt")
if(res.status_code == 200):
    print(res)
    res.close() # 或是 txt = res.text 也可以
    print("Success.")
        
gc.collect()
print("done") 
