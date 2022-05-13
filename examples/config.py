""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FEFE" + WIFI_MAC[6:12]

# for US915
LORA_FREQUENCY = 903900000
LORA_GW_DR = "SF7BW125"
LORA_NODE_DR = 3
