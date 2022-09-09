
from PycomClient import PysenseClient
import urequests


SERVER_IP = "http://192.168.100.6"
SERVER_PORT = "5000"

SSID = "LCD"
PASSWD = "1cdunc0rd0ba"

DATA_ENDPOINT = "/api/data/"
RATES_ENDPOINT = "/api/set_rates/"
TIME_ENDPOINT = "/api/unixtime/"

rates = {
        'transmission_rate':10,
        'acceleration_rate':10,
        'light_rate':10,
        'temperature_rate':10,
        'humidity_rate':10,
        'altitude_rate':10,
        'battery_voltage_rate':10,
        'roll_rate':10,
        'pitch_rate':10
        }

pysense = PysenseClient("Pedro")

pysense.connectToNetwork(SSID, PASSWD)


pysense.setServerToConnect(SERVER_IP, SERVER_PORT)
pysense.setUnixtime(TIME_ENDPOINT)


pysense.setRatesFromPycom(rates, RATES_ENDPOINT)
print("volvio")

# pysense.getCurrentRates()
# print("getCurrentRates")
