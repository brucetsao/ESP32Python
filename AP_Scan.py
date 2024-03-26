import esp,network,utime
esp.osdebug(None)
#import webrepl
#webrepl.start()
wifi= network.WLAN(network.STA_IF)
wifi.active(True)
try:
    wifi.connect('ncnuiot','iot12345')
    print('start to connect wifi')
    for i in range(10):
        print('try to connect wifi in {}s'.format(i))
        utime.sleep(1)
        if wifi.isconnected():
            break          
    if wifi.isconnected():
        print('WiFi connection OK!')
        print('Network Config=',wifi.ifconfig())
    else:
        print('WiFi connection Error')
except Exception as e: print(e)