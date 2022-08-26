from pycomClient import pycomClient
from const import PYSCAN
from machine import Timer

class pysenseClient(pycomClient):

    def __init__(self, name):
        super().__init__(name)
        self.pyObject = super()._configSensors(PYSCAN)

    def transmission_handler(alarm):
        alarm.cancel()
        alarm = Timer.Alarm(transmission_handler, self.rates['transmission_rate'], periodic=True)
        # print("[{}]: Transmission alarm every {} seconds.".format(int(chrono.read()), rates['transmission_rate']))


    def acceleration_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self.acceleration_handler, self.rates['acceleration_rate'], periodic=True)
        data_sensors['acceleration'] = self.pyObject.get_acceleration()
        # print("[{}]: Acceleration alarm every {} seconds.".format(int(chrono.read()), rates['acceleration_rate']))


    def light_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self.light_handler, self.rates['light_rate'], periodic=True)
        data_sensors['light'] = self.pyObject.get_light()
        # print("[{}]: Light alarm every {} seconds.".format(int(chrono.read()), rates['light_rate']))


    def temperature_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self.temperature_handler, self.rates['temperature_rate'], periodic=True)
        data_sensors['temperature'] = self.pySensors.get_temperature()*100
        # print("[{}]: Temperature alarm every {} seconds.".format(int(chrono.read()), rates['temperature_rate']))


    def humidity_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self.humidity_handler, self.rates['humidity_rate'], periodic=True)
        data_sensors['humidity'] = pySensors.get_humidity()*100
        # print("[{}]: Humidity alarm every {} seconds.".format(int(chrono.read()), rates['humidity_rate']))


    def altitude_handler(self, alarm):
        alarm.cancel()
        alarm = Timer.Alarm(self.altitude_handler, self.rates['altitude_rate'], periodic=True)
        data_sensors['altitude'] = pySensors.get_altitude()*100
        # print("[{}]: Altitude alarm every {} seconds.".format(int(chrono.read()), rates['altitude_rate']))
        
    def setInitRates(self, json_rates)):
        # Cambios en todos los rates con un solo JSON

       headers = {'Content-Type': 'application/json'}
       response = urequests.post(self.serverAdress, data=json_rates, headers=headers)
       self.rates = json_rates # Validar 
                               # notar que esta variable puede ser modificada con getRatesFromApi de parent class
    
    # Se debe cambiar la API para que acepte cambios individuales de parametros
    # Se le debe colocar a cada documento JSON un id, probablemente la MAC de cada device

    def set_transmission_rate(self, rate):
        # API POST
        pass
    def set_acceleration_rate(self, rate):
        pass
    def set_light_rate(self, rate):
        pass
    def set_temperature_rate(self, rate):
        pass
    def set_humidity_rate(self, rate):
        pass
    def set_altitude_rate(self, rate):
