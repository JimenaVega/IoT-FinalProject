from network import WLAN
from pysense import Pysense
from base import CreateSensors
import pycom
import machine
import urequests
import time
import ujson

RED = 0x7f0000
GREEN = 0x007f00
YELLOW = 0x7f7f00

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
# wlan.connect(ssid='LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

def get_data():
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

    return json_data_sensors

for i in range(4):
    pycom.rgbled(RED)
    response = urequests.post("http://192.168.1.162:5000/api/v1/users/", data=get_data())
    pycom.rgbled(GREEN)
    print(response)
    time.sleep(2)
    pycom.rgbled(YELLOW)