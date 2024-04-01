import os
import json
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

@app.route('/getName', methods=['GET'])
def get_name():
    return jsonify({'name': 'Bob'})
