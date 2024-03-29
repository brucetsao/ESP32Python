import network#網路使用套件
import ubinascii#轉換N進位顯示使用套件
 
wlan = network.WLAN(network.STA_IF)#建立網路物件
wlan.active(True)#啟動網路物件
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
#透過網路物件方法，取得網路卡編號，並把取得網路卡編號變數轉成16進位表示之文字
print(mac.upper())
#先將取得網路卡編號的字串，轉成大寫英文文字後，印出來