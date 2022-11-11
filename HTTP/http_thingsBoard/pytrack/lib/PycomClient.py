import pycom
import machine
import urequests
import time
import ujson
import binascii

from network import WLAN
from machine import Timer
from machine import RTC
from const import RED, GREEN, BLUE

from L76GNSS import L76GNSS

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
    

class PytrackClient(PycomClient):

    def __init__(self, name):
        super().__init__(name)
        
        self.pytrack = Pycoproc(Pycoproc.PYTRACK)
        self.sensors = dict()
        print("Se creo el pytrack: ", name)
        
        self.sensors["coordinates"]=L76GNSS(self.pytrack)

        self.chrono = Timer.Chrono()

    def get_coordinates(self):
        return self.sensors["coordinates"].coordinates()

        
    def _transmission_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._transmission_handler, self.rates['transmission_rate'], periodic=True)
        # print("[{}]: Transmission alarm every {} seconds.".format(int(chrono.read()), rates['transmission_rate']))

    def _coordinates_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._coordinates_handler, self.rates['coordinates'], periodic=True)
        self.data_sensors['coordinates'] = self.get_coordinates()

    def _battery_voltage_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._battery_voltage_handler,  self.rates['battery_voltage_rate'], periodic=True)
        self.data_sensors['battery_voltage'] = self.pytrack.read_battery_voltage() * 100
        # print("[{}]: Battery voltage alarm every {} seconds.".format(int(chrono.read()), rates['battery_voltage_rate']))


    def initTimers(self):
        transmission_alarm      = Timer.Alarm(self._transmission_handler, self.rates['transmission_rate'], periodic=True)
        coordinates             = Timer.Alarm(self._coordinates_handler, self.rates['coordinates_rate'], periodic=True)
        battery_voltage_alarm   = Timer.Alarm(self._battery_voltage_handler, self.rates['battery_voltage_rate'], periodic=True)
       
        print("Init timers DONE ")
       
