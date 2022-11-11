import pycom
import machine
import urequests
import time
import ujson
import binascii

from network import WLAN
from machine import Timer
from machine import RTC
from const import RED, GREEN, BLUE, PYSCAN, PYTRACK

from MFRC630 import MFRC630
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01

from machine import Timer
from pycoproc_1 import Pycoproc


class PycomClient:
    
    def __init__(self, name):
        self.name = name
        self.MAC = binascii.hexlify(machine.unique_id())
        self.ssid = None
        self.psswd = None
        self.serverURL = ""
        self.RGB = [RED, GREEN, BLUE]
        self.rates = None
        self.unixtime = None
        self.data_sensors = dict() # Datos de los sensores
        print("MAC ADDRESS: ", self.MAC)
       
    def connectToNetwork(self, ssid, password):
        # pycom.heartbeat(False)

        wlan = WLAN(mode=WLAN.STA)

        wlan.connect(ssid=ssid, auth=(WLAN.WPA2, password))

        while not wlan.isconnected():
                machine.idle()
        print("WiFi connected succesfully")
        print(wlan.ifconfig())
            
    def setServerToConnect(self, server):
        # Conexion con la API server
        self.serverURL = server
        
    def setUnixtime(self, address):
        """POST to RPC (remote procedure calls) of Thingsboard to get current unixtime
        Args:
            address (string): Thingsboard RPC url
        """

        try: 
            self.unixtime = urequests.post(address, 
                                           headers={'Content-Type': 'application/json'},
                                           data=ujson.dumps({"method": "getCurrentTime", "params": {"device_id": 0}}))
            print("unixtime: ", self.unixtime.json())
            
        except:
            print("Error requesting UNIXTIME from API.")

        
        rtc = RTC()
        rtc.now()
        rtc.init(time.localtime(int(self.unixtime.json()['unixtime']/1000)))
        self.unixtime.close()
    
        
    def getServerDirection(self):
        return self.serverURL
        

    def postData(self, address, raw_data):
        print("ADDRESS: ", address)
        headers = {'Content-Type': 'application/json'}

        response = urequests.post(address, data=raw_data, headers=headers)
        #server_response = response.json()
        #print(server_response)
        response.close()
        #return server_response
    
    #     elif(self.pycomType == PYTRACK):
    #         py = Pycoproc(Pycoproc.PYTRACK)
    #         pyObject = PytrackSensors(py)
    
    def setDeviceRatesFromApi(self, endpoint):
        # endpoint = "/api/rates/"
        response = urequests.get(self.serverAddress + ":" + self.PORT + endpoint ).json()
        self.rates = response.json()
    
    def setRatesInDB(self, rates, endpoint):
        """ Sets rates for every sensor into a mongo database

        Args:
            rates (_dictonary_): json dictonary with every sensors' sample rate and sending data rate
            endpoint (_string_): endpoint of the http api to send the new rates file
        """
        self.setRatesInPycom(rates)
        print("setRatesFromJSON")
        print(self.serverURL + endpoint)
        changes = self.postData(endpoint, self.rates)
        print(changes)

    def setRatesInPycom(self, rates):
        self.rates = rates
        print("Rates now are: ", self.rates)
    
    def getCurrentRates(self, endpoint):
        response = urequests.get(self.serverURL + endpoint)
        new_rates = response.json()
        print('NEW RATES ARE:')
        print(new_rates)
    
    def getUnixTimestamp(self):
        return self.unixtime

    def getDataFromSensors(self):
        data = dict()
        data["ts"] = time.time()*1000
        data["values"] = self.data_sensors
        time.sleep(1)

        return ujson.dumps(data)
    

class PyscanClient(PycomClient):

    def __init__(self, name):
        super().__init__(name)
        
        self.pyscan = Pycoproc(Pycoproc.PYSCAN)
        self.sensors = dict()
        print("Se creo el pyscan: ", name)
        
        self.sensors["light"]=LTR329ALS01(self.pyscan)
        self.sensors["acceleration"]=LIS2HH12(self.pyscan)
        self.sensors["nfc"] = MFRC630(self.pyscan)
        
        self.chrono = Timer.Chrono()
        
    def get_acceleration(self):
        # Return a tuple of three elements
        return self.sensors["acceleration"].acceleration()

    def get_light(self):
        # Return a tuple of two elements
        return self.sensors["light"].light()
        
    def _transmission_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._transmission_handler, self.rates['transmission_rate'], periodic=True)
        # print("[{}]: Transmission alarm every {} seconds.".format(int(chrono.read()), rates['transmission_rate']))


    def _acceleration_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._acceleration_handler, self.rates['acceleration_rate'], periodic=True)
        self.data_sensors['acceleration'] = self.get_acceleration()
        # print("[{}]: Acceleration alarm every {} seconds.".format(int(chrono.read()), rates['acceleration_rate']))


    def _light_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._light_handler, self.rates['light_rate'], periodic=True)
        self.data_sensors['light'] = self.get_light()
        # print("[{}]: Light alarm every {} seconds.".format(int(chrono.read()), rates['light_rate']))


    def _battery_voltage_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._battery_voltage_handler,  self.rates['battery_voltage_rate'], periodic=True)
        self.data_sensors['battery_voltage'] = self.pyscan.read_battery_voltage() * 100
        # print("[{}]: Battery voltage alarm every {} seconds.".format(int(chrono.read()), rates['battery_voltage_rate']))


    
    def initTimers(self):
        transmission_alarm      = Timer.Alarm(self._transmission_handler, self.rates['transmission_rate'], periodic=True)
        acceleration_alarm      = Timer.Alarm(self._acceleration_handler, self.rates['acceleration_rate'], periodic=True)
        light_alarm             = Timer.Alarm(self._light_handler, self.rates['light_rate'], periodic=True)
        battery_voltage_alarm   = Timer.Alarm(self._battery_voltage_handler, self.rates['battery_voltage_rate'], periodic=True)
       
        print("Init timers DONE ")
       
