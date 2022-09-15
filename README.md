# PycomExamples
Examples of python/micropython collected and used in pycom chips

## Consideraciones

### ThingsBoard
Corriendo una instancia local con Docker en la PC de Horacio.

IP: 192.168.1.6

Port: 8080

**Mosquitto Broker**

Corriendo en la PC de Horacio.

IP: 192.168.1.6

Port: 1884 (Previamente en 1883, se cambió porque TB utiliza también ese puerto, por lo que daba errores)

User: otros

Password: 1cdunc0rd0ba

Suscripción:

`mosquitto_sub -h host -p 1884 -u "user" -P "password" -t "topic"`


Publicación:

`mosquitto_pub -h host -p 1884 -u "user" -P "password" -m "message" -t "topic"`

host: localhost en caso de estar en la PC donde corre el server

---

## Posibles errores
**MQTT Micropython** (robust.py/simple.py)
1. MQTTException 5: Problema con las credenciales de autenticación por MQTT. ([Mismo problema](https://forum.micropython.org/viewtopic.php?t=4412))
2. Hay un bug en donde la placa no se conecta a la red de WiFi si no se desactiva el heartbeat. `pycom.heartbeat(False)`
