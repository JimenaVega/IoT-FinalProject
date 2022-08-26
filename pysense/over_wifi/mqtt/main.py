import machine
import robust
import ujson
from network import WLAN

SERVER_ADDRESS = "192.168.1.6"

wlan = WLAN(mode=WLAN.STA)

wlan.antenna(WLAN.EXT_ANT)

wlan.connect(ssid='LCD', auth=(WLAN.WPA2, '1cdunc0rd0ba'))

while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

requestId = 1
request = {
    "method": "getCurrentTime",
    "params": "{}"
}

unixtime = 0

def subscribe_callback(topic, msg):
    print("Topic: {0} \t- Message: {1}".format(topic, msg))

mqtt = robust.MQTTClient("device1", SERVER_ADDRESS, user=b"hftE8awQVgB6j5NgOFMw", password=b"", keepalive=60)
mqtt.set_callback(subscribe_callback)
mqtt.connect(clean_session=False)

print("To publish: ", request)
p_response = mqtt.publish(topic=b"v1/devices/me/rpc/request/1", msg=ujson.dumps(request))
print("P_Response:", p_response)

s_response = mqtt.subscribe(topic=b"v1/devices/me/rpc/response/1")
print("S_Response:", s_response)

while 1:
    print("Testing...")