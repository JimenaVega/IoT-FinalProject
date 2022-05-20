'''
Simple Pyscan NFC / MiFare Classic Example
Copyright (c) 2019, Pycom Limited.

This example continuously sends a REQA for ISO14443A card type
If a card is discovered, it will read the UID
If DECODE_CARD = True, will attempt to authenticate with CARDkey
If authentication succeeds will attempt to read sectors from the card
'''
# PYSCAN
from pycoproc_1 import Pycoproc
from MFRC630 import MFRC630
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01

#OTHER 
from network import WLAN
import machine
import urequests
import ujson
import time
import pycom

RGB_BRIGHTNESS = 0x8

RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

counter = 0

py = Pycoproc(Pycoproc.PYSCAN)
nfc = MFRC630(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True



pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))


def check_uid(uid, len):
    return VALID_CARDS.count(uid[:len])

def send_sensor_data(name, timeout):
    if(pybytes_enabled):
        while(True):
            pybytes.send_signal(2, lt.light())
            pybytes.send_signal(3, li.acceleration())
            time.sleep(timeout)

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

def get_data():
    data_sensors = {
        'acceleration': li.acceleration(),
        'light': lt.light()
    }
    json_data_sensors = ujson.dumps(data_sensors)

    return json_data_sensors


print('Scanning for cards')
while(1):
    response = urequests.post("http://192.168.1.162:5000/api/v1/users/", data=get_data())
    print(response)
    time.sleep(1)

