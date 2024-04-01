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
    r = requests.get('name-service-svc.default.svc.cluster.local:31313')    
    # r = requests.get('http://localhost:31313/getName')
    data = r.json()
    print(data)
    return render_template('index.html', username = str(data.name))

if __name__ == '__main__':
    app.run(debug=True)

