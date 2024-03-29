# Visit Microcontrollerslab.com for complete project details

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

#set your unique OpenWeatherMap.org URL
#                       https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
open_weather_map_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=' + open_weather_map_api_key
print(open_weather_map_url)
weather_data = requests.get(open_weather_map_url)
print(weather_data.json())

# Location (City and Country code)
location = 'Location: ' + weather_data.json().get('name') + ' - ' + weather_data.json().get('sys').get('country')
print(location)

# Weather Description
description = 'Description: ' + weather_data.json().get('weather')[0].get('main')
print(description)

# Temperature
raw_temperature = weather_data.json().get('main').get('temp')-273.15

# Temperature in Celsius
temperature = 'Temperature: ' + str(raw_temperature) + '*C'
#uncomment for temperature in Fahrenheit
#temperature = 'Temperature: ' + str(raw_temperature*(9/5.0)+32) + '*F'
print(temperature)

# Pressure
pressure = 'Pressure: ' + str(weather_data.json().get('main').get('pressure')) + 'hPa'
print(pressure)

# Humidity
humidity = 'Humidity: ' + str(weather_data.json().get('main').get('humidity')) + '%'
print(humidity)

# Wind
wind = 'Wind: ' + str(weather_data.json().get('wind').get('speed')) + 'mps ' + str(weather_data.json().get('wind').get('deg')) + '*'
print(wind)