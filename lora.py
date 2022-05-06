from network import LoRa
import socket
import ubinascii
import struct

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an ABP authentication params
dev_addr = struct.unpack(">l", ubinascii.unhexlify('260C8CAC'))[0]
nwk_swkey = ubinascii.unhexlify('7CF285486B09839C2B7E40D719A56FF1')
app_swkey = ubinascii.unhexlify('2A4AC8439992C5AF1953D39203304FBC')

# # Uncomment for US915 / AU915 & Pygate
# for i in range(0,8):
#     lora.remove_channel(i)
# for i in range(16,65):
#     lora.remove_channel(i)
# for i in range(66,72):
#     lora.remove_channel(i)

# join a network using ABP (Activation By Personalisation)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

print("joined? = ", lora.has_joined())

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# make the socket non-blocking
#s.setblocking(False)

# send some data
#s.send(bytes([0x01, 0x02, 0x07]))
s.send('Hello')

s.settimeout(5.5)


# get any data received...
data = s.recv(64)
print(data)