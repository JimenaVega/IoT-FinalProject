from PycomClient import PysenseClient


SERVER_API = "http://192.168.100.6:5000/api/unixtime/"
THINGSBOARD_ADDRESS = "http://192.168.100.6:8080/api/v1/gcv0VF7NiudY5qSEf3b4/telemetry"

SSID = "LCD"
PASSWD = "1cdunc0rd0ba"

# https://thingsboard.io/docs/reference/http-api/

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

# Create object
pysense = PysenseClient("Pedro")

# Connect to WIFI network
pysense.connectToNetwork(SSID, PASSWD)

# Gives unixtime to device
pysense.setUnixtime(SERVER_API)

# Sampling and sending default rates
pysense.setRatesInPycom(rates)

# Optional
pysense.setServerToConnect(THINGSBOARD_ADDRESS)
# Optional
# pysense.setRatesFromPycom(rates, RATES_ENDPOINT)
# print("setRatesFromPycom")
# Get rates setted for this device from db 
#pysense.getRatesFromdb()


# Initialize collection of all data 
pysense.initTimers()

# curl -v -X POST --data "{"ts": 1666912613000, "values": {"roll": -47.82048, "temperature": 3081.25, "pitch": -6148.442, "light": [11, 5], "humidity": 3788.046, "battery_voltage": 464.1541, "altitude": 44650.0, "acceleration": [0.002319336, 0.1120605, 1.016602]}}" http://192.168.100.6:8080/api/v1/gcv0VF7NiudY5qSEf3b4/telemetry --header "Content-Type:application/json"
# For example, $THINGSBOARD_HOST_NAME reference live demo server, $ACCESS_TOKEN is ABC123:

while True:
        # POST data to server
        sensorsData = pysense.getDataFromSensors()
        print("Sensors Data: \n", sensorsData)

        try:
            pysense.postData(THINGSBOARD_ADDRESS, sensorsData)   
        except:
            print("Pysense couldn't POST data to api")
