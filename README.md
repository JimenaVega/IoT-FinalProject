<img src="./img/UNC.jpg" alt="drawing" width="100"/>


# Proyecto integrador final - 2022




## 🚩 Table of Contents

  - [📌 Project introduction](#-project-introduction)
  - [🎨 Features](#-features)
  
  - [🔧 Set up](#-set-up)
       - [Pre-requisits](#pre-requisits)
       - [HTTP server](#http-server)
       - [MQTT server](#mqtt-server)
  - [🐾 Usage example](#-examples)
  - [💬 Contributing](#-contributing)
  - [🚀 Referencer](#-references)
  - [📜 License](#-license)


## Project introduction
COMPLETAR


## 🎨 Features

COMPLETAR

## 🐾 Examples

COMPLETAR

* [Basic](https://nhn.github.io/tui.editor/latest/tutorial-example01-editor-basic)
* [Viewer](https://nhn.github.io/tui.editor/latest/tutorial-example04-viewer)
* [Using All Plugins](https://nhn.github.io/tui.editor/latest/tutorial-example12-editor-with-all-plugins)
* [Creating the User's Plugin](https://nhn.github.io/tui.editor/latest/tutorial-example13-creating-plugin)
* [Customizing the Toobar Buttons](https://nhn.github.io/tui.editor/latest/tutorial-example15-customizing-toolbar-buttons)
* [Internationalization (i18n)](https://nhn.github.io/tui.editor/latest/tutorial-example16-i18n)

Here are more [examples](https://nhn.github.io/tui.editor/latest/tutorial-example01-editor-basic) and play with TOAST UI Editor!



## 🔧 Setup

Fork `main` branch into your personal repository. Clone it to local computer. Install node modules. Before starting development, you should check if there are any errors.

### Pre-requisits
In Linux:
- Python 3 
- pip 3
- [mongoDB](#https://www.mongodb.com/try/download/community)

---
### HTTP server
1. Create environment:
   
```
mkdir environments
cd environments
python3 -m venv <env-name>
source activate <env-name>
source ~/environments/<env-name>/bin/activate 

```
Disable env: inside env
```
deactivate
```


2. Install flask and pymongo:
   
```
pip3 install Flask pymongo
```
3. Export environment variable:
```
export FLASK_APP=api_server.py
```
4. To change flask port:
```
export FLASK_RUN_PORT=<PORT_NUMBER>
```
5. Activate env and run server 
```
 flask run --host=0.0.0.0
 ```

> TOAST UI Editor uses [npm workspace](https://docs.npmjs.com/cli/v7/using-npm/workspaces/), so you need to set the environment based on [npm7](https://github.blog/2021-02-02-npm-7-is-now-generally-available/). If subversion is used, dependencies must be installed by moving direct paths per package.

--- 

### MQTT server



### ThingsBoard
Corriendo una instancia local con Docker en la PC de Horacio.

IP: 192.168.1.6

Port: 8080

**Mosquitto Broker**

Corriendo en la PC de Horacio.

IP: 192.168.1.108

Port: 1884 (Previamente en 1883, se cambió porque TB utiliza también ese puerto, por lo que daba errores)

User: otros

Password: 1cdunc0rd0ba

Suscripción:

`mosquitto_sub -h host -p 1884 -u "user" -P "password" -t "topic"`


Publicación:

`mosquitto_pub -h host -p 1884 -u "user" -P "password" -m "message" -t "topic"`

host: localhost en caso de estar en la PC donde corre el server

---


### Analizador de tráfico

**libpcap**

Documentation: ls
https://python-libpcap.readthedocs.io/en/latest/introduction.html#usage

## Posibles errores
**MQTT Micropython** (robust.py/simple.py)
1. MQTTException 5: Problema con las credenciales de autenticación por MQTT. ([Mismo problema](https://forum.micropython.org/viewtopic.php?t=4412))
2. Hay un bug en donde la placa no se conecta a la red de WiFi si no se desactiva el heartbeat. `pycom.heartbeat(False)`


## 🚀 References

* [Pycom documentarion](https://pycom.io/)



## 📜 License

This software is licensed under the [MIT](https://github.com/nhn/tui.editor/blob/master/LICENSE) © [NHN Cloud](https://github.com/nhn).
