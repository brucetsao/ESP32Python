# Import necessary libraries
import urequests
import time
import ubinascii
import machine
import network
from machine import Pin, I2C      
import bme280        #importing BME280 library

ssid = 'replace_with_your_wifi_ssid'  # Write your SSID
password = 'replace_with_your_wifi_password'  # Write your Password

IFTTT_URL = '/trigger/BME280_Sensor_Readings/with/key/enter_your_key_here'
server = 'maker.ifttt.com'

last_message = 0
message_interval = 10

# Assign pins for BME280 sensor on Raspberry Pi Pico W
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)  # initializing the I2C method
bme = bme280.BME280(i2c=i2c)         

# Define function to connect to WiFi network
def connect_wifi(ssid, password):
  # Connect to your network
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())

def make_ifttt_request():
    print('Connecting to', server)
    json_data = '{"value1":"' + bme.values[0] + '","value2":"' + bme.values[1]  + \
        '","value3":"' + bme.values[2] + '"}'
    headers = {'Content-Type': 'application/json'}
    response = urequests.post('https://' + server + IFTTT_URL, data=json_data, headers=headers)
    print('Response:', response.content.decode())
    response.close()
    print('Closing Connection')
while True:
    if (time.time() - last_message) > message_interval:
        print('Sensor reading in progress...')
        connect_wifi(ssid, password)
        make_ifttt_request()
        last_message = time.time()
