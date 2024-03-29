# Visit Microcontrollerslab.com for complete project details
import gc 
import time

try:
  import urequests as requests
except:
  import requests
  
try:
  import ujson as json
except:
  import json

import network

import gc
gc.collect()

ssid = 'NCNUIOT'
password = '12345678'

city = 'Puli'
country_code = 'TW'
#example
#city = 'Lahore'
#country_code = 'PAK'

open_weather_map_api_key = 'a14064cb58b67aff9d6116e82b3364dd'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

gc.collect()   
#set your unique OpenWeatherMap.org URL
#                       https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
httpget_url = 'http://ncnu.arduino.org.tw:9999/ems/GetAllDevice.php'
print(httpget_url)
r = requests.get(httpget_url)
#httpget_data.decode()
#data=json.loads(r.text)
#data=json.dumps(r.text, ensure_ascii=False).encode('utf8')
data=json.dumps(r.text)
print(data)
gc.collect()


#data = httpget_data.json(encoding = 'utf-8')

#data1 = json.loads(json.dumps(data).encode('utf-8'))
#print(json.dumps(data, indent=4, sort_keys=True))

