
from MFRC630 import MFRC630
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from SI7006A20 import SI7006A20
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE
from L76GNSS import L76GNSS

from PycomClient import PycomClient
from machine import Timer
import time
#from pysense import Pysense
from pycoproc_1 import Pycoproc



class PysenseClient(PycomClient):

    def __init__(self, name):
        super().__init__(name)
        
        # self.pysense = Pysense()
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
        time.sleep_ms(5)
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
        alarm = Timer.Alarm(transmission_handler, self.rates['transmission_rate'], periodic=True)
        # print("[{}]: Transmission alarm every {} seconds.".format(int(chrono.read()), rates['transmission_rate']))


    def _acceleration_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(acceleration_handler, self.rates['acceleration_rate'], periodic=True)
        data_sensors['acceleration'] = self.get_acceleration()
        # print("[{}]: Acceleration alarm every {} seconds.".format(int(chrono.read()), rates['acceleration_rate']))


    def _light_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(light_handler, self.rates['light_rate'], periodic=True)
        data_sensors['light'] = self.get_light()
        # print("[{}]: Light alarm every {} seconds.".format(int(chrono.read()), rates['light_rate']))

    # VER SI ACEPTA DOBLE ARGUMENTO
    def _temperature_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(temperature_handler, self.rates['temperature_rate'], periodic=True)
        data_sensors['temperature'] = self.get_temperature()*100
        # print("[{}]: Temperature alarm every {} seconds.".format(int(chrono.read()), rates['temperature_rate']))


    def _humidity_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(humidity_handler, self.rates['humidity_rate'], periodic=True)
        data_sensors['humidity'] = self.get_humidity()*100
        # print("[{}]: Humidity alarm every {} seconds.".format(int(chrono.read()), rates['humidity_rate']))


    def _altitude_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(altitude_handler, self.rates['altitude_rate'], periodic=True)
        data_sensors['altitude'] = self.get_altitude()*100
        # print("[{}]: Altitude alarm every {} seconds.".format(int(chrono.read()), rates['altitude_rate']))


    def _battery_voltage_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(battery_voltage_handler,  self.rates['battery_voltage_rate'], periodic=True)
        data_sensors['battery_voltage'] = py.read_battery_voltage()*100
        # print("[{}]: Battery voltage alarm every {} seconds.".format(int(chrono.read()), rates['battery_voltage_rate']))


    def _roll_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(roll_handler,  self.rates['roll_rate'], periodic=True)
        data_sensors['roll'] = pySensors.get_roll()*1000
        # print("[{}]: Roll alarm every {} seconds.".format(int(chrono.read()), rates['roll_rate']))


    def _pitch_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(pitch_handler, rates['pitch_rate'], periodic=True)
        data_sensors['pitch'] = pySensors.get_pitch()*1000
        # print("[{}]: Pitch alarm every {} seconds.".format(int(chrono.read()), rates['pitch_rate']))
        
    