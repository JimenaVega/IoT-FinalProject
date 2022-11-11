from PycomClient import PysenseClient
FLASK_API_ADDRESS = "http://192.168.1.163:5000/api/unixtime/"
THINGSBOARD_ADDRESS = "http://192.168.1.163:8080/api/v1/"
TOKEN_ID = "k4xhQ85dcdrVWYeKuKMn"

SSID = "LCD"
PASSWD = "1cdunc0rd0ba"
#https://demo.thingsboard.io/api/v1/ABC123/attributes?clientKeys=attribute1,attribute2

rates = {
        'transmission_rate':10,
        'acceleration_rate':2,
        'light_rate':2,
        'temperature_rate':2,
        'humidity_rate':2,
        'altitude_rate':2,
        'battery_voltage_rate':5,
        'roll_rate':6,
        'pitch_rate':2
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

# curl -v -X POST --data "{"ts": 1666912613000, "values": {"roll": -47.82048, "temperature": 3081.25, "pitch": -6148.442, "light": [11, 5], "humidity": 3788.046, "battery_voltage": 464.1541, "altitude": 44650.0, "acceleration": [0.002319336, 0.1120605, 1.016602]}}" http://192.168.100.6:8080/api/v1/IxQPiSAH6gScQZ1KBjcY/telemetry --header "Content-Type:application/json"

# http://YOUR_HOST:PORT/swagger-ui.html
while True:

        sensorsData = pysense.getDataFromSensors()
        print("Sensors data: \n", sensorsData)

        try:
            pysense.postData(THINGSBOARD_ADDRESS + TOKEN_ID + "/telemetry", sensorsData)   
        except:
            print("Pysense couldn't POST data to api")
