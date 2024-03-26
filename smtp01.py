# Import necessary libraries
import umail # Micropython lib to send emails: https://github.com/shawwwn/uMail
import network
import bme280        
import network
from machine import Pin, I2C    

# Your network credentials
ssid = 'replace_with_your_ssid' # Replace with the name of your network
password = 'replace_with_your_password' # Replace with your network password

# Email details
sender_email = 'write_senders_email' # Replace with the email address of the sender
sender_name = 'BME280 Mail Client' # Replace with the name of the sender
sender_app_password = 'write_senders_app_password' # Replace with the app password of the sender's email account
recipient_email ='write_receivers_email' # Replace with the email address of the recipient
email_subject = 'BME280 Sensor Readings' # Subject of the email

# Assign pins for BME280 sensor on Raspberry Pi Pico W
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)  # initializing the I2C method
bme = bme280.BME280(i2c=i2c)         

# Define function to read sensor data
def read_bme_sensor():
  try:
    # Get sensor readings
    temp = bme.values[0] # Temperature in Celsius
    hum = bme.values[2] # Humidity in %
    pres = bme.values[1] # Pressure in hPa

    return temp, hum, pres
    # else:
    #   return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')
  
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
    
# Connect to your WiFi network
connect_wifi(ssid, password)

# Get sensor readings
temp, hum, pres = read_bme_sensor()
print(temp)
print(hum)
print(pres)

# Send email with sensor readings
smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
smtp.login(sender_email, sender_app_password)
smtp.to(recipient_email)
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
smtp.write("Temperature " + temp + "\n")
smtp.write("Humidity " + hum + "\n")
smtp.write("Pressure " + pres + "\n")
smtp.send()
smtp.quit()