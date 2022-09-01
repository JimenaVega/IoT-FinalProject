# pycomExamples
Examples of python/micropython collected and used in pycom chips

**Consideraciones**

**ThingsBoard**
Corriendo una instancia local con Docker en la PC de Horacio.
IP: 192.168.1.6
Port: 8080

**Mosquitto Broker**
Corriendo en la PC de Horacio.
Port: 1884 (Previamente en 1883, se cambió porque TB utiliza también ese puerto, por lo que daba errores)
User: otros
Password: 1cdunc0rd0ba

Suscripción: mosquitto_sub -h host(localhost en caso de estar en la PC donde corre el server) -p 1884 -u "user" -P "password" -t "topic"
Publicación: mosquitto_pub -h host(localhost en caso de estar en la PC donde corre el server) -p 1884 -u "user" -P "password" -m "message" -t "topic"

