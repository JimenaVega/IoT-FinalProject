from network import WLAN
from pysense import Pysense
from base import CreateSensors
import pycom
import machine
import urequests
import time
import utime
import ujson
from machine import Timer
from urequests import Response

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

rates = {
    'transmission_rate': 3,
    'acceleration_rate': 30,
    'light_rate': 30,
    'temperature_rate': 30,
    'humidity_rate': 30,
    'altitude_rate': 3,
    'battery_voltage_rate': 30,
    'roll_rate': 30,
    'pitch_rate': 30
}

def transmission_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(transmission_handler, rates['transmission_rate'], periodic=True)
    print("Transmission alarm every {} seconds.".format(rates['transmission_rate']))

transmission_alarm = Timer.Alarm(transmission_handler, rates['transmission_rate'], periodic=True)

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

def get_rates(address):
    response = urequests.get(address)
    new_rates = response.json()

    print("Old rates:\n",rates)

    rates['transmission_rate']      = new_rates['transmission_rate']
    rates['acceleration_rate']      = new_rates['acceleration_rate']
    rates['light_rate']             = new_rates['light_rate']
    rates['temperature_rate']       = new_rates['temperature_rate']
    rates['humidity_rate']          = new_rates['humidity_rate']
    rates['altitude_rate']          = new_rates['altitude_rate']
    rates['battery_voltage_rate']   = new_rates['battery_voltage_rate']
    rates['roll_rate']              = new_rates['roll_rate']
    rates['pitch_rate']             = new_rates['pitch_rate']
    
    print("New rates:\n",rates)

    return response

sent = 0

while True:
    get_response = get_rates("http://192.168.1.162:5000/api/rates/")
    pycom.rgbled(RED)
    stored_data = store_data(2, 5)
    print("Store data done")
    response = post_method("http://192.168.1.162:5000/api/v1/users/", stored_data)
    sent += 1
    blinking_sleep(3, GREEN)
    print("{0}:{1}".format(sent,response))
    blinking_sleep(3, YELLOW)