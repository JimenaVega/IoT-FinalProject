from PysenseClient import PysenseClient

SERVER_IP = "192.168.1.162"
SERVER_PORT = "5000"
NETWORK = 'LCD'
PASSWD = '1cdunc0rd0ba'
DATA_ENDPOINT = "/api/data/"
RATES_ENDPOINT = "/api/set_rates/"

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
pysense.connectToNetwork(NETWORK, PASSWD)
pysense.setServerToConnect(SERVER_IP, SERVER_PORT)
pysense.setRatesFromJSON(rates, RATES_ENDPOINT)

