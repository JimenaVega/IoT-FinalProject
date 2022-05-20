# Using flask to make an api
# import necessary libraries and functions
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
  
# driver function
if __name__ == '__main__':
  
    app.run(host='0.0.0.0',port=5000,debug=True)