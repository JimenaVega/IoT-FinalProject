# from pyrsistent import s
from network import WLAN
from pysense import Pysense
from base import CreateSensors
import pycom
import machine
import time
import utime
import ujson
import robust
from machine import Timer
from machine import RTC

DEVICE_ID = "23"
SERVER_ADDRESS = "192.168.1.108"

RPC_REQUEST_TOPIC = "v1/devices/me/rpc/request/"
RPC_RESPONSE_TOPIC = "v1/devices/me/rpc/response/"

RED = 0x7f0000
GREEN = 0x007f00
YELLOW = 0x7f7f00
ORANGE = 0xffa500
NO_COLOUR = 0x000000

LED_STATE = False

def switch_led():
    global LED_STATE

    if LED_STATE:
        pycom.rgbled(0x000000)
        LED_STATE = False
    elif not LED_STATE:
        pycom.rgbled(0x330033)
        LED_STATE = True

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LCD', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

request = {
    "method": "getCurrentTime",
    "params": {"device_id": DEVICE_ID}
}

unixtime = 0

rates = {
    'transmission_rate': 3,
    'acceleration_rate': 5,
    'light_rate': 6,
    'temperature_rate': 5,
    'humidity_rate': 5,
    'altitude_rate': 5,
    'battery_voltage_rate': 5,
    'roll_rate': 5,
    'pitch_rate': 5
}

def subscribe_callback(topic, msg):
    global unixtime

    response = ujson.loads(msg.decode('utf-8'))
    request_id = str(topic[len(RPC_REQUEST_TOPIC):len(topic)], 'utf-8')

    if RPC_RESPONSE_TOPIC in topic:
        if response["device_id"] == DEVICE_ID:
            unixtime = response["unixtime"]
    elif RPC_REQUEST_TOPIC in topic:
        method = response["method"]

        if method == "switch_led":
            switch_led()
        elif method.startswith("set_"):
            if method.endswith("transmission_rate"):
                rates['transmission_rate'] = response["params"]
            elif method.endswith("acceleration_rate"):
                rates['acceleration_rate'] = response["params"]
            elif method.endswith("light_rate"):
                rates['light_rate'] = response["params"]
            elif method.endswith("temperature_rate"):
                rates['temperature_rate'] = response["params"]
            elif method.endswith("humidity_rate"):
                rates['humidity_rate'] = response["params"]
            elif method.endswith("altitude_rate"):
                rates['altitude_rate'] = response["params"]
            elif method.endswith("battery_voltage_rate"):
                rates['battery_voltage_rate'] = response["params"]
            elif method.endswith("roll_rate"):
                rates['roll_rate'] = response["params"]
            elif method.endswith("pitch_rate"):
                rates['pitch_rate'] = response["params"]
            
        elif method.startswith("get_"):
            if method.endswith("transmission_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['transmission_rate']))
            elif method.endswith("acceleration_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['acceleration_rate']))
            elif method.endswith("light_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['light_rate']))
            elif method.endswith("temperature_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['temperature_rate']))
            elif method.endswith("humidity_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['humidity_rate']))
            elif method.endswith("altitude_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['altitude_rate']))
            elif method.endswith("battery_voltage_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['battery_voltage_rate']))
            elif method.endswith("roll_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['roll_rate']))
            elif method.endswith("pitch_rate"):
                mqtt.publish(topic=RPC_RESPONSE_TOPIC+request_id, msg=ujson.dumps(rates['pitch_rate']))


mqtt = robust.MQTTClient("FP23", SERVER_ADDRESS, port=1883, user=b"FP23", password=b"23", keepalive=60)
mqtt.set_callback(subscribe_callback)
mqtt.connect(clean_session=False)

mqtt.subscribe(topic=b"v1/devices/me/rpc/response/+")
mqtt.subscribe(topic=b"v1/devices/me/rpc/request/+")
unixtime_request = mqtt.publish(topic=b"v1/devices/me/rpc/request/"+DEVICE_ID, msg=ujson.dumps(request))

mqtt.wait_msg()

print("TYPE: ", type(time.localtime(int(unixtime/1000))))
print("LOCALTIME: ", time.localtime(int(unixtime/1000)))

rtc = RTC()
rtc.now()
rtc.init(time.localtime(int(unixtime/1000)))

# Pysense Object and sensors
py = Pysense()
pySensors = CreateSensors(py)

data_sensors = {
    'acceleration': pySensors.get_acceleration(),
    'blue_light': pySensors.get_light()[0],
    'red_light': pySensors.get_light()[1],
    'temperature': pySensors.get_temperature(),
    'humidity': pySensors.get_humidity(),
    'altitude': pySensors.get_altitude(),
    'battery_voltage': py.read_battery_voltage(),
    'roll': pySensors.get_roll(),
    'pitch': pySensors.get_pitch()
    }

chrono = Timer.Chrono()

def transmission_handler(alarm):
    alarm.cancel()
    data = get_data()
    mqtt.publish("v1/devices/me/telemetry", data)
    print("Transmission every {} seconds.".format(rates['transmission_rate']))
    alarm = Timer.Alarm(transmission_handler, rates['transmission_rate'], periodic=True)


def acceleration_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(acceleration_handler, rates['acceleration_rate'], periodic=True)
    data_sensors['acceleration'] = pySensors.get_acceleration()


def light_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(light_handler, rates['light_rate'], periodic=True)
    data_sensors['blue_light'] = pySensors.get_light()[0]
    data_sensors['red_light'] = pySensors.get_light()[1]


def temperature_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(temperature_handler, rates['temperature_rate'], periodic=True)
    data_sensors['temperature'] = pySensors.get_temperature()


def humidity_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(humidity_handler, rates['humidity_rate'], periodic=True)
    data_sensors['humidity'] = pySensors.get_humidity()


def altitude_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(altitude_handler, rates['altitude_rate'], periodic=True)
    data_sensors['altitude'] = pySensors.get_altitude()


def battery_voltage_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(battery_voltage_handler, rates['battery_voltage_rate'], periodic=True)
    data_sensors['battery_voltage'] = py.read_battery_voltage()


def roll_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(roll_handler, rates['roll_rate'], periodic=True)
    data_sensors['roll'] = pySensors.get_roll()


def pitch_handler(alarm):
    alarm.cancel()
    alarm = Timer.Alarm(pitch_handler, rates['pitch_rate'], periodic=True)
    data_sensors['pitch'] = pySensors.get_pitch()


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


while True:
    mqtt.check_msg()
    # data = get_data()
    # mqtt.publish("v1/devices/me/telemetry", data)
    # print("Transmission every {} seconds.".format(rates['transmission_rate']))