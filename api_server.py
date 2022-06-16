# Using flask to make an api
# import necessary libraries and functions
import time
from distutils.log import debug
from flask import Flask, jsonify, request, render_template
  
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
  
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data/', methods=['POST'])
def get_data():
    print('ENTRO')
    try:
        json = request.get_json(force=True)
        print(json)
    except:
        print('error handleado')

    return jsonify({'changes': 1})

@app.route('/api/unixtime/', methods=['GET']) 
def get_timestamp():
    unix_timestamp = int(time.time()) 
    print(unix_timestamp)
    
    return jsonify({"ts":unix_timestamp})

# Use with:
# curl -X POST -H "Content-Type: application/json" -d '{"transmission_rate":1}' http://192.168.1.162:5000/api/set_rates/#
@app.route('/api/set_rates/', methods=['POST'])
def set_rates():
    print('SET_RATES')
    rate_change = True
    print(rate_change)
    print('----------')
    try:
        json = request.get_json(force=False)
        print(json)
    except:
        print('error handleado')
    
    return jsonify({'changes': '1'})

@app.route('/api/rates/', methods=['GET'])
def get_rates():
    return jsonify(rates)


# driver function
if __name__ == '__main__':
  
    app.run(host='0.0.0.0',port=5000,debug=True)