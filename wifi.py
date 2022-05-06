from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

while True:
    True