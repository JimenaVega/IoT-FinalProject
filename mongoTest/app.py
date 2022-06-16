from flask import Flask,  render_template, request, url_for, redirect
from pymongo import MongoClient

# Running on http://127.0.0.1:3000

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
# create a collection 
pycom = db.pycom

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        transmission_rate = request.form['transmission_rate']
        acceleration_rate = request.form['acceleration_rate']
        light_rate = request.form['light_rate']
        temperature_rate = request.form['temperature_rate']
        humidity_rate = request.form['humidity_rate']
        altitude_rate = request.form['altitude_rate']
        battery_voltage_rate = request.form['battery_voltage_rate']
        roll_rate = request.form['roll_rate']
        pitch_rate = request.form['pitch_rate']

        degree = request.form['degree']
        pycom.insert_one({
                            'content':content,
                            'degree': degree
                         })
        return redirect(url_for('index'))


    # pycom.insert_one({
    #                 'transmission_rate':transmission_rate,
    #                 'acceleration_rate':acceleration_rate,
    #                 'light_rate':light_rate,
    #                 'temperature_rate':temperature_rate,
    #                 'humidity_rate':humidity_rate,
    #                 'altitude_rate':altitude_rate,
    #                 'battery_voltage_rate':battery_voltage_rate,
    #                 'roll_rate':roll_rate,
    #                 'pitch_rate':pitch_rate,
    #                 'degree': degree
    #                 })

    all_pycom = pycom.find()
    return render_template('index.html', pycom=all_pycom)