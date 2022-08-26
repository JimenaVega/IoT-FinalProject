import time
import json
import paho.mqtt.client as mqtt

broker = '192.168.1.6'
port = 1883
topic = "v1/devices/me/rpc/request/1"
# generate client ID with pub prefix randomly
client_id = 'hftE8awQVgB6j5NgOFMw'
username = 'hftE8awQVgB6j5NgOFMw'
password = ''
publish_msg = {"method": "getCurrentTime", "params": "{}"}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        result = client.publish(topic, json.dumps(publish_msg))
        client.subscribe("v1/devices/me/rpc/response/1")
    else:
        print("Failed to connect, return code %d\n", rc)
def on_message(client, userdata, msg):
    print(f"Message received [{msg.topic}]: {msg.payload}")
    time.sleep(5)
    client.publish(topic, json.dumps(publish_msg))
client = mqtt.Client(client_id) # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)
client.connect(broker, port)
client.loop_forever()  # Start networking daemon
