from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import gc
gc.collect()

ssid = 'HUAWEI-u67E'
password = '4uF77R2n'
mqtt_server = '192.168.18.8'  #Replace with your MQTT Broker IP

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'rpi_pico_w/test_pub'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

def connect():
  print('Connecting to MQTT Broker...')
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect()
except OSError as e:
  restart_and_reconnect()
  
push_button = Pin(15, Pin.IN)
push_button_Prv_state = False
mesg_id = 0

while True:
  try:
    msg = "Message id: " + str(mesg_id)
    print('Publishing message: %s on topic %s' % (msg, topic_pub))
    client.publish(topic_pub, msg)
    time.sleep(2)
    mesg_id = mesg_id + 1
  except OSError as e:
    restart_and_reconnect()