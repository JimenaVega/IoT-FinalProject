# Using flask to make an api
# import necessary libraries and functions
import time
from distutils.log import debug
from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient

from bson.json_util import dumps

# creating a Flask app
app = Flask(__name__)

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

client = MongoClient('localhost', 27017)
db = client.flask_db
# create a collection 
pycom = db.pycom
  
@app.route('/', methods=('GET', 'POST'))
def index():

    if request.method=='POST':
        mac_address = request.form['MAC']
        transmission_rate = request.form['transmission']
        acc_rate = request.form['acc_rate']
        light_rate = request.form['light_rate']
        temp_rate = request.form['temp_rate']
        hum_rate = request.form['hum_rate']
        alt_rate = request.form['alt_rate']
        roll_rate = request.form['roll_rate']
        pitch_rate = request.form['pitch_rate']
        degree = request.form['degree']
        pycom.insert_one({
                          'mac_address':mac_address,
                          'transmission_rate':transmission_rate,
                          'acceleration_rate':acc_rate,
                          'light_rate':light_rate,
                          'temperature_rate':temp_rate,
                          'humidity_rate':hum_rate,
                          'altitude_rate':alt_rate,
                          'roll_rate':roll_rate,
                          'pitch_rate':pitch_rate,
                          'degree': degree})
        return redirect(url_for('index'))

    all_pycom = pycom.find()
    return render_template('index.html', pycom=all_pycom)

# API receives data from pycom devices
# As an answer it sends back the last frequencies' document from mongodb
@app.route('/api/data/', methods=['POST'])
def get_data():
    
    try:
        json = request.get_json(force=True)
        print(json)
    except:
        print('error handleado')

    cursor = pycom.find().limit(1).sort([('$natural',-1)])
   
    return dumps(cursor)

# In the first connection with the pycom device the API sends back the unix timestamp
@app.route('/api/unixtime/', methods=['GET']) 
def get_timestamp():
    unix_timestamp = int(time.time()) 
    print('UNIX')
    print(unix_timestamp)

    return jsonify({"ts":unix_timestamp})

# Rates can also be configurated through this api method
# curl -X POST -H "Content-Type: application/json" -d '{"transmission_rate":1}' http://192.168.1.162:5000/api/set_rates/#
@app.route('/api/set_rates/', methods=['POST'])
def set_rates():
    try:
        json = request.get_json(force=False)
        print(json)
    except:
        print('error handleado')
    
    return jsonify({'changes': '1'})

@app.route('/api/rates/', methods=['GET'])
def get_rates():
    return jsonify(rates)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)