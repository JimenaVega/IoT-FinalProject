
from MFRC630 import MFRC630
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from SI7006A20 import SI7006A20
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE
from L76GNSS import L76GNSS


class PyscanSensors:
    sensors = {}
    def __init__(self, py):
        self.sensors["acceleration"] = LIS2HH12(py)
        self.sensors["light"] = LTR329ALS01(py)
        # nfc = MFRC630(py)
    
    def get_acceleration(self):
        time.sleep_ms(5)
        return self.sensors['acceleration'].acceleration()

    def get_light(self):
        return self.sensors['light'].light()

class PysenseSensors:
    sensors = {}
    def __init__(self, pysense):
        self.sensors["light"]=LTR329ALS01(pysense)
        self.sensors["humidity"]=SI7006A20(pysense)
        self.sensors["altitude"]=MPL3115A2(pysense,mode=ALTITUDE)
        self.sensors["acceleration"]=LIS2HH12(pysense)

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

    def __del__(self):
        print ("object deleted")


class PytrackSensors:
    sensors = {}
    def __init__(self,pytrack):
        self.sensors["position"]=L76GNSS(pytrack)

    def get_position(self):
        return self.sensors["position"]

    def __del__(self):
        print("Object deleted")