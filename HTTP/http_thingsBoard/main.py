from PycomClient import PysenseClient
FLASK_API_ADDRESS = "http://192.168.1.163:5000/api/unixtime/"
#THINGSBOARD_ADDRESS = "http://192.168.1.108:8080/api/v1/"
THINGSBOARD_ADDRESS = "http://192.168.1.163:8080/api/v1/"
TOKEN_ID = "k4xhQ85dcdrVWYeKuKMn" 
#TOKEN_ID = "sAJ20eaXKIBDjGzHaDj0"

#SERVER_API = "http://192.168.1.163:5000/api/unixtime/"
# THINGSBOARD_RPC = "http://192.168.1.163:8080/api/v1/k4xhQ85dcdrVWYeKuKMn/rpc"
# THINGSBOARD_ADDRESS = "http://192.168.1.163:8080/api/v1/k4xhQ85dcdrVWYeKuKMn/telemetry"

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
pysense.setUnixtime(THINGSBOARD_ADDRESS + TOKEN_ID + "/rpc")

# Sampling and sending default rates
pysense.setRatesInPycom(rates)

# Optional
pysense.setServerToConnect(THINGSBOARD_ADDRESS + TOKEN_ID + "/telemetry/")


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
