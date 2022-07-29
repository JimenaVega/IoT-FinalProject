import pycom
import machine
import urequests
import time
import ujson
import binascii

from network import WLAN
from machine import Timer
from machine import RTC
from urequests import Response
from const import RED, GREEN, BLUE, PYSCAN, PYSENSE, PYTRACK

# (ssid='LCD3', auth=(WLAN.WPA2, '1cdunc0rd0ba')

class PycomClient():
    self.MAC = None
    self.ssid = None
    self.psswd = None
    self.serverAdress = None
    self.PORT = None
    self.RGB = [RED, GREEN, BLUE]
    self.rates = None
    self.pycomType = None

    def _setMAC(self):
        self.MAC = binascii.hexlify(machine.unique_id())
    
    def setInitPycomConfig(self):
        pycom.heartbeat(False)
        
    def connectToNetwork(self, ssid, password):

        self._setMAC()

        self.ssid = ssid
        self.psswd = password

        wlan = WLAN(mode=WLAN.STA)
        wlan.connect(ssid=self.ssid, auth=(WLAN.WPA2, self.psswd))
        while not wlan.isconnected():
            machine.idle()
        print("WiFi connected succesfully")
        print(wlan.ifconfig())
    
    def configSensors(self, pycomType):
        self.pycomType = pycomType
        pyObject = None

        if(self.pycomType == PYSCAN):
            py = Pycoproc(Pycoproc.PYSCAN)
            pyObject = PyscanSensors(py)

        return pyObject
