from network import WLAN
import pycom
import machine
import urequests
import time
import utime
import ujson
from machine import Timer
from machine import RTC
from urequests import Response

SERVER_ADDRESS = "http://192.168.1.184" #pc alejo
# SERVER_ADDRESS = "http://192.168.1.162" #pc jime
SERVER_PORT = "5000"

ADDRESS = "http://192.168.1.6:8080/api/v1/hftE8awQVgB6j5NgOFMw/telemetry"
headers = {'Content-Type': 'application/json'}

RED = 0x7f0000
GREEN = 0x007f00
YELLOW = 0x7f7f00
ORANGE = 0xffa500
NO_COLOUR = 0x000000

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

# wlan.connect(ssid='LCD-IoT', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
wlan.connect(ssid='LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

unixtime = urequests.get(SERVER_ADDRESS + ":" + SERVER_PORT + "/api/unixtime/")

print("Unix Time: ", unixtime.json())
rtc = RTC()
rtc.now()
rtc.init(time.localtime(unixtime.json()['ts']))

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
    data_sensors['acceleration'] = pySensors.get_acceleration()
    # print("[{}]: Acceleration alarm every {} seconds.".format(int(chrono.read()), rates['acceleration_rate']))


def light_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(light_handler, rates['light_rate'], periodic=True)
    data_sensors['light'] = pySensors.get_light()
    # print("[{}]: Light alarm every {} seconds.".format(int(chrono.read()), rates['light_rate']))


def temperature_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(temperature_handler, rates['temperature_rate'], periodic=True)
    data_sensors['temperature'] = pySensors.get_temperature()*100
    # print("[{}]: Temperature alarm every {} seconds.".format(int(chrono.read()), rates['temperature_rate']))


def humidity_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(humidity_handler, rates['humidity_rate'], periodic=True)
    data_sensors['humidity'] = pySensors.get_humidity()*100
    # print("[{}]: Humidity alarm every {} seconds.".format(int(chrono.read()), rates['humidity_rate']))


def altitude_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(altitude_handler, rates['altitude_rate'], periodic=True)
    data_sensors['altitude'] = pySensors.get_altitude()*100
    # print("[{}]: Altitude alarm every {} seconds.".format(int(chrono.read()), rates['altitude_rate']))


def battery_voltage_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(battery_voltage_handler, rates['battery_voltage_rate'], periodic=True)
    data_sensors['battery_voltage'] = py.read_battery_voltage()*100
    # print("[{}]: Battery voltage alarm every {} seconds.".format(int(chrono.read()), rates['battery_voltage_rate']))


def roll_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(roll_handler, rates['roll_rate'], periodic=True)
    data_sensors['roll'] = pySensors.get_roll()*1000
    # print("[{}]: Roll alarm every {} seconds.".format(int(chrono.read()), rates['roll_rate']))


def pitch_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(pitch_handler, rates['pitch_rate'], periodic=True)
    data_sensors['pitch'] = pySensors.get_pitch()*1000
    # print("[{}]: Pitch alarm every {} seconds.".format(int(chrono.read()), rates['pitch_rate']))


chrono.start()

transmission_alarm      = Timer.Alarm(transmission_handler, rates['transmission_rate'], periodic=True)
acceleration_alarm      = Timer.Alarm(acceleration_handler, rates['acceleration_rate'], periodic=True)
light_alarm             = Timer.Alarm(light_handler, rates['light_rate'], periodic=True)
temperature_alarm       = Timer.Alarm(temperature_handler, rates['temperature_rate'], periodic=True)
humidity_rate           = Timer.Alarm(humidity_handler, rates['humidity_rate'], periodic=True)
altitude_alarm          = Timer.Alarm(altitude_handler, rates['altitude_rate'], periodic=True)
battery_voltage_alarm   = Timer.Alarm(battery_voltage_handler, rates['battery_voltage_rate'], periodic=True)
roll_alarm              = Timer.Alarm(roll_handler, rates['roll_rate'], periodic=True)
pitch_alarm             = Timer.Alarm(pitch_handler, rates['pitch_rate'], periodic=True)

alarm_sets = []

alarm_sets.append([transmission_alarm, transmission_handler, 'transmission_rate'])
alarm_sets.append([acceleration_alarm, acceleration_handler, 'acceleration_rate'])
alarm_sets.append([light_alarm, light_handler, 'light_rate'])
alarm_sets.append([temperature_alarm, temperature_handler, 'temperature_rate'])
alarm_sets.append([humidity_rate, humidity_handler, 'humidity_rate'])
alarm_sets.append([altitude_alarm, altitude_handler, 'altitude_rate'])
alarm_sets.append([battery_voltage_alarm, battery_voltage_handler, 'battery_voltage_rate'])
alarm_sets.append([roll_alarm, roll_handler, 'roll_rate'])
alarm_sets.append([pitch_alarm, pitch_handler, 'pitch_rate'])


def store_data(samples, interval):
    stored_data = {}
    for i in range(samples):
        time.sleep(interval)
        aux = dict()
        aux["ts"] = int(time.time()*1000)
        aux["values"] = data_sensors
        stored_data["{0}".format(i)] = aux

    json_stored_data = ujson.dumps(stored_data)

    return json_stored_data

def get_data():
    data = dict()
    data["ts"] = time.time()*1000
    data["values"] = data_sensors
    time.sleep(1)

    return ujson.dumps(data)

def post_method(address, raw_data):
    headers = {'Content-Type': 'application/json'}
    response = urequests.post(address, data=raw_data, headers=headers)

    return response


def get_rates(address):
    global rates
    response = urequests.get(address)
    new_rates = response.json()
    rates = new_rates

    return response


sent = 0

while True:
    try:
        get_response = get_rates(SERVER_ADDRESS + ":" + SERVER_PORT + "/api/rates/")
        get_response.close()
    except:
        print("GET attempt failed.")
    # stored_data = store_data(2, 5)
    data = get_data()

    # data = ujson.dumps({"temperature": 70+sent})
    # print(data)
    # response = urequests.post(ADDRESS, data=data, headers=headers)
    # response.close()

    try:
        # response = post_method(SERVER_ADDRESS + ":" + SERVER_PORT + "/api/data/", stored_data)
        response = urequests.post(ADDRESS, data=data, headers=headers)
        print(data)
        response.close()
    except:
        response = ''
        print("POST attempt failed.")

    sent += 1
    print("Packets sent: ", sent)