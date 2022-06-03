# Using flask to make an api
# import necessary libraries and functions
import datetime
from distutils.log import debug
from flask import Flask, jsonify, request, render_template
  
# creating a Flask app
app = Flask(__name__)

rate_change = False

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

# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
  
    return jsonify({'data': num**2})


@app.route('/api/v1/users/', methods=['POST'])
def create_user():
    print('ENTRO')
    try:
        json = request.get_json(force=True)
        print(json)
    except:
        print('error handleado')
    print('CREATE_USER')
    print(rate_change)
    print('--------------')

    return jsonify({'changes': rate_change})

@app.route('/api/settings/', methods=['GET']) 
def get_timestamp():

    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
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
    # rate_change = False
    return jsonify(rates)


# driver function
if __name__ == '__main__':
  
    app.run(host='0.0.0.0',port=5000,debug=True)