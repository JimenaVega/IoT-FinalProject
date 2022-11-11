from PycomClient import PytrackClient
FLASK_API_ADDRESS = "http://192.168.1.163:5000/api/unixtime/"
THINGSBOARD_ADDRESS = "http://192.168.1.163:8080/api/v1/"
TOKEN_ID = "eKFazljydZqNpOPv6uwy"

SSID = "LCD"
PASSWD = "1cdunc0rd0ba"


rates = {
        'transmission_rate':10,
        'coordinates_rate':2,
        'battery_voltage_rate': 2,
        }

# Create object
pytrack = PytrackClient("Pytrack_0")

# Connect to WIFI network
pytrack.connectToNetwork(SSID, PASSWD)

# Gives unixtime to device
pytrack.setUnixtime(THINGSBOARD_ADDRESS + TOKEN_ID + "/rpc")

# Sampling and sending default rates
pytrack.setRatesInPycom(rates)

# Optional
pytrack.setServerToConnect(THINGSBOARD_ADDRESS + TOKEN_ID + "/telemetry/")


# Initialize collection of all data 
pytrack.initTimers()

# curl -v -X POST --data "{"ts": 1666912613000, "values": {"roll": -47.82048, "temperature": 3081.25, "pitch": -6148.442, "light": [11, 5], "humidity": 3788.046, "battery_voltage": 464.1541, "altitude": 44650.0, "acceleration": [0.002319336, 0.1120605, 1.016602]}}" http://192.168.100.6:8080/api/v1/IxQPiSAH6gScQZ1KBjcY/telemetry --header "Content-Type:application/json"

# http://YOUR_HOST:PORT/swagger-ui.html
while True:

        sensorsData = pytrack.getDataFromSensors()
        print("Sensors data: \n", sensorsData)

        try:
            pytrack.postData(THINGSBOARD_ADDRESS + TOKEN_ID + "/telemetry", sensorsData)   
        except:
            print("Pysense couldn't POST data to api")
