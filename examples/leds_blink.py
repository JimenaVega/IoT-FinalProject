#ctrl+shift+g para abrir el json

from time import time
import pycom
import time

DELAY = 2

RED = 0x7f0000
GREEN = 0x007f00
YELLOW = 0x7f7f00

pycom.heartbeat(False)

for cycles in range(10):
    pycom.rgbled(RED)
    time.sleep(DELAY)
    
    pycom.rgbled(GREEN)
    time.sleep(DELAY)
    
    pycom.rgbled(YELLOW)
    time.sleep(DELAY)
    