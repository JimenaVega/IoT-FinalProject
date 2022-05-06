# See https://docs.pycom.io for more information regarding library specifics

# Imports for LoraWan Node
from network import LoRa
import socket
import binascii
import ubinascii
import struct
import time
import config
import machine
import pycom
import struct
from pysense import Pysense
from base import CreateSensors

DEBUG = True
minutes = 5 # minutes that the device is sleeping

'''
    call back for handling RX packets
'''
def lora_cb(lora):
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        if lora_socket is not None:
            frame, port = lora_socket.recvfrom(512) # longuest frame is +-220
            if DEBUG == True:
                print("Received Data = Port {}, Data {}".format(port,frame))
    if events & LoRa.TX_PACKET_EVENT:
        if DEBUG == True:
            print("Tx Time on Air: {} ms @dr {}".format(lora.stats().tx_time_on_air, lora.stats().sftx))
    if events & LoRa.TX_FAILED_EVENT:
        if DEBUG == True:
            print("Your message sending has failed")

# initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)
lora.callback(trigger=( LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT |
                    LoRa.TX_FAILED_EVENT  ), handler=lora_cb)

# create a configure LoRa socket
lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_socket.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# create an ABP authentication params
dev_addr = struct.unpack(">l", ubinascii.unhexlify('260C8CAC'))[0]
app_swkey = ubinascii.unhexlify('2A4AC8439992C5AF1953D39203304FBC')
nwk_swkey = ubinascii.unhexlify('7CF285486B09839C2B7E40D719A56FF1')

def prepare_channels():
    for i in range(0,8):
        lora.remove_channel(i)
    for i in range(16,65):
        lora.remove_channel(i)
    for i in range(66,72):
        lora.remove_channel(i)

    # remove all the channels
#    for channel in range(0, 72):
#        lora.remove_channel(channel)

#    # set all channels to the same frequency (must be before sending the OTAA join request)
#    for channel in range(0, 72):
#        lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)

def join_lora():
    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

def go_to_deep_sleep(pySense, minutes):
    if DEBUG == True:
        print("I'm going to sleep for {} minutes, bye bye !".format(minutes))

    # Save the LoRa Information
    lora.nvram_save()
    # Deep Sleep
    pySense.setup_sleep(minutes*60)
    pySense.go_to_sleep()

def send_data():
    # Pysense Object and sensors
    py = Pysense()
    pySensors = CreateSensors(py)
    # Set Socket Timeout, will try to deliver the full message in that time
    lora_socket.settimeout(10)
    payload = b''
    acceleration=pySensors.get_acceleration()
    light= pySensors.get_light()

    payload += int(pySensors.get_temperature()*100).to_bytes(2,'little',True)
    payload += int(pySensors.get_humidity()*100).to_bytes(2,'little')
    payload += int(pySensors.get_altitude()*100).to_bytes(2,'little',True)
    payload += int(py.read_battery_voltage()*100).to_bytes(2,'little')

    for i in range(3):
        payload += int(acceleration[i]*1000).to_bytes(2,'little',True)

    payload += int(pySensors.get_roll()*1000).to_bytes(2,'little', True)
    payload += int(pySensors.get_pitch()*1000).to_bytes(2,'little', True)

    for i in range(2):
        payload += int(light[i]*100).to_bytes(2,'little')  # Channel Blue

    print(binascii.hexlify(payload))
    print('Sending: ')

    lora_socket.send(payload)
    # Release the socket
    lora_socket.setblocking(False)

    # Wait 8 seconds (worst case) to check if some information is Received
    start = time.ticks_ms()
    while (time.ticks_diff(time.ticks_ms(), start) < 8000):
        machine.idle()
    go_to_deep_sleep(py, minutes)

lora.nvram_restore()

# to know if they are alive
for cycles in range(10): # stop after 10 cycles
    pycom.rgbled(0x007f00) # green
    time.sleep_ms(50)
    pycom.rgbled(0x000000) # off
    time.sleep_ms(50)  #

if (lora.has_joined()):
    print("already joined")
    prepare_channels()
    send_data()
else:
    print("joining by ABP")
    prepare_channels()
    join_lora()
    send_data()
