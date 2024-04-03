import os
import json
import requests
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def hello():
    r = requests.get('http://name-svc:80') 
    # return r.json()

    # if r.status_code == 200:
    #     print("Request successful")
    #     print(r.text)
    # else:
    #     print("Request failed with status code:", r.status_code)
    data = r.json()
    print(data)
    return render_template('index.html', username=data['name'])

if __name__ == '__main__':
    app.run(debug=True)

