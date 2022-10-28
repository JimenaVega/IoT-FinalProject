import pycom
import machine
import urequests
import time
import ujson
import binascii

from network import WLAN
from machine import Timer
from machine import RTC
from const import RED, GREEN, BLUE, PYSCAN, PYSENSE, PYTRACK

from MFRC630 import MFRC630
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from SI7006A20 import SI7006A20
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE
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
        headers = {'Content-Type': 'application/json'}

        response = urequests.post(address, data=raw_data, headers=headers)
        print(response)
        response.close()
        return response
    
    # def _configSensors(self):
    #     pyObject = None

    #     if(self.pycomType == PYSCAN):
    #         py = Pycoproc(Pycoproc.PYSCAN)
    #         pyObject = PyscanSensors(py)
    #     elif(self.pycomType == PYSENSE):
    #         py = Pysense()
    #         pyObject = PysenseSensors(py)
    #     elif(self.pycomType == PYTRACK):
    #         py = Pycoproc(Pycoproc.PYTRACK)
    #         pyObject = PytrackSensors(py)

    #     return pyObject
    
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
    

class PysenseClient(PycomClient):

    def __init__(self, name):
        super().__init__(name)
        
        #self.pysense = Pysense()
        self.pysense = Pycoproc(Pycoproc.PYSENSE)
        self.sensors = dict()
        print("Se creo el pysense: ", name)
        
        self.sensors["light"]=LTR329ALS01(self.pysense)
        self.sensors["humidity"]=SI7006A20(self.pysense)
        self.sensors["altitude"]=MPL3115A2(self.pysense,mode=ALTITUDE)
        self.sensors["acceleration"]=LIS2HH12(self.pysense)
        
        self.chrono = Timer.Chrono()
        
    def get_acceleration(self):
        # Return a tuple of three elements
        return self.sensors["acceleration"].acceleration()

    def get_pitch(self):
        return self.sensors["acceleration"].pitch()

    def get_roll(self):
        return self.sensors["acceleration"].roll()

    def get_humidity(self):
        return self.sensors["humidity"].humidity()

    def get_light(self):
        # Return a tuple of two elements
        return self.sensors["light"].light()

    def get_altitude(self):
        return self.sensors["altitude"].altitude()

    def get_temperature(self):
        # The Sensor that return the temperature is the same of Altitude one
        return self.sensors["altitude"].temperature()
        
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

    # VER SI ACEPTA DOBLE ARGUMENTO
    def _temperature_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._temperature_handler, self.rates['temperature_rate'], periodic=True)
        self.data_sensors['temperature'] = self.get_temperature() * 100
        # print("[{}]: Temperature alarm every {} seconds.".format(int(chrono.read()), rates['temperature_rate']))


    def _humidity_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._humidity_handler, self.rates['humidity_rate'], periodic=True)
        self.data_sensors['humidity'] = self.get_humidity() * 100
        # print("[{}]: Humidity alarm every {} seconds.".format(int(chrono.read()), rates['humidity_rate']))


    def _altitude_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._altitude_handler, self.rates['altitude_rate'], periodic=True)
        self.data_sensors['altitude'] = self.get_altitude() * 100
        # print("[{}]: Altitude alarm every {} seconds.".format(int(chrono.read()), rates['altitude_rate']))


    def _battery_voltage_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._battery_voltage_handler,  self.rates['battery_voltage_rate'], periodic=True)
        self.data_sensors['battery_voltage'] = self.pysense.read_battery_voltage() * 100
        # print("[{}]: Battery voltage alarm every {} seconds.".format(int(chrono.read()), rates['battery_voltage_rate']))


    def _roll_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._roll_handler,  self.rates['roll_rate'], periodic=True)
        self.data_sensors['roll'] = self.get_roll() * 1000
        # print("[{}]: Roll alarm every {} seconds.".format(int(chrono.read()), rates['roll_rate']))


    def _pitch_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self._pitch_handler, self.rates['pitch_rate'], periodic=True)
        self.data_sensors['pitch'] = self.get_pitch() * 1000
        # print("[{}]: Pitch alarm every {} seconds.".format(int(chrono.read()), rates['pitch_rate']))
    
    def initTimers(self):
        transmission_alarm      = Timer.Alarm(self._transmission_handler, self.rates['transmission_rate'], periodic=True)
        acceleration_alarm      = Timer.Alarm(self._acceleration_handler, self.rates['acceleration_rate'], periodic=True)
        light_alarm             = Timer.Alarm(self._light_handler, self.rates['light_rate'], periodic=True)
        temperature_alarm       = Timer.Alarm(self._temperature_handler, self.rates['temperature_rate'], periodic=True)
        humidity_rate           = Timer.Alarm(self._humidity_handler, self.rates['humidity_rate'], periodic=True)
        altitude_alarm          = Timer.Alarm(self._altitude_handler, self.rates['altitude_rate'], periodic=True)
        battery_voltage_alarm   = Timer.Alarm(self._battery_voltage_handler, self.rates['battery_voltage_rate'], periodic=True)
        roll_alarm              = Timer.Alarm(self._roll_handler, self.rates['roll_rate'], periodic=True)
        pitch_alarm             = Timer.Alarm(self._pitch_handler, self.rates['pitch_rate'], periodic=True)

        print("Init timers DONE ")
        # alarm_sets = []

        # alarm_sets.append([transmission_alarm, self._transmission_handler, 'transmission_rate'])
        # alarm_sets.append([acceleration_alarm, self._acceleration_handler, 'acceleration_rate'])
        # alarm_sets.append([light_alarm, self._light_handler, 'light_rate'])
        # alarm_sets.append([temperature_alarm, self._temperature_handler, 'temperature_rate'])
        # alarm_sets.append([humidity_rate, self._humidity_handler, 'humidity_rate'])
        # alarm_sets.append([altitude_alarm, self._altitude_handler, 'altitude_rate'])
        # alarm_sets.append([battery_voltage_alarm, self._battery_voltage_handler, 'battery_voltage_rate'])
        # alarm_sets.append([roll_alarm, self._roll_handler, 'roll_rate'])
        # alarm_sets.append([pitch_alarm, self._pitch_handler, 'pitch_rate'])

