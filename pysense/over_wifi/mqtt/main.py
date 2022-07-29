from network import WLAN
from pysense import Pysense
from base import CreateSensors
import pycom
import machine
import time
import utime
import ujson
import simple
from machine import Timer
from machine import RTC

SERVER_ADDRESS = "192.168.1.6"

RED = 0x7f0000
GREEN = 0x007f00
YELLOW = 0x7f7f00
ORANGE = 0xffa500
NO_COLOUR = 0x000000

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LCD', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

mqtt = simple.MQTTClient("hftE8awQVgB6j5NgOFMw", SERVER_ADDRESS, user=b"hftE8awQVgB6j5NgOFMw", password=b"")
mqtt.connect()

unixtime = 1659109057

print("Unix Time: ", unixtime)
rtc = RTC()
rtc.now()
rtc.init(time.localtime(unixtime))

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


def acceleration_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(acceleration_handler, rates['acceleration_rate'], periodic=True)
    data_sensors['acceleration'] = pySensors.get_acceleration()


def light_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(light_handler, rates['light_rate'], periodic=True)
    data_sensors['light'] = pySensors.get_light()


def temperature_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(temperature_handler, rates['temperature_rate'], periodic=True)
    data_sensors['temperature'] = pySensors.get_temperature()*100


def humidity_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(humidity_handler, rates['humidity_rate'], periodic=True)
    data_sensors['humidity'] = pySensors.get_humidity()*100


def altitude_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(altitude_handler, rates['altitude_rate'], periodic=True)
    data_sensors['altitude'] = pySensors.get_altitude()*100


def battery_voltage_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(battery_voltage_handler, rates['battery_voltage_rate'], periodic=True)
    data_sensors['battery_voltage'] = py.read_battery_voltage()*100


def roll_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(roll_handler, rates['roll_rate'], periodic=True)
    data_sensors['roll'] = pySensors.get_roll()*1000


def pitch_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(pitch_handler, rates['pitch_rate'], periodic=True)
    data_sensors['pitch'] = pySensors.get_pitch()*1000


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


sent = 0

while True:

    data = get_data()
    mqtt.publish("v1/devices/me/telemetry", data)

    sent += 1
    print("Packets sent: ", sent)
    print(type(data))
    print(data)