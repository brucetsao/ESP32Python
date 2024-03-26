import network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.disconnect()
aps = wifi.scan()
for ap in aps:
    for x in ap:
        #x.decode('utf-8')
        print("type:",type(x),end="/")
        print(x, end=",")
    print("\n==========================\ng")
    