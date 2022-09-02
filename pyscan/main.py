'''
Simple Pyscan NFC / MiFare Classic Example
Copyright (c) 2019, Pycom Limited.
'''
# PYSCAN
from pycoproc_1 import Pycoproc
from MFRC630 import MFRC630
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01

#OTHER 
from network import WLAN
import machine
from machine import Timer
import binascii
import urequests
import ujson
import time
import pycom

RGB_BRIGHTNESS = 0x8

RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

SERVER_ADDRESS = 'http://192.168.100.6'
SERVER_PORT = ':5000'

SAMPLES = 2
INTERVAL = 5

MAC = binascii.hexlify(machine.unique_id())


SSID = "LCD"
PASSWD = "1cdunc0rd0ba"

pycom.heartbeat(False)
wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid=SSID, auth=(WLAN.WPA2, PASSWD))

while not wlan.isconnected():
    machine.idle()
    
unixtime = urequests.get(SERVER_ADDRESS + SERVER_PORT + "/api/unixtime/")

print("Unix Time: ", unixtime.json())
# rtc = RTC()
# rtc.now()
# rtc.init(time.localtime(unixtime.json()['ts'])


class CreateSensors:
    sensors = {}
    def __init__(self, py):
        self.sensors["acceleration"] = LIS2HH12(py)
        self.sensors["light"] = LTR329ALS01(py)
        # nfc = MFRC630(py)
    
    def get_acceleration(self):
        time.sleep_ms(5)
        return self.sensors['acceleration'].acceleration()

    def get_light(self):
        return self.sensors['light'].light()

py = Pycoproc(Pycoproc.PYSCAN)
pyscan = CreateSensors(py)

data_sensors = {
        'MAC':  MAC,
        'acceleration': pyscan.get_acceleration(),
        'light': pyscan.get_light()
}

# rates = {
#     'acceleration_rate':5,
#     'light_rate':5
# }

rates = {
    'transmission_rate': 5,
    'acceleration_rate': 5,
    'light_rate': 5,
    'temperature_rate': 5,
    'humidity_rate': 5,
    'altitude_rate': 5,
    'battery_voltage_rate': 5,
    'roll_rate': 5,
    'pitch_rate': 5
}


chrono = Timer.Chrono()

def transmission_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(transmission_handler, rates['transmission_rate'], periodic=True)
    # print("[{}]: Transmission alarm every {} seconds.".format(int(chrono.read()), rates['transmission_rate']))

def acceleration_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(acceleration_handler, rates['acceleration_rate'], periodic=True)
    data_sensors['acceleration'] = pyscan.get_acceleration()

def light_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(light_handler, rates['light_rate'], periodic=True)
    data_sensors['light'] = pyscan.get_light()

chrono.start()
transmission_alarm      = Timer.Alarm(transmission_handler, rates['transmission_rate'], periodic=True)
acceleration_alarm      = Timer.Alarm(acceleration_handler, rates['acceleration_rate'], periodic=True)
light_alarm             = Timer.Alarm(light_handler, rates['light_rate'], periodic=True)

# def get_init_config(address):
#     response = urequests.get(address)
#     new_config =

def get_rates(address):
    global rates
    print(address)
    response = urequests.get(address)
    new_rates = response.json()
    print('NEW RATES ARE:')
    print(new_rates)
    rates = new_rates

    return response

print("WiFi connected succesfully")
print(wlan.ifconfig())


def get_data():
    data_sensors = {
        'MAC': MAC,
        'acceleration': pyscan.acceleration(),
        'light': pyscan.light()
    }
    json_data_sensors = ujson.dumps(data_sensors)

    return json_data_sensors

def store_data(samples, interval):
    stored_data = {}
    for i in range(samples):
        time.sleep(interval)
        aux = dict()
        aux["ts"] = int(time.time())
        aux["values"] = data_sensors
        stored_data["{0}".format(i)] = aux

    json_stored_data = ujson.dumps(stored_data)

    return json_stored_data

def post_method(address, raw_data):
    headers = {'Content-Type': 'application/json'}
    response = urequests.post(address, data=raw_data, headers=headers)

    return response


sent = 0

while(1):
    print('PYSCAN IN WHILE')
    # print(data_sensors)
    try:
        get_response = get_rates(SERVER_ADDRESS + SERVER_PORT + "/api/rates/")
        print('SOY PYSCAN GET')
    except:
        print('GET attempt failed.')
    
    stored_data = store_data(SAMPLES,INTERVAL) # Stores every INTERVAL of time SAMPLES samples of sensor data
    # print('STORED_DATA')
    # print(stored_data)
    # try:
    #     response = post_method(SERVER_ADDRESS + SERVER_PORT + "/api/data/", stored_data)
    #     print('SOY PYSCAN POST')
    # except:
    #     response = ''
    #     print("POST attempt failed.")

    sent += 1
