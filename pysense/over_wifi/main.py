from network import WLAN
from pysense import Pysense
from base import CreateSensors
import pycom
import machine
import urequests
import time
import utime
import ujson

RED = 0x7f0000
GREEN = 0x007f00
YELLOW = 0x7f7f00
NO_COLOUR = 0x000000

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
# wlan.connect(ssid='LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

def get_data(json=False):
    # Pysense Object and sensors
    py = Pysense()
    pySensors = CreateSensors(py)

    data_sensors = {
        'acceleration': pySensors.get_acceleration(),
        'light': pySensors.get_light(),
        'temperature': pySensors.get_temperature()*100,
        'humidity': pySensors.get_humidity()*100,
        'altitude': pySensors.get_altitude()*100,
        'battery_voltage': py.read_battery_voltage()*100,
        'roll': pySensors.get_roll()*1000,
        'pitch': pySensors.get_pitch()*1000
    }

    json_data_sensors = ujson.dumps(data_sensors)

    if json==True:
        return json_data_sensors
    else:
        return data_sensors

def store_data(samples, interval):
    stored_data = {}
    for i in range(samples):
        time.sleep(interval)
        stored_data["{0}".format(i)] = get_data()

    json_stored_data = ujson.dumps(stored_data)

    print(type(stored_data))
    print(type(json_stored_data))

    return json_stored_data

def blinking_sleep(secs, colour):
    for i in range(secs):
        pycom.rgbled(colour)
        time.sleep(0.3)
        pycom.rgbled(NO_COLOUR)
        time.sleep(0.7)

def post_method(address, raw_data):
    response = urequests.post(address, data=raw_data)

    return response

sent = 0

while True:
    pycom.rgbled(RED)
    stored_data = store_data(10, 2)
    print(stored_data)
    response = post_method("http://192.168.1.162:5000/api/v1/users/", stored_data)
    sent += 1
    blinking_sleep(3, GREEN)
    print("{0}:{1}".format(sent,response))
    blinking_sleep(3, YELLOW)