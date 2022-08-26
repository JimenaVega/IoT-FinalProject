from PysenseClient import PysenseClient

SERVER_IP = "192.168.100.6"
SERVER_PORT = "5000"

pysense = PysenseClient("Pedro")
pysense.setServerToConnect(SERVER_IP, SERVER_PORT)
print("me cree xd")
