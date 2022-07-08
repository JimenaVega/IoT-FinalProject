import urequests
import ujson
import pycom
import machine
import time
from network import WLAN

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

# wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
wlan.connect(ssid='LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

ADDRESS = "http://192.168.1.107:8080/api/v1/hftE8awQVgB6j5NgOFMw/telemetry"
headers = {'Content-Type': 'application/json'}

for i in range(5):
    data = ujson.dumps({"temperature": 70+i})
    print(data)
    response = urequests.post(ADDRESS, data=data, headers=headers)
    time.sleep(1)