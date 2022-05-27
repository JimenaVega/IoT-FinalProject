# Using flask to make an api
# import necessary libraries and functions
import datetime
from distutils.log import debug
from flask import Flask, jsonify, request
  
# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})

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
        # json = request.args.get(1)
        print(json)
    except:
        print('error handleado')
  

    return jsonify({'user': 'holi'})

@app.route('/api/settings/', methods=['GET']) 
def get_timestamp():

    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
    print(unix_timestamp)
    
    return jsonify({"ts":unix_timestamp})
  
@app.route('/api/rates/', methods=['GET'])
def get_rates():
    
    rates = {
            'transmission_rate':2,
            'acceleration_rate':12,
            'light_rate':11,
            'temperature_rate':11,
            'humidity_rate':5,
            'altitude_rate':5,
            'battery_voltage_rate':5,
            'roll_rate':5,
            'pitch_rate':5
         }

    return jsonify(rates)


# driver function
if __name__ == '__main__':
  
    app.run(host='0.0.0.0',port=5000,debug=True)