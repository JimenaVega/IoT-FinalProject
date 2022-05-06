from network import WLAN
import machine
import usocket as socket
import time

wlan = WLAN(mode=WLAN.STA)

# wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
wlan.connect(ssid='LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

use_stream=False

s = socket.socket()

ai = socket.getaddrinfo("192.168.1.162", 5000)
print("Address infos:", ai)
addr = ai[0][-1]

print("Connect address:", addr)

s.connect(addr)

if use_stream:
    # MicroPython socket objects support stream (aka file) interface
    # directly, but the line below is needed for CPython.
    s = s.makefile("rwb", 0)
    s.write(b"GET / HTTP/1.0\r\n\r\n")
    print(s.read())
else:
    s.send(b"GET / HTTP/1.0\r\n\r\n")
    print(s.recv(8192))

print("Closing connection...")
s.close()