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

SERVER_ADDRESS = "192.168.1.6"
DEVICE_ID = "23"

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.antenna(WLAN.EXT_ANT)

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

def subscribe_callback(topic, msg):
    global unixtime
    response = ujson.loads(msg.decode('utf-8'))

    if response["device_id"] == DEVICE_ID:
        unixtime = response["unixtime"]


mqtt = robust.MQTTClient("FP23", SERVER_ADDRESS, port=1883, user=b"FP23", password=b"23", keepalive=60)
mqtt.set_callback(subscribe_callback)
mqtt.connect(clean_session=False)

mqtt.subscribe(topic=b"v1/devices/me/rpc/response/+")

count = 0
while 1:
    mqtt.check_msg()
    print("To publish: ", request)
    p_response = mqtt.publish(topic=b"v1/devices/me/rpc/request/"+DEVICE_ID, msg=ujson.dumps(request))
    print("P_Response:", p_response)
    print("{0} seconds up...".format(count))
    time.sleep(2)
    count += 2
    print("unixtime: ", unixtime)