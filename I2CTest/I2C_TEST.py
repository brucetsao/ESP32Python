from machine import I2C,Pin
#Initialize the I2C 
#i2c = I2C(id=1,scl=Pin(7),sda=Pin(6),freq=100_000)
i2c = I2C(id=1,scl=Pin(7),sda=Pin(6), freq=100_000)
#產生i2c 物件， 用I2C 類別產生，id=哪一組I2C, scl=Pin(GPIO號碼),sda=Pin(GPIO號碼)
i2c0 = I2C(id=0,scl=Pin(9),sda=Pin(8),freq=100_000)
#產生i2c 物件， 用I2C 類別產生，id=哪一組I2C, scl=Pin(GPIO號碼),sda=Pin(GPIO號碼)
# Get the address of all devices under the I2C bus
addr_list = i2c.scan()	#掃描I2C BUS有哪些裝置
# Resolving device information
if len(addr_list) >= 1:	 #有找到一組以上I2C裝置
    print("in I2C(%d)" % 1)		#印出哪一組I2C編號
    for x in addr_list:		#列出所有找到的I2C裝置
        #who = i2c.readfrom_mem(x,0x00,1)	#取出I2C 裝置屬性
        print(x)
        # Identify ICM20948
        print("Have a device connected ")
        #print("address is :(%x)" % int(x[0]))	#取出I2C 裝置屬性第一個是I2C device adderess
# Nothing connected
elif len(addr_list) == 0:
    print("in I2C(%d)" % 1)
    print("Nothing connected")
# More than one device is connected
else:
    print("More than one device is connected")

#------------------------------------------------
addr_list = i2c0.scan()	#掃描I2C BUS有哪些裝置
# Resolving device information
if len(addr_list) >= 1:		#有找到一組以上I2C裝置
    print("in I2C(%d)" % 0)	#印出哪一組I2C編號
    for x in addr_list:		#列出所有找到的I2C裝置
        #who = i2c0.readfrom_mem(x,0x00,1)	#取出I2C 裝置屬性
        print(x)
        # Identify ICM20948
        print("Have a device connected ")
        #print("address is :(%x)" % who[0])	#取出I2C 裝置屬性第一個是I2C device adderess
# Nothing connected
elif len(addr_list) == 0:
    print("Nothing connected")
# More than one device is connected
else:
    print("More than one device is connected")

#------------------------------------------------
    
