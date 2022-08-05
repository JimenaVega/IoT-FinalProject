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
from Sensors import PyscanSensors, PysenseSensors, PytrackSensors
from pysense import Pysense
from pycoproc_1 import Pycoproc


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
    self.unixtime = None
    self.data = None
    
    def setInitPycomConfig(self, server, port):
        self.serverAddress = server # validar
        self.PORT = port    #validar
        self.unixtime = urequests.get(self.serverAddress + ":" + self.PORT)
        print("Unix Time: ",self.unixtime.json())
        rtc = RTC()
        rtc.now()
        rtc.init(time.localtime(self.unixtime.json()['ts']))

    def _setMAC(self):
        self.MAC = binascii.hexlify(machine.unique_id())  

    def connectToNetwork(self, ssid, password):
        pycom.heartbeat(False)
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
        elif(self.pycomType == PYSENSE):
            py = Pysense()
            pyObject = PysenseSensors(py)
        elif(self.pycomType == PYTRACK):
            py = Pycoproc(Pycoproc.PYTRACK)
            pyObject = PytrackSensors(py)

        return pyObject
    
    def setDeviceRatesFromApi(self, endpoint):
        # endpoint = "/api/rates/"
        self.rates = urequests.get(self.serverAddress + ":" + self.PORT + endpoint ).json()
    
    def getCurrentRates(self):
        return self.rates
    
    def getUnixTimestamp(self):
        return self.unixtime
    
