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
    return render_template('index.html', todos=all_pycom)

