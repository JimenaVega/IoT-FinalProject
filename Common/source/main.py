from PycomClient import PysenseClient


SERVER_IP = "http://192.168.1.162"
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
print("setUnixtime")

# Optional
pysense.setRatesFromPycom(rates, RATES_ENDPOINT)
print("setRatesFromPycom")

# Get rates setted for this device from db 
#pysense.getRatesFromdb()

# Initialize collection of all data 
pysense.initTimers()

while True:
        # POST data to server
        sensorsData = pysense.getDataFromSensors()

        try:
            pysense.postData(DATA_ENDPOINT, sensorsData)   
        except:
            print("Pysense couldn't POST data to api")
