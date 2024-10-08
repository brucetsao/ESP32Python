from ESP32WebServer import *
import network
import machine

GPIO_NUM = 2 # Builtin led (D4)

# Wi-Fi configuration
STA_SSID = "NCNUIOT"
STA_PSK = "12345678"

# Disable AP interface
ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
    ap_if.active(False)

# Connect to Wi-Fi if not connected
sta_if = network.WLAN(network.STA_IF)
if not ap_if.active():
    sta_if.active(True)
if not sta_if.isconnected():
    sta_if.connect(STA_SSID, STA_PSK)
    # Wait for connecting to Wi-Fi
    while not sta_if.isconnected(): 
        pass

# Show IP address
print("Server started @", sta_if.ifconfig()[0])

# Get pin object for controlling builtin LED
pin = machine.Pin(GPIO_NUM, machine.Pin.OUT)
pin.on() # Turn LED off (it use sinking input)

# Handler for path "/cmd?led=[on|off]"    
def handleCmd(socket, args):
    if 'led' in args:
        if args['led'] == 'on':
            pin.off()
        elif args['led'] == 'off':
            pin.on()
        ESP32WebServer.ok(socket, "200", args["led"])
    else:
        ESP32WebServer.err(socket, "400", "Bad Request")

# Start the server @ port 8899
ESP32WebServer.begin(8899)

# Register handler for each path
ESP32WebServer.onPath("/cmd", handleCmd)

try:
    while True:
        # Let server process requests
        ESP32WebServer.handleClient()
except:
    ESP32WebServer.close()