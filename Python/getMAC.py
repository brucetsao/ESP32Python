import network#網路使用套件
import ubinascii#轉換N進位顯示使用套件
 
wlan = network.WLAN(network.STA_IF)#建立網路物件	#正常上網模式
wlan.active(True)#啟動網路物件
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
#透過網路物件方法，取得網路卡編號，並把取得網路卡編號變數轉成16進位表示之文字
# ubinascii.hexlify(要轉換的mac address).decode()
# network.WLAN().config('mac')  取得網路卡編號
print(mac.upper())	#字串.upper()，將這個字串轉成大寫英文
#先將取得網路卡編號的字串，轉成大寫英文文字後，印出來