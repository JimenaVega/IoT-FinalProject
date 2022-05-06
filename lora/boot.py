import machine
from network import WLAN
from network import Server
from network import Bluetooth
from machine import UART
from network import LTE
import pycom
import time
import os

# SetUP Serial Debug
uart = UART(0,115200)
os.dupterm(uart)

if pycom.wifi_on_boot():
    print("wifi on boot was true")
    pycom.wifi_on_boot(False)
    wlan = WLAN()
    wlan.deinit()
else:
    print("wifi on boot was false")
if pycom.lte_modem_en_on_boot():
    print("lte on boot was true")
    pycom.lte_modem_en_on_boot(False)
    pycom.rgbled(0xff0000)
    lte = LTE()
    lte.attach()
    lte.deinit()
else:
    print("lte on boot was false")

# Switching off Heartbeat
pycom.heartbeat(False)
print ("disable heartbeat")

# Switching off Server
server = Server()
server.deinit()
print ("disable server")

if machine.reset_cause() in [machine.PWRON_RESET]:
    print('HARD PWRON')
    print('CLEAN NVS')
    pycom.nvs_erase_all()
    time.sleep_ms(5)
